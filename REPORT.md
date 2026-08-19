# EE5333 — Introduction to Physical Design Automation
## Coursework and End-Semester Project Report

## 1. Overview

This repository contains selected coursework and the end-semester project for **EE5333 — Introduction to Physical Design Automation at IIT Madras**.

The coursework covers several algorithmic problems that appear in VLSI physical design and combinatorial optimization:

1. ILP-based graph optimization
2. Fiduccia–Mattheyses hypergraph partitioning
3. Sequence-pair floorplanning
4. DPLL SAT solving
5. Graph isomorphism
6. Branch and Bound for ILP

The end-semester project implements a **detailed routing workflow** using LEF, DEF, and routing-guide data.

---

# 2. Assignment 1 — ILP Graph Optimization

Assignment 1 formulates graph problems as Integer Linear Programs using the `mip` library.

The primary submitted implementation provides:

- Minimum Dominating Set (MDS)
- Minimum-weighted Independent Set (MWIS)

The repository also contains `assignment_1.py`, which includes an additional `colorGraph` graph-colouring formulation.

### MDS

The Minimum Dominating Set formulation minimizes the number of selected vertices subject to every vertex either being selected or having a selected neighbor.

### MWIS

The Minimum-weighted Independent Set implementation selects an independent set according to vertex weights while enforcing adjacency constraints.

### Files

```text
assignment_1/
├── assignment1_statement.txt
├── assignment_1.py
├── ee19b108.py
├── Introduction (1).ipynb
└── README.md
```

---

# 3. Assignment 2 — Fiduccia–Mattheyses Partitioning

Assignment 2 implements the **Fiduccia–Mattheyses algorithm** for bi-partitioning a hypergraph.

The objective is to satisfy area constraints while reducing the number of cut hyperedges.

The implementation uses the function:

```python
partitionFM(V, E, Amin, Amax)
```

The implementation follows the FM workflow:

```text
Initial feasible partition
        ↓
Calculate gains
        ↓
Choose legal highest-gain move
        ↓
Lock vertex
        ↓
Continue moves
        ↓
Find best intermediate partition
        ↓
Rollback after best point
        ↓
Repeat pass if improvement exists
```

### Files

```text
assignment_2/
├── assignement_2_statement.txt
├── ee19b108.py
├── FM_Partition.ipynb
└── README.md
```

---

# 4. Assignment 3 — Sequence-Pair Floorplanning

Assignment 3 implements floorplanning using **sequence pairs and simulated annealing**.

The implementation represents a floorplan using positive and negative module sequences. The sequence pair is transformed into horizontal and vertical constraint relationships, and longest-path calculations determine module coordinates.

The optimization searches over:

- sequence-pair permutations,
- module aspect-ratio choices.

The perturbation operations include:

- swapping two modules in the positive sequence,
- swapping two modules in both sequences,
- changing a module's aspect ratio.

The objective is to minimize the area of the enclosing floorplan.

### Files

```text
assignment_3/
├── ee19b108.py
├── EE5333_assgn3.pdf
├── Floorplanning.ipynb
└── README.md
```

---

# 5. Assignment 4 — DPLL SAT Solver

Assignment 4 implements a **Davis–Putnam–Logemann–Loveland (DPLL)** SAT solver for CNF formulas in DIMACS format.

The implementation includes:

- clause evaluation,
- unit propagation,
- pure-literal elimination,
- conflict detection,
- branching,
- recursive search,
- DIMACS CNF file loading.

The solver therefore demonstrates the basic recursive structure of a classical complete SAT-solving algorithm.

### Example inputs

Six CNF files are included:

```text
CNF_Examples/
├── 1.cnf
├── uf20-01.cnf
├── uf20-02.cnf
├── uf20-03.cnf
├── uf20-04.cnf
└── uf20-05.cnf
```

### Files

```text
assignment_4/
├── CNF_Examples/
├── ee19b108.py
├── README.md
├── SAT.pdf
└── SAT_examples.ipynb
```

---

# 6. Assignment 5 — Graph Isomorphism

Assignment 5 implements graph isomorphism for **undirected simple graphs with vertex attributes**.

The primary function is:

```python
is_isomorphic(G, H)
```

The implementation first rejects graphs that differ in:

- number of vertices,
- number of edges,
- vertex-attribute multiset.

For compatible graphs, it searches vertex mappings and verifies preservation of the undirected edge relationships.

### Files

```text
assignment_5/
├── ee19b108.py
├── EE5333_Assgn5.pdf
├── README.md
└── Untitled14.ipynb
```

---

# 7. Assignment 6 — Branch and Bound for ILP

Assignment 6 implements **Branch and Bound for Integer Linear Programming** using the provided simplex routine for solving LP relaxations.

The implementation:

1. solves the LP relaxation,
2. checks whether the decision-variable solution is integral,
3. updates the incumbent when an improved integer solution is found,
4. selects a fractional variable,
5. creates lower/upper branching subproblems,
6. recursively solves the subproblems,
7. prunes branches whose LP bound cannot improve the incumbent.

The integer check is applied to the original decision variables; simplex slack variables do not need to satisfy the integer restriction.

### Files

```text
assignment_6/
├── Assignment_6.pdf
├── EE19B108.py
└── README.md
```

---

# 8. End-Semester Project — Detailed Routing

## 8.1 Objective

The project implements a **detailed routing algorithm for standard-cell designs**.

The supplied router reads:

- LEF technology/design information,
- DEF design data,
- routing-guide data,

and generates routed DEF output.

The repository also contains a checker for:

- spacing DRC,
- connectivity/open nets.

---

# 9. Project Organization

```text
project/
├── data/
├── docs/
├── output/
├── scr/
├── tempwheel/
├── lefdefparser-0.1-cp312-cp312-win_amd64.whl
├── LEFDEFParser.cp312-win_amd64.pyd
└── README.md
```

## Input benchmark set

The project contains seven DEF benchmarks:

```text
add5
c17
c432
c499
c6288
c7552
spm
```

Each has a corresponding routing guide.

The project uses the supplied:

```text
data/lef/sky130.lef
```

technology LEF file.

---

# 10. Router Implementation

The actual source directory is:

```text
project/scr/
```

### `detailed_router.py`

This is the main routing implementation.

The file contains functionality for:

- parsing routing guides,
- representing routing geometry,
- handling layer preferences,
- maintaining occupancy,
- handling obstructions,
- generating pin-access structures,
- selecting routing candidates,
- guide-aware routing,
- DRC-aware routing,
- constructing routes between terminals.

The implementation also contains a minimum-spanning-tree based routing stage.

### `checker.py`

The checker loads the LEF/DEF design and verifies routed geometry.

Its documented checks include:

- spacing violations,
- connectivity/open nets.

It also contains layer orientation, spacing, width, and adjacency information for the routing layers used by the design.

### `writeSol.py`

This is a small solution-generation script that demonstrates writing routing rectangles into a DEF design and producing a new DEF file.

---

# 11. Routing Flow

The project can be viewed as:

```text
Sky130 LEF
     │
     ├──────────────┐
     │              │
     ▼              ▼
  DEF design    Routing guide
     │              │
     └───────┬──────┘
             ▼
     detailed_router.py
             │
             ▼
       Routed DEF file
             │
             ▼
         checker.py
          /       \
         ▼         ▼
 Connectivity   Spacing DRC
```

This separates route generation from post-routing validation.

---

# 12. Generated Outputs

The repository contains three selected routed DEF outputs:

```text
project/output/
├── add5_out.def
├── c17_out.def
└── c7552_out.def
```

The seven input benchmarks and seven routing guides should not be confused with the three generated DEF files currently committed.

---

# 13. LEF/DEF Parser Dependency

The project includes a Windows CPython 3.12 wheel and compiled parser extension:

```text
lefdefparser-0.1-cp312-cp312-win_amd64.whl
LEFDEFParser.cp312-win_amd64.pyd
```

The `tempwheel/` directory contains an unpacked copy of related wheel metadata and compiled package artifacts.

The supplied project README specifies installation of the parser wheel and notes that `rtree` is required by the checker.

---

# 14. Project Documentation

The project documentation includes:

```text
project/docs/
└── EE5333_endsem_project.pdf
```

The project-specific README also contains usage instructions for generating a routed DEF file and running the checker.

One important repository correction is that the supplied project source directory is:

```text
scr/
```

not:

```text
src/
```

Therefore, commands using `src/detailed_router.py` or `src/checker.py` in the older README should be interpreted as outdated path references; the actual files are under `project/scr/`.

---

# 15. Technical Skills Demonstrated

## Optimization

- Integer Linear Programming
- Mixed-Integer Programming
- LP relaxation
- Branch and Bound
- simulated annealing

## Algorithms

- graph optimization
- graph colouring
- hypergraph partitioning
- sequence-pair floorplanning
- DPLL SAT solving
- graph isomorphism
- detailed routing

## VLSI Physical Design

- partitioning
- floorplanning
- placement-related algorithmic concepts
- routing
- LEF/DEF interchange formats
- routing guides
- DRC checking
- connectivity checking

## Software

- Python
- Jupyter notebooks
- MIP solver integration
- custom physical-design data parsing
- algorithm implementation and testing

---

