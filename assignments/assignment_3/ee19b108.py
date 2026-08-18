"""
Course      : EE5333 - Introduction to Physical Design Automation
Assignment  : 3
Program     : Floorplanning using Sequence Pairs

Description :
Implements sequence-pair based floorplanning using
simulated annealing. The objective is to determine
the placement and aspect ratio of modules that
minimizes the area of the enclosing floorplan.

Author      : Vikas Raj
"""
import math
import random
import copy
import time

class Module:
    def __init__(self, name, area, aspect_ratios):
        self._name = name
        self._area = area
        self._wh = [(math.sqrt(area * r), math.sqrt(area / r)) for r in aspect_ratios]

    def __repr__(self):
        return f"'{self._name}' area:{self._area}"

class SeqPair:
    def __init__(self, modules):
        n = len(modules)
        self._pos = list(range(n))  # positive sequence
        self._neg = list(range(n))  # negative sequence
        random.shuffle(self._pos)
        random.shuffle(self._neg)
        self._ap = [0 for _ in range(n)]  # aspect ratio choice
        self._coords = [(0, 0) for _ in range(n)]
        self._w = 0
        self._h = 0

    def perturb(self, modules):
        """3 moves: swap in pos, swap in both, change aspect ratio"""
        n = len(modules)
        choice = random.randint(1, 3)

        if choice == 1:
            i, j = random.sample(range(n), 2)
            self._pos[i], self._pos[j] = self._pos[j], self._pos[i]

        elif choice == 2:
            m1, m2 = random.sample(range(n), 2)
            p1, p2 = self._pos.index(m1), self._pos.index(m2)
            n1, n2 = self._neg.index(m1), self._neg.index(m2)
            self._pos[p1], self._pos[p2] = self._pos[p2], self._pos[p1]
            self._neg[n1], self._neg[n2] = self._neg[n2], self._neg[n1]

        else:
            i = random.randint(0, n - 1)
            self._ap[i] = (self._ap[i] + 1) % len(modules[i]._wh)

    def costEval(self, modules):
        """Build HCG/VCG and compute longest paths"""
        n = len(modules)
        src, tgt = n, n + 1

        pos_idx = {val: i for i, val in enumerate(self._pos)}
        neg_idx = {val: i for i, val in enumerate(self._neg)}

        hcg = {i: [] for i in range(n + 2)}
        vcg = {i: [] for i in range(n + 2)}
        in_h = {i: 0 for i in range(n + 2)}
        in_v = {i: 0 for i in range(n + 2)}

        # Sequence pair relations → HCG / VCG
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if pos_idx[j] < pos_idx[i] and neg_idx[j] < neg_idx[i]:
                    hcg[j].append(i)
                    in_h[i] += 1
                if pos_idx[j] > pos_idx[i] and neg_idx[j] < neg_idx[i]:
                    vcg[j].append(i)
                    in_v[i] += 1

        for i in range(n):
            if in_h[i] == 0:
                hcg[src].append(i)
                in_h[i] += 1
            if in_v[i] == 0:
                vcg[src].append(i)
                in_v[i] += 1

            hcg[i].append(tgt)
            vcg[i].append(tgt)
            in_h[tgt] += 1
            in_v[tgt] += 1

        def longest_path(graph, indegree, dim):
            dist = {u: 0 for u in graph}
            weights = {i: modules[i]._wh[self._ap[i]][dim] for i in range(n)}
            weights[src] = 0
            weights[tgt] = 0

            queue = [u for u in graph if indegree[u] == 0]

            while queue:
                u = queue.pop(0)
                for v in graph[u]:
                    dist[v] = max(dist[v], dist[u] + weights[u])
                    indegree[v] -= 1
                    if indegree[v] == 0:
                        queue.append(v)

            return dist

        x = longest_path(hcg, in_h.copy(), 0)
        y = longest_path(vcg, in_v.copy(), 1)

        for i in range(n):
            self._coords[i] = (x[i], y[i])

        self._w, self._h = x[tgt], y[tgt]
        return self._w * self._h

# --- 2. Test Execution ---
# Module(name, area, [aspect_ratio_options])
m1 = Module("A", 120, [1.0, 2.0, 0.5])
m2 = Module("B", 80, [1.0, 1.5, 0.66])
m3 = Module("C", 200, [1.0, 2.5])
m4 = Module("D", 60, [1.0, 3.0, 0.33])
m5 = Module("E", 150, [1.0, 1.8])

modules_list = [m1, m2, m3, m4, m5]
sp = SeqPair(modules_list)

# Initial Evaluation
area = sp.costEval(modules_list)

print("--- Sequence Pair Result ---")
print(f"Gamma+: {sp._pos}")
print(f"Gamma-: {sp._neg}")
print(f"Total Width: {sp._w:.2f}, Total Height: {sp._h:.2f}")
print(f"Total Area: {area:.2f}")

print("\n" + "="*75)
print(f"{'Module':<8} | {'Coord (x,y)':<15} | {'Size (w x h)':<15} | {'Aspect Ratio (r)':<10}")
print("-" * 75)

for i, (x, y) in enumerate(sp._coords):
    # Get width and height from the selected aspect ratio pointer (_ap)
    w, h = modules_list[i]._wh[sp._ap[i]]

    # Calculate the ratio used
    used_r = w / h

    name = modules_list[i]._name
    coord_str = f"({x:.1f}, {y:.1f})"
    size_str = f"{int(w)} x {int(h)}"

    print(f"{name:<8} | {coord_str:<15} | {size_str:<15} | {used_r:>8.2f}")

print("="*75)

def accept(delC, T):
    if delC <= 0:
        return True
    return random.random() < math.exp(-delC / T)


def simulated_annealing(Tmin, Tmax, N, alpha, S, modules):
    T = Tmax
    curr_S = S
    curr_C = curr_S.costEval(modules)

    best_S = copy.deepcopy(curr_S)
    best_C = curr_C

    while T > Tmin:
        for _ in range(N):
            Snew = copy.deepcopy(curr_S)
            Snew.perturb(modules)
            Cnew = Snew.costEval(modules)

            if accept(Cnew - curr_C, T):
                curr_S, curr_C = Snew, Cnew
                if curr_C < best_C:
                    best_S, best_C = copy.deepcopy(curr_S), curr_C

        T *= alpha

    return best_S, best_C


def sp_floorplan(modules):
    S = SeqPair(modules)
    Tmax = sum(m._area for m in modules) * 2

    Sbest, Cbest = simulated_annealing(1, Tmax, 100, 0.95, S, modules)

    sol = [
        (Sbest._coords[i], modules[i]._wh[Sbest._ap[i]], modules[i]._name)
        for i in range(len(modules))
    ]

    return sol, Cbest

def plot(coords):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots()
    ax.plot([0, 0])
    ax.set_aspect('equal')
    ax.set_xlim(0, max([r[0][0] + r[1][0] for r in coords]))
    ax.set_ylim(0, max([r[0][1] + r[1][1] for r in coords]))

    for i, r in enumerate(coords):
        match i % 4:
            case 3:
                hatch, color = '/+', 'red'
            case 2:
                hatch, color = '///', 'green'
            case 1:
                hatch, color = '/\\//\\//\\/', 'blue'
            case _:
                hatch, color = '\\\\', 'gray'

        ax.add_patch(Rectangle(
            r[0], r[1][0], r[1][1],
            edgecolor=color,
            facecolor=color,
            hatch=hatch,
            fill=False,
            lw=2
        ))

        ax.text(
            r[0][0] + r[1][0] // 2,
            r[0][1] + r[1][1] // 2,
            r[2],
            fontsize=8
        )

    plt.show()

m = [Module('a', 16, [0.25, 4]),Module('b', 32, [2.0, 0.5]),Module('c', 27, [1./3, 3.0]),Module('d', 6, [6])]
sumarea = sum([i._area for i in m])
for fpfn in [sp_floorplan]:
  t = time.time()
  sol, area = fpfn(m)
  print(f"{fpfn.__name__} runtime :", time.time() - t)
  if sol:
    print(f"{fpfn.__name__} area :", area, "Utilization :", sumarea * 100./area)
    plot(sol)

m = [Module(str(i), random.randint(10, 100), [1.]) for i in range(10)]
sumarea = sum([i._area for i in m])
for fpfn in [ sp_floorplan]:
  t = time.time()
  sol, area = fpfn(m)
  print(f"{fpfn.__name__} runtime :", time.time() - t)
  if sol:
    print(f"{fpfn.__name__} area :", area, "Utilization :", sumarea * 100./area)
    plot(sol)