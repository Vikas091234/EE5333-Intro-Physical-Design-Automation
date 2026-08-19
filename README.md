# EE5333 — Introduction to Physical Design Automation

Coursework and end-semester project work from **EE5333 at IIT Madras**, covering algorithmic problems and implementation techniques used in VLSI physical design automation.

The repository contains six assignments and a detailed-routing project. The coursework covers graph optimization, hypergraph partitioning, floorplanning, SAT solving, graph isomorphism, and branch-and-bound ILP. The project works with LEF/DEF physical-design data and routing guides and contains a detailed router, checker, benchmark inputs, and selected routed DEF outputs.

## Repository structure

```text
.
├── README.md
├── REPORT.md
│
├── assignments/
│   ├── assignment_1/
│   │   ├── assignment1_statement.txt
│   │   ├── assignment_1.py
│   │   ├── ee19b108.py
│   │   ├── Introduction (1).ipynb
│   │   └── README.md
│   │
│   ├── assignment_2/
│   │   ├── assignement_2_statement.txt
│   │   ├── ee19b108.py
│   │   ├── FM_Partition.ipynb
│   │   └── README.md
│   │
│   ├── assignment_3/
│   │   ├── ee19b108.py
│   │   ├── EE5333_assgn3.pdf
│   │   ├── Floorplanning.ipynb
│   │   └── README.md
│   │
│   ├── assignment_4/
│   │   ├── CNF_Examples/
│   │   │   ├── 1.cnf
│   │   │   ├── uf20-01.cnf
│   │   │   ├── uf20-02.cnf
│   │   │   ├── uf20-03.cnf
│   │   │   ├── uf20-04.cnf
│   │   │   └── uf20-05.cnf
│   │   ├── ee19b108.py
│   │   ├── README.md
│   │   ├── SAT.pdf
│   │   └── SAT_examples.ipynb
│   │
│   ├── assignment_5/
│   │   ├── ee19b108.py
│   │   ├── EE5333_Assgn5.pdf
│   │   ├── README.md
│   │   └── Untitled14.ipynb
│   │
│   └── assignment_6/
│       ├── Assignment_6.pdf
│       ├── EE19B108.py
│       └── README.md
│
└── project/
    ├── README.md
    ├── data/
    │   ├── def/
    │   │   ├── add5.def
    │   │   ├── c17.def
    │   │   ├── c432.def
    │   │   ├── c499.def
    │   │   ├── c6288.def
    │   │   ├── c7552.def
    │   │   └── spm.def
    │   ├── gr/
    │   │   ├── add5.guide
    │   │   ├── c17.guide
    │   │   ├── c432.guide
    │   │   ├── c499.guide
    │   │   ├── c6288.guide
    │   │   ├── c7552.guide
    │   │   └── spm.guide
    │   └── lef/
    │       └── sky130.lef
    │
    ├── docs/
    │   └── EE5333_endsem_project.pdf
    │
    ├── output/
    │   ├── add5_out.def
    │   ├── c17_out.def
    │   ├── c7552_out.def
    │   ├── lefdefparser-0.1-cp312-cp312-win_amd64.whl
    │   └── LEFDEFParser.pyd
    │
    ├── scr/
    │   ├── checker.py
    │   ├── detailed_router.py
    │   └── writeSol.py
    │
    ├── tempwheel/
    │   ├── lefdefparser-0.1.dist-info/
    │   │   ├── licenses/
    │   │   │   └── LICENSE
    │   │   ├── METADATA
    │   │   ├── RECORD
    │   │   ├── top_level.txt
    │   │   └── WHEEL
    │   ├── Release/
    │   │   ├── LEFDEFParser.cp312-win_amd64.pyd
    │   │   ├── LEFDEFParser.exp
    │   │   └── LEFDEFParser.lib
    │   ├── lefdefparser-0.1-cp312-cp312-win_amd64.whl
    │   └── LEFDEFParser.cp312-win_amd64.pyd
    │
    ├── lefdefparser-0.1-cp312-cp312-win_amd64.whl
    └── LEFDEFParser.cp312-win_amd64.pyd
```

> The tree above reflects the supplied repository. Generated/binary files that are actually committed are shown rather than silently omitted.

---

# Coursework

## Assignment 1 — ILP-based graph optimization

Assignment 1 formulates graph problems as Integer Linear Programs using the `mip` optimization library.

The submitted implementation in `ee19b108.py` provides:

- **Minimum Dominating Set (MDS)**
- **Minimum-weighted Independent Set (MWIS)**

The additional `assignment_1.py` file also contains a `colorGraph` function for graph colouring.

### Main concepts

- binary decision variables
- ILP formulation
- graph constraints
- optimization objectives
- MIP solver usage

---

## Assignment 2 — Fiduccia–Mattheyses partitioning

Assignment 2 implements the **Fiduccia–Mattheyses (FM)** algorithm for bi-partitioning a hypergraph.

The implementation:

1. creates an initial feasible partition,
2. calculates vertex gains,
3. selects legal moves,
4. locks moved vertices,
5. records intermediate partition costs,
6. retains the best partition,
7. rolls back moves after the best point,
8. repeats passes while improvement is possible.

The main function is:

```python
partitionFM(V, E, Amin, Amax)
```

---

## Assignment 3 — Floorplanning using sequence pairs

Assignment 3 implements sequence-pair based floorplanning with **simulated annealing**.

The implementation uses:

- positive and negative sequences,
- module aspect-ratio choices,
- horizontal constraint graphs,
- vertical constraint graphs,
- longest-path calculations,
- simulated-annealing perturbations.

The documented perturbations include:

- swapping two modules in the positive sequence,
- swapping two modules in both sequences,
- changing a module's aspect ratio.

The supplied files include the implementation, a floorplanning notebook, a PDF, and assignment documentation.

---

## Assignment 4 — DPLL SAT solver

Assignment 4 implements the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm for SAT problems represented in DIMACS CNF format.

The implementation includes:

- clause evaluation,
- unit-clause detection and propagation,
- pure-literal handling,
- conflict detection,
- branching,
- recursive search,
- DIMACS CNF loading.

The repository also contains six CNF example files:

```text
1.cnf
uf20-01.cnf
uf20-02.cnf
uf20-03.cnf
uf20-04.cnf
uf20-05.cnf
```

---

## Assignment 5 — Graph Isomorphism

Assignment 5 implements graph isomorphism for **undirected simple graphs with vertex attributes**.

The main function is:

```python
is_isomorphic(G, H)
```

The implementation first performs basic compatibility checks, including:

- number of vertices,
- number of edges,
- vertex-attribute multisets.

It then searches vertex permutations and verifies that the required edge mapping is preserved.

---

## Assignment 6 — Branch and Bound for ILP

Assignment 6 implements **Branch and Bound for Integer Linear Programming** using a simplex routine for the LP relaxation.

The implementation includes:

- integer-solution checking,
- LP relaxation,
- branching on fractional variables,
- recursive subproblem generation,
- bound-based pruning,
- best-solution tracking.

The integer check applies to the original decision variables; slack variables introduced by the LP formulation are not required to be integral.

---

# End-Semester Project — Detailed Routing

The main project is a **detailed router for standard-cell designs** using LEF, DEF, and routing-guide data.

The project directory is organized as:

```text
project/
├── data/
├── docs/
├── output/
├── scr/
├── tempwheel/
├── LEFDEFParser...
└── README.md
```

## Input data

### DEF benchmarks

Seven DEF benchmark designs are supplied:

- `add5.def`
- `c17.def`
- `c432.def`
- `c499.def`
- `c6288.def`
- `c7552.def`
- `spm.def`

### Routing guides

Seven corresponding routing-guide files are supplied:

- `add5.guide`
- `c17.guide`
- `c432.guide`
- `c499.guide`
- `c6288.guide`
- `c7552.guide`
- `spm.guide`

### Technology data

The project uses:

```text
sky130.lef
```

---

## Router implementation

The actual project source directory is:

```text
project/scr/
```

It contains:

### `detailed_router.py`

The main detailed-routing implementation.

Its documented functionality includes reading DEF/LEF/GUIDE information, routing design nets, and generating routed DEF output.

The implementation contains routing logic involving:

- routing-guide parsing,
- layer preference and geometry handling,
- occupancy tracking,
- obstruction handling,
- pin access,
- candidate scoring,
- minimum-spanning-tree based routing,
- guide-aware path selection,
- DRC-aware routing.

### `checker.py`

Checks routed designs for:

- spacing violations,
- connectivity/open nets.

The checker uses the `LEFDEFParser` package and contains technology/layer information for the supplied SkyWater 130 nm LEF data.

### `writeSol.py`

A small solution-generation/example script that reads a DEF file, adds selected routing rectangles to specified nets, and writes a new DEF file.

---

# Project data flow

The intended project flow is:

```text
LEF + DEF + GUIDE
       │
       ▼
detailed_router.py
       │
       ▼
routed DEF
       │
       ▼
checker.py
       ├── spacing DRC check
       └── connectivity check
```

The repository contains selected generated DEF outputs:

```text
output/
├── add5_out.def
├── c17_out.def
└── c7552_out.def
```

The presence of three generated DEF outputs does **not** imply that outputs for all seven benchmarks are committed.

---

# Parser dependency

The project contains a Windows CPython 3.12 wheel and compiled extension for `LEFDEFParser`:

```text
lefdefparser-0.1-cp312-cp312-win_amd64.whl
LEFDEFParser.cp312-win_amd64.pyd
```

A copy of the wheel and related unpacked package/build files is also present under `project/tempwheel/`.

The project README specifies installation through the supplied wheel and notes that `rtree` is required by the checker.

---

# Running the project

The **actual source directory is `scr/`**, so commands should reference `scr/`, not `src/`.

From the `project/` directory, the project README gives the following intended router invocation pattern:

```bash
python scr/detailed_router.py \
    --lef data/lef/sky130.lef \
    --def data/def/add5.def \
    --guide data/gr/add5.guide \
    --output output/add5_out.def
```

The checker can then be invoked as:

```bash
python scr/checker.py \
    --lef data/lef/sky130.lef \
    --def output/add5_out.def \
    --guide data/gr/add5.guide
```

The checker reports the number of open/disconnected nets and spacing violations.

The supplied project README also describes an optional placement visualizer using the `-p` option.

> The original project README contains older command examples referring to `src/`. Those paths do not match the supplied repository, whose implementation directory is `scr/`.

---

# Tools and concepts demonstrated

- Python
- Integer Linear Programming
- Mixed-Integer Programming
- Graph algorithms
- Hypergraph partitioning
- Fiduccia–Mattheyses algorithm
- Sequence-pair floorplanning
- Simulated annealing
- SAT / DPLL
- Graph isomorphism
- Branch and Bound
- Simplex / LP relaxation
- VLSI physical design
- LEF/DEF
- Routing guides
- Detailed routing
- Connectivity checking
- Spacing DRC

---
