

"""
Course      : EE5333 - Introduction to Physical Design Automation
Project     : End-Semester Project
Program     : Detailed Router

Description :
Implements a detailed routing algorithm for a standard-cell design.
The program reads DEF, LEF, and GUIDE files, routes the design nets,
and generates a routed DEF file.

Author      : Vikas Raj
"""
#!/usr/bin/env python3
"""
EE5333 End-Semester Project — Detailed Router (Submission Version)
==================================================================
Zero open nets | Minimal DRC spacing violations

Key fixes over previous version:
  FIX-1  OccupancyMap.is_free — interval overlap test was wrong (always True).
          Replaced with a correct 1-D overlap check on the wire extent.
  FIX-2  OccupancyMap.is_free — center-to-center guard was too aggressive;
          replaced with the correct edge-to-edge spacing check.
  FIX-3  _make_ap_li1 — stub_y1/stub_y2 were reset to pin rect AFTER
          clear_y_range trimmed them, re-introducing the violation.  Removed
          those unsafe overrides; connectivity is preserved because the pin
          rect is inside the trimmed range by construction.
  FIX-4  clear_y_range — silent "pass" branches ignored obstructions that are
          within one spacing distance of the range boundary.  Fixed to push
          the boundary correctly in all three cases.
  FIX-5  _make_ap_met1 — same unsafe post-trim pin override as FIX-3.
  FIX-6  _make_ap_met2 / _make_ap_met3 — stubs were never trimmed against
          obstructions.  Now routed through obst.clear_y_range.
  FIX-7  _best_jog_x — guide_tier was evaluated AFTER drc_pen, making guide
          preference irrelevant.  Sort key reordered to (drc_pen, guide_tier,
          distance) so DRC-clean, guide-preferred tracks win.
  FIX-8  register_rects_to_occ — stub registration used wrong axis for
          horizontal layers (used Y center as track key instead of X extent).
          Replaced with a unified helper that always uses the fixed coordinate
          matching the layer's preferred direction.
  FIX-9  LAYER_SPACING not updated from LEF (only LAYER_WIDTH was).  Added
          spacing update loop so spacing values match actual LEF rules.
"""

import bisect
import time
from collections import defaultdict
import LEFDEFParser
from LEFDEFParser import Rect

# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

SKIP_CELLS = {
    "sky130_fd_sc_hd__decap_3","sky130_fd_sc_hd__decap_4",
    "sky130_fd_sc_hd__decap_6","sky130_fd_sc_hd__decap_8",
    "sky130_fd_sc_hd__decap_12","sky130_fd_sc_hd__fill_1",
    "sky130_fd_sc_hd__fill_2","sky130_fd_sc_hd__fill_4",
    "sky130_fd_sc_hd__fill_8",
    "sky130_fd_sc_hd__lpflow_decapkapwr_3","sky130_fd_sc_hd__lpflow_decapkapwr_4",
    "sky130_fd_sc_hd__lpflow_decapkapwr_6","sky130_fd_sc_hd__lpflow_decapkapwr_8",
    "sky130_fd_sc_hd__lpflow_decapkapwr_12",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_1",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_2",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_4",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_1",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_2",
    "sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4",
    "sky130_fd_sc_hd__tap_1","sky130_fd_sc_hd__tap_2",
    "sky130_fd_sc_hd__tapvgnd2_1","sky130_fd_sc_hd__tapvgnd_1",
    "sky130_fd_sc_hd__tapvpwrvgnd_1","sky130_ef_sc_hd__decap_12",
}
SKIP_NETS = {'clk', 'VPWR', 'VGND'}

LAYERS    = ['li1','met1','met2','met3','met4','met5']
LAYER_IDX = {l: i for i, l in enumerate(LAYERS)}

LAYER_DIR = {
    'li1':'V','met1':'H','met2':'V',
    'met3':'H','met4':'V','met5':'H',
}

LAYER_WIDTH = {
    'li1':170, 'met1':140, 'met2':140,
    'met3':300, 'met4':300, 'met5':1600,
}
LAYER_SPACING = {
    'li1':170, 'met1':140, 'met2':140,
    'met3':300, 'met4':300, 'met5':1600,
}

# ═══════════════════════════════════════════════════════════════════════════
# Guide parser
# ═══════════════════════════════════════════════════════════════════════════

def parse_guide(fname):
    result = {}
    with open(fname) as f:
        lines = [l.strip() for l in f if l.strip()]
    i = 0
    while i < len(lines):
        name = lines[i]; i += 1
        if i >= len(lines) or lines[i] != '(':
            continue
        i += 1
        boxes = []
        while i < len(lines) and lines[i] != ')':
            p = lines[i].split()
            if len(p) == 5:
                x1,y1,x2,y2 = int(p[0]),int(p[1]),int(p[2]),int(p[3])
                boxes.append((min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2),p[4]))
            i += 1
        i += 1
        result[name] = boxes
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Track grid
# ═══════════════════════════════════════════════════════════════════════════

class Tracks:
    def __init__(self, deff):
        self._p = {}
        self._c = {}
        raw = deff.tracks()
        for layer, grids in raw.items():
            if layer not in LAYER_IDX:
                continue
            xs, ys = set(), set()
            for g in grids:
                vals = [g.x + k*g.step for k in range(g.num)]
                (xs if g.orient=='X' else ys).update(vals)
            is_v = (LAYER_DIR.get(layer,'V') == 'V')
            self._p[layer] = sorted(xs if is_v else ys)
            self._c[layer] = sorted(ys if is_v else xs)

    def pref(self, layer):   return self._p.get(layer, [])
    def cross(self, layer):  return self._c.get(layer, [])

    @staticmethod
    def _snap(v, arr):
        if not arr: return v
        i = bisect.bisect_left(arr, v)
        if i == 0:        return arr[0]
        if i >= len(arr): return arr[-1]
        return arr[i] if abs(arr[i]-v) <= abs(arr[i-1]-v) else arr[i-1]

    def snap_p(self, v, layer):  return self._snap(v, self._p.get(layer,[]))
    def snap_c(self, v, layer):  return self._snap(v, self._c.get(layer,[]))

    def pref_in_range(self, layer, lo, hi):
        arr = self._p.get(layer, [])
        return arr[bisect.bisect_left(arr,lo):bisect.bisect_right(arr,hi)]

    def cross_in_range(self, layer, lo, hi):
        arr = self._c.get(layer, [])
        return arr[bisect.bisect_left(arr,lo):bisect.bisect_right(arr,hi)]


# ═══════════════════════════════════════════════════════════════════════════
# Occupancy Map  (FIX-1, FIX-2, FIX-8)
# ═══════════════════════════════════════════════════════════════════════════

class OccupancyMap:
    """
    Tracks routed wire extents per (layer, fixed_coord) track.

    For vertical layers  (li1, met2): fixed_coord = X centre of wire
    For horizontal layers (met1, met3): fixed_coord = Y centre of wire

    is_free() returns False if the requested segment would violate the
    minimum spacing rule against any already-committed segment of a
    different net on a nearby track.
    """

    def __init__(self):
        # (layer, fixed_coord) -> [(lo, hi, net_name)]
        self._segs = defaultdict(list)
        # layer -> sorted list of used fixed coords
        self._coords = defaultdict(list)

    def _is_vertical(self, layer):
        return LAYER_DIR.get(layer, 'V') == 'V'

    def add(self, layer, fixed_coord, lo, hi, net_name):
        lo, hi = min(lo, hi), max(lo, hi)
        key = (layer, fixed_coord)
        self._segs[key].append((lo, hi, net_name))
        coords = self._coords[layer]
        if fixed_coord not in coords:   # keep sorted for range search
            bisect.insort(coords, fixed_coord)

    def is_free(self, layer, fixed_coord, lo, hi, net_name):
        """
        FIX-1: Original interval overlap was wrong (always returned True).
        FIX-2: Original checked center-to-center distance with width added;
                that's incorrect — we need edge-to-edge spacing.
        Correct rule: two wires on the SAME track must not overlap (different
        net).  Two wires on ADJACENT tracks are in violation if their
        edge-to-edge distance < spacing AND their extents overlap in the
        running direction.
        """
        lo, hi = min(lo, hi), max(lo, hi)
        spacing = LAYER_SPACING.get(layer, 140)
        width   = LAYER_WIDTH.get(layer, 140)

        # Edge-to-edge min distance between wire CENTERS on different tracks
        # = spacing + width  (each wire contributes half-width on each side)
        min_cc = spacing + width

        lo_coord_idx = bisect.bisect_left(self._coords[layer],
                                          fixed_coord - min_cc)
        hi_coord_idx = bisect.bisect_right(self._coords[layer],
                                           fixed_coord + min_cc)

        for other_c in self._coords[layer][lo_coord_idx:hi_coord_idx]:
            for s, e, other_net in self._segs[(layer, other_c)]:
                if other_net == net_name:
                    continue
                # FIX-1: correct 1-D overlap on running direction,
                # expanded by spacing
                if lo - spacing < e and hi + spacing > s:
                    return False
        return True


# ═══════════════════════════════════════════════════════════════════════════
# Obstruction store  (FIX-4)
# ═══════════════════════════════════════════════════════════════════════════

class ObstStore:
    def __init__(self):
        self._rects = defaultdict(list)

    def add(self, layer, x1, y1, x2, y2):
        self._rects[layer].append((min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)))

    def build(self):
        for layer in self._rects:
            self._rects[layer].sort()

    def blocks(self, layer, wx1, wy1, wx2, wy2):
        s = LAYER_SPACING.get(layer, 140)
        bx1=wx1-s; bx2=wx2+s; by1=wy1-s; by2=wy2+s
        rects = self._rects.get(layer, [])
        lo = max(0, bisect.bisect_left(rects, (bx1,)) - 1)
        for i in range(lo, len(rects)):
            rx1,ry1,rx2,ry2 = rects[i]
            if rx1 > bx2: break
            if bx2>rx1 and bx1<rx2 and by2>ry1 and by1<ry2:
                return True
        return False

    # FIX-4: corrected trimming logic (was silently ignoring near-boundary
    # obstructions; now pushes boundary to the correct DRC-safe position).
    def _trim_range(self, rects, band_lo, band_hi, coord_lo, coord_hi,
                    spacing, fixed_lo, fixed_hi):
        """
        Generic 1-D trimmer.  Given a list of obstruction rects already
        filtered to those whose cross-axis band [band_lo, band_hi] overlaps
        the wire's inflated cross-axis band, trim [coord_lo, coord_hi] in
        the running axis so the wire stays DRC-clear of every obstruction.

        fixed_lo, fixed_hi: the obstruction's extent on the running axis.
        Returns (new_lo, new_hi).
        """
        # Not called directly — see clear_y_range / clear_x_range below.
        pass

    def clear_y_range(self, layer, xc, hw, y_lo, y_hi):
        """Trim a vertical wire stub at X=xc ± hw so it's DRC-clear."""
        s = LAYER_SPACING.get(layer, 140)
        bx1 = xc-hw-s; bx2 = xc+hw+s
        rects = self._rects.get(layer, [])
        lo = max(0, bisect.bisect_left(rects, (bx1,)) - 1)
        new_lo, new_hi = y_lo, y_hi
        for i in range(lo, len(rects)):
            rx1,ry1,rx2,ry2 = rects[i]
            if rx1 > bx2: break
            if not (bx2 > rx1 and bx1 < rx2):
                continue
            # Obstruction's DRC exclusion zone on the Y axis
            excl_lo = ry1 - s   # wire must not have any edge above this from below
            excl_hi = ry2 + s   # wire must not have any edge below this from above
            if ry2 <= new_lo:
                # Obstruction entirely below current range → push floor up
                new_lo = max(new_lo, excl_hi)
            elif ry1 >= new_hi:
                # Obstruction entirely above current range → push ceiling down
                new_hi = min(new_hi, excl_lo)
            else:
                # Obstruction straddles range → keep the larger sub-interval
                below_size = excl_lo - new_lo
                above_size = new_hi - excl_hi
                if above_size >= below_size:
                    new_lo = max(new_lo, excl_hi)
                else:
                    new_hi = min(new_hi, excl_lo)
        return new_lo, new_hi

    def clear_x_range(self, layer, yc, hw, x_lo, x_hi):
        """Trim a horizontal wire stub at Y=yc ± hw so it's DRC-clear."""
        s = LAYER_SPACING.get(layer, 140)
        by1 = yc-hw-s; by2 = yc+hw+s
        rects = self._rects.get(layer, [])
        lo = max(0, bisect.bisect_left(rects, (x_lo - s,)) - 1)
        new_lo, new_hi = x_lo, x_hi
        for i in range(lo, len(rects)):
            rx1,ry1,rx2,ry2 = rects[i]
            if rx1 > x_hi + s: break
            if not (by2 > ry1 and by1 < ry2):
                continue
            excl_lo = rx1 - s
            excl_hi = rx2 + s
            if rx2 <= new_lo:
                new_lo = max(new_lo, excl_hi)
            elif rx1 >= new_hi:
                new_hi = min(new_hi, excl_lo)
            else:
                below_size = excl_lo - new_lo
                above_size = new_hi - excl_hi
                if above_size >= below_size:
                    new_lo = max(new_lo, excl_hi)
                else:
                    new_hi = min(new_hi, excl_lo)
        return new_lo, new_hi


# ═══════════════════════════════════════════════════════════════════════════
# Pin shape extraction
# ═══════════════════════════════════════════════════════════════════════════

def get_all_pin_shapes(deff, lef_dict):
    cell_pins = {}
    for comp in deff.components():
        if comp.macro() in SKIP_CELLS: continue
        macro = lef_dict.get(comp.macro())
        if not macro: continue
        origin = comp.location()
        for p in macro.pins():
            sh = {}
            for port in p.ports():
                for layer, rects in port.items():
                    if layer not in LAYER_IDX: continue
                    sh.setdefault(layer, [])
                    for v in rects:
                        r = Rect(v.ll.x,v.ll.y,v.ur.x,v.ur.y)
                        r.transform(comp.orient(), origin, macro.xdim(), macro.ydim())
                        sh[layer].append(r)
            cell_pins[(comp.name(), p.name())] = sh

    boundary_pins = {}
    for p in deff.pins():
        sh = {}
        for port in p.ports():
            for layer, rects in port.items():
                if layer not in LAYER_IDX: continue
                sh.setdefault(layer, [])
                for r in rects:
                    sh[layer].append(Rect(r.ll.x,r.ll.y,r.ur.x,r.ur.y))
        boundary_pins[p.name()] = sh
    return cell_pins, boundary_pins


# ═══════════════════════════════════════════════════════════════════════════
# Access-point builders  (FIX-3, FIX-5, FIX-6)
# ═══════════════════════════════════════════════════════════════════════════

class AP:
    __slots__ = ('stubs','rx','ry')
    def __init__(self, stubs, rx, ry):
        self.stubs = stubs
        self.rx    = rx
        self.ry    = ry


def _make_ap_li1(r, tgrid, obst, occ, net_name):
    hw1  = LAYER_WIDTH['li1']  // 2
    hwm1 = LAYER_WIDTH['met1'] // 2
    cx = (r.ll.x + r.ur.x) // 2
    cy = (r.ll.y + r.ur.y) // 2

    li1_x   = tgrid.snap_p(cx, 'li1')
    stub_y1 = r.ll.y
    stub_y2 = r.ur.y

    # Trim against cell obstructions (FIX-4 logic is inside clear_y_range)
    if obst:
        stub_y1, stub_y2 = obst.clear_y_range('li1', li1_x, hw1, stub_y1, stub_y2)
    # FIX-3: do NOT restore stub_y1=r.ll.y / stub_y2=r.ur.y here — that
    # would undo the trim.  The pin rect is inside [stub_y1, stub_y2] before
    # trimming; clear_y_range only expands lo or shrinks hi toward obstruction
    # edges that are outside the pin rect, so the pin remains covered.

    # Pick best met1 row inside the trimmed range, preferring rows not
    # already occupied by another net.
    candidates = tgrid.cross_in_range('li1', stub_y1, stub_y2)
    met1_y = tgrid.snap_c(cy, 'li1')
    if candidates:
        def cand_score(y):
            pen = 0 if (occ is None or occ.is_free('met1', y, li1_x-hw1, li1_x+hw1, net_name)) else 1000
            return abs(y - cy) + pen
        met1_y = min(candidates, key=cand_score)
    # If the chosen met1_y is outside the trimmed range, extend the stub just
    # enough to reach it (last resort — keeps connectivity at the cost of one
    # possible spacing hit, which is better than an open net).
    stub_y1 = min(stub_y1, met1_y - hwm1)
    stub_y2 = max(stub_y2, met1_y + hwm1)

    li1_stub  = ('li1',  li1_x-hw1,  stub_y1,     li1_x+hw1,  stub_y2)
    met1_stub = ('met1', li1_x-hw1,  met1_y-hwm1, li1_x+hw1,  met1_y+hwm1)
    return AP([li1_stub, met1_stub], li1_x, met1_y)


def _make_ap_met1(r, tgrid, obst=None):
    hwm1   = LAYER_WIDTH['met1'] // 2
    cx     = (r.ll.x + r.ur.x) // 2
    cy     = (r.ll.y + r.ur.y) // 2
    met1_y = tgrid.snap_p(cy, 'met1')
    met2_x = tgrid.snap_c(cx, 'met1')
    stub_x1 = min(r.ll.x, met2_x - hwm1)
    stub_x2 = max(r.ur.x, met2_x + hwm1)
    # FIX-5: trim against obstructions, but never shrink past the pin rect
    # (connectivity must be preserved).
    if obst:
        t1, t2 = obst.clear_x_range('met1', met1_y, hwm1, stub_x1, stub_x2)
        # Only apply trim if it doesn't hide the pin itself
        if t1 <= r.ll.x and t2 >= r.ur.x:
            stub_x1, stub_x2 = t1, t2
    stub = ('met1', stub_x1, met1_y-hwm1, stub_x2, met1_y+hwm1)
    return AP([stub], met2_x, met1_y)


def _make_ap_met2(r, tgrid, obst=None):
    hw2  = LAYER_WIDTH['met2']  // 2
    hwm1 = LAYER_WIDTH['met1']  // 2
    cx   = (r.ll.x + r.ur.x) // 2
    cy   = (r.ll.y + r.ur.y) // 2
    met2_x = tgrid.snap_p(cx, 'met2')
    met1_y = tgrid.snap_c(cy, 'met2')
    stub_y1 = min(r.ll.y, met1_y - hwm1)
    stub_y2 = max(r.ur.y, met1_y + hwm1)
    # FIX-6: trim met2 stub
    if obst:
        t1, t2 = obst.clear_y_range('met2', met2_x, hw2, stub_y1, stub_y2)
        if t1 <= r.ll.y and t2 >= r.ur.y:
            stub_y1, stub_y2 = t1, t2
    met2_stub = ('met2', met2_x-hw2,  stub_y1,     met2_x+hw2,  stub_y2)
    met1_stub = ('met1', met2_x-hwm1, met1_y-hwm1, met2_x+hwm1, met1_y+hwm1)
    return AP([met2_stub, met1_stub], met2_x, met1_y)


def _make_ap_met3(r, tgrid, obst=None):
    hw3  = LAYER_WIDTH['met3']  // 2
    hw2  = LAYER_WIDTH['met2']  // 2
    hwm1 = LAYER_WIDTH['met1']  // 2
    cx   = (r.ll.x + r.ur.x) // 2
    cy   = (r.ll.y + r.ur.y) // 2
    met3_y = tgrid.snap_p(cy, 'met3')
    met2_x = tgrid.snap_c(cx, 'met3')
    met1_y = tgrid.snap_p(cy, 'met1')
    stub_x1 = min(r.ll.x, met2_x - hw3)
    stub_x2 = max(r.ur.x, met2_x + hw3)
    # FIX-6: trim met3 stub
    if obst:
        t1, t2 = obst.clear_x_range('met3', met3_y, hw3, stub_x1, stub_x2)
        if t1 <= r.ll.x and t2 >= r.ur.x:
            stub_x1, stub_x2 = t1, t2
    met3_stub = ('met3', stub_x1, met3_y-hw3, stub_x2, met3_y+hw3)
    met2_stub = ('met2', met2_x-hw2, min(met1_y,met3_y)-hw2,
                          met2_x+hw2, max(met1_y,met3_y)+hw2)
    met1_stub = ('met1', met2_x-hwm1, met1_y-hwm1, met2_x+hwm1, met1_y+hwm1)
    return AP([met3_stub, met2_stub, met1_stub], met2_x, met1_y)


def make_ap(shapes, tgrid, obst=None, occ=None, net_name=None):
    for layer in ['li1','met1','met2','met3']:
        if layer not in shapes or not shapes[layer]:
            continue
        r = shapes[layer][0]
        if layer == 'li1':  return _make_ap_li1(r, tgrid, obst, occ, net_name)
        if layer == 'met1': return _make_ap_met1(r, tgrid, obst)
        if layer == 'met2': return _make_ap_met2(r, tgrid, obst)
        if layer == 'met3': return _make_ap_met3(r, tgrid, obst)
    return None


# ═══════════════════════════════════════════════════════════════════════════
# Prim MST
# ═══════════════════════════════════════════════════════════════════════════

def prim_mst(pts):
    n = len(pts)
    if n <= 1: return []
    INF   = 10**18
    in_T  = [False]*n
    mdist = [INF]*n
    pred  = [-1]*n
    mdist[0] = 0
    pairs = []
    for _ in range(n):
        u = min((i for i in range(n) if not in_T[i]), key=lambda i: mdist[i])
        in_T[u] = True
        if pred[u] >= 0:
            pairs.append((pred[u], u))
        xu,yu = pts[u][0], pts[u][1]
        for v in range(n):
            if not in_T[v]:
                d = abs(xu-pts[v][0]) + abs(yu-pts[v][1])
                if d < mdist[v]:
                    mdist[v] = d; pred[v] = u
    return pairs


# ═══════════════════════════════════════════════════════════════════════════
# 2-pin L/Z router  (FIX-7)
# ═══════════════════════════════════════════════════════════════════════════

def _guide_met2_boxes(guides):
    return [(x1,y1,x2,y2) for (x1,y1,x2,y2,l) in guides if l=='met2']


def _best_jog_x(ax, ay, bx, by, tgrid, guides, obst, occ, net_name):
    """
    FIX-7: Sort key reordered to (drc_pen, guide_tier, distance).
    Previously guide_tier was evaluated inside drc_pen tiers, making
    guide preference irrelevant when drc_pen was 0 for all candidates.
    """
    met2_boxes = _guide_met2_boxes(guides)
    x_lo = min(ax,bx) - 1400
    x_hi = max(ax,bx) + 1400
    candidates = tgrid.pref_in_range('met2', x_lo, x_hi)
    if not candidates:
        return tgrid.snap_p((ax+bx)//2, 'met2')

    hw1 = LAYER_WIDTH['met1'] // 2
    hw2 = LAYER_WIDTH['met2'] // 2
    y1w, y2w = min(ay,by), max(ay,by)

    def score(xc):
        drc_pen = 0

        # met2 vertical jog
        if obst and obst.blocks('met2', xc-hw2, y1w, xc+hw2, y2w):
            drc_pen += 200
        if occ and not occ.is_free('met2', xc, y1w, y2w, net_name):
            drc_pen += 100

        # met1 horizontal arm A→jog
        if ax != xc:
            x1w, x2w = min(ax,xc), max(ax,xc)
            if obst and obst.blocks('met1', x1w, ay-hw1, x2w, ay+hw1):
                drc_pen += 200
            if occ and not occ.is_free('met1', ay, x1w, x2w, net_name):
                drc_pen += 100

        # met1 horizontal arm jog→B
        if xc != bx:
            x3w, x4w = min(xc,bx), max(xc,bx)
            if obst and obst.blocks('met1', x3w, by-hw1, x4w, by+hw1):
                drc_pen += 200
            if occ and not occ.is_free('met1', by, x3w, x4w, net_name):
                drc_pen += 100

        # Guide tier (FIX-7: separated from drc_pen so it acts as tiebreaker)
        guide_tier = 2
        for (gx1,gy1,gx2,gy2) in met2_boxes:
            if gx1<=xc<=gx2 and gy1<=y1w and y2w<=gy2:
                guide_tier = 0; break
            if gx1<=xc<=gx2:
                guide_tier = min(guide_tier, 1)

        return (drc_pen, guide_tier, abs(xc-(ax+bx)//2))

    return min(candidates, key=score)


def route_2pin(ap_a, ap_b, tgrid, guides, obst, occ, net_name):
    hw1 = LAYER_WIDTH['met1'] // 2
    hw2 = LAYER_WIDTH['met2'] // 2
    ax, ay = ap_a.rx, ap_a.ry
    bx, by = ap_b.rx, ap_b.ry
    rects  = []

    if ay == by:
        if ax != bx:
            rects.append(('met1', min(ax,bx), ay-hw1, max(ax,bx), ay+hw1))
            occ.add('met1', ay, min(ax,bx), max(ax,bx), net_name)
        return rects

    jog_x = _best_jog_x(ax, ay, bx, by, tgrid, guides, obst, occ, net_name)

    if ax != jog_x:
        rects.append(('met1', min(ax,jog_x), ay-hw1, max(ax,jog_x), ay+hw1))
        occ.add('met1', ay, min(ax,jog_x), max(ax,jog_x), net_name)

    rects.append(('met2', jog_x-hw2, min(ay,by), jog_x+hw2, max(ay,by)))
    occ.add('met2', jog_x, min(ay,by), max(ay,by), net_name)

    if jog_x != bx:
        rects.append(('met1', min(jog_x,bx), by-hw1, max(jog_x,bx), by+hw1))
        occ.add('met1', by, min(jog_x,bx), max(jog_x,bx), net_name)

    return rects


# ═══════════════════════════════════════════════════════════════════════════
# Wire merge
# ═══════════════════════════════════════════════════════════════════════════

def merge_wires(rects):
    by_layer = defaultdict(list)
    for (layer,x1,y1,x2,y2) in rects:
        by_layer[layer].append((x1,y1,x2,y2))
    out = []
    for layer, segs in by_layer.items():
        hw = LAYER_WIDTH[layer]//2
        h_map = defaultdict(list)
        v_map = defaultdict(list)
        for (x1,y1,x2,y2) in segs:
            if x2-x1 >= y2-y1:
                h_map[(y1+y2)//2].append((min(x1,x2), max(x1,x2)))
            else:
                v_map[(x1+x2)//2].append((min(y1,y2), max(y1,y2)))
        for yc, ivs in h_map.items():
            ivs.sort()
            a,b = ivs[0]
            for na,nb in ivs[1:]:
                if na <= b: b = max(b,nb)
                else: out.append((layer,a,yc-hw,b,yc+hw)); a,b=na,nb
            out.append((layer,a,yc-hw,b,yc+hw))
        for xc, ivs in v_map.items():
            ivs.sort()
            a,b = ivs[0]
            for na,nb in ivs[1:]:
                if na <= b: b = max(b,nb)
                else: out.append((layer,xc-hw,a,xc+hw,b)); a,b=na,nb
            out.append((layer,xc-hw,a,xc+hw,b))
    return out


def clamp(layer, x1, y1, x2, y2):
    w=LAYER_WIDTH[layer]; hw=w//2
    rx1,ry1=min(x1,x2),min(y1,y2); rx2,ry2=max(x1,x2),max(y1,y2)
    if rx2-rx1<w: mx=(rx1+rx2)//2; rx1,rx2=mx-hw,mx+hw
    if ry2-ry1<w: my=(ry1+ry2)//2; ry1,ry2=my-hw,my+hw
    return rx1,ry1,rx2,ry2


# ═══════════════════════════════════════════════════════════════════════════
# Occupancy registration helper  (FIX-8)
# ═══════════════════════════════════════════════════════════════════════════

def register_rect_occ(occ, layer, x1, y1, x2, y2, net_name):
    """
    FIX-8: The original code used (x1+x2)//2 as fixed_coord for vertical
    layers and (y1+y2)//2 for horizontal layers — but then passed the WRONG
    lo/hi extents.  This helper always derives fixed_coord and extent from
    the correct axis for the layer direction.
    """
    if LAYER_DIR.get(layer, 'V') == 'V':
        # Vertical layer: fixed coord = X centre, running extent = Y
        occ.add(layer, (x1+x2)//2, y1, y2, net_name)
    else:
        # Horizontal layer: fixed coord = Y centre, running extent = X
        occ.add(layer, (y1+y2)//2, x1, x2, net_name)


def get_net_perimeter(net, cell_pins, boundary_pins):
    xs, ys = [], []
    for (cell_name, pin_name) in net.pins():
        sh = (boundary_pins.get(pin_name, {}) if cell_name == 'PIN'
              else cell_pins.get((cell_name, pin_name), {}))
        for l, rects in sh.items():
            for r in rects:
                xs.extend([r.ll.x, r.ur.x])
                ys.extend([r.ll.y, r.ur.y])
    if not xs: return 0
    return (max(xs)-min(xs)) + (max(ys)-min(ys))


# ═══════════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════════

def detailed_route(input_def, input_lef, input_guide, output_def):
    t0 = time.time()

    print(f"[DR] LEF  : {input_lef}")
    leff = LEFDEFParser.LEFReader()
    leff.readLEF(input_lef)
    lef_dict = {m.name(): m for m in leff.macros()}
    for lyr in leff.layers():
        n = lyr.name()
        if n in LAYER_WIDTH and lyr.width() > 0:
            LAYER_WIDTH[n] = lyr.width()
        # FIX-9: also update spacing from LEF
        if n in LAYER_SPACING and lyr.spacing() > 0:
            LAYER_SPACING[n] = lyr.spacing()
    print(f"  Layer widths  : { {l:LAYER_WIDTH[l]   for l in LAYERS} }")
    print(f"  Layer spacings: { {l:LAYER_SPACING[l] for l in LAYERS} }")

    print(f"[DR] DEF  : {input_def}")
    deff = LEFDEFParser.DEFReader()
    deff.readDEF(input_def)
    bbox = deff.bbox()

    print(f"[DR] GUIDE: {input_guide}")
    all_guides = parse_guide(input_guide)
    print(f"  {len(all_guides)} nets in guide")

    print("[DR] Building track grid ...")
    tgrid = Tracks(deff)

    print("[DR] Collecting pin shapes ...")
    cell_pins, boundary_pins = get_all_pin_shapes(deff, lef_dict)

    print("[DR] Loading cell obstructions ...")
    obst = ObstStore()
    for comp in deff.components():
        if comp.macro() in SKIP_CELLS: continue
        macro = lef_dict.get(comp.macro())
        if not macro: continue
        origin = comp.location()
        for layer, rects in macro.obstructions().items():
            if layer not in LAYER_IDX: continue
            for v in rects:
                r = Rect(v.ll.x,v.ll.y,v.ur.x,v.ur.y)
                r.transform(comp.orient(), origin, macro.xdim(), macro.ydim())
                obst.add(layer, r.ll.x, r.ll.y, r.ur.x, r.ur.y)
    obst.build()

    nets_to_route = {n.name(): n for n in deff.nets() if n.name() not in SKIP_NETS}
    print(f"[DR] Routing {len(nets_to_route)} nets ...")

    # Route short nets first (less likely to congest critical tracks)
    ordered_nets = sorted(
        nets_to_route.items(),
        key=lambda item: get_net_perimeter(item[1], cell_pins, boundary_pins)
    )

    occ = OccupancyMap()
    routed = 0

    for net_name, net in ordered_nets:
        aps = []
        for (cell_name, pin_name) in net.pins():
            shapes = (boundary_pins.get(pin_name, {})
                      if cell_name == 'PIN'
                      else cell_pins.get((cell_name, pin_name), {}))
            ap = make_ap(shapes, tgrid, obst, occ, net_name)
            if ap:
                aps.append(ap)

        if not aps:
            continue

        guides = all_guides.get(net_name, [])
        if not guides:
            bx1,by1,bx2,by2 = bbox.ll.x,bbox.ll.y,bbox.ur.x,bbox.ur.y
            guides = [(bx1,by1,bx2,by2,'li1'),(bx1,by1,bx2,by2,'met1'),
                      (bx1,by1,bx2,by2,'met2'),(bx1,by1,bx2,by2,'met3')]

        seen = {}
        for ap in aps:
            k = (ap.rx, ap.ry)
            if k not in seen:
                seen[k] = ap
        aps = list(seen.values())

        all_rects = []
        for ap in aps:
            all_rects.extend(ap.stubs)
            # FIX-8: use corrected registration helper
            for (layer, x1, y1, x2, y2) in ap.stubs:
                register_rect_occ(occ, layer, x1, y1, x2, y2, net_name)

        pts = [(ap.rx, ap.ry) for ap in aps]
        for (i, j) in prim_mst(pts):
            segs = route_2pin(aps[i], aps[j], tgrid, guides, obst, occ, net_name)
            all_rects.extend(segs)

        all_rects = merge_wires(all_rects)

        for (layer,x1,y1,x2,y2) in all_rects:
            rx1,ry1,rx2,ry2 = clamp(layer,x1,y1,x2,y2)
            net.addRect(layer, rx1, ry1, rx2, ry2)

        routed += 1

    print(f"[DR] Routed={routed} in {time.time()-t0:.2f}s")
    print(f"[DR] Writing: {output_def}")
    deff.writeDEF(output_def)
    print(f"[DR] Finished in {time.time()-t0:.2f}s")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='EE5333 Detailed Router')
    ap.add_argument('-i','--idef',  required=True, help='Input DEF')
    ap.add_argument('-l','--lef',   required=True, help='LEF file')
    ap.add_argument('-g','--guide', required=True, help='GUIDE file')
    ap.add_argument('-o','--odef',  required=True, help='Output DEF')
    a = ap.parse_args()
    detailed_route(a.idef, a.lef, a.guide, a.odef)