# EE5333 — Introduction to Physical Design Automation

Coursework and End-Semester Project repository for **EE5333 — Introduction to Physical Design Automation, IIT Madras**.

This repository contains six course assignments covering major algorithmic techniques used in VLSI physical design automation, together with an End-Semester detailed-routing project.

## Repository Contents

```text
.
├── README.md
├── REPORT.md
├── assignments/
│   ├── assignment_1/
│   ├── assignment_2/
│   ├── assignment_3/
│   ├── assignment_4/
│   ├── assignment_5/
│   └── assignment_6/
└── project/
    ├── README.md
    ├── REPORT.md
    ├── data/
    ├── docs/
    ├── output/
    ├── scr/
    └── ...
```

The root `README.md` provides a high-level overview of the complete repository. The root `REPORT.md` provides the consolidated technical report, including the six assignments and the final End-Semester project evaluation.

---

# Assignments

## Assignment 1 — ILP-Based Graph Optimization

Assignment 1 formulates graph optimization problems as Integer Linear Programs using the `mip` library.

The submitted implementation includes:

- **Minimum Dominating Set (MDS)**
- **Minimum-Weighted Independent Set (MWIS)**

The repository also contains an `assignment_1.py` implementation with a graph-colouring formulation.

### Main concepts

- binary decision variables
- ILP objective functions
- graph constraints
- MIP solver usage
- combinatorial optimization

---

## Assignment 2 — Fiduccia–Mattheyses Hypergraph Partitioning

Assignment 2 implements the **Fiduccia–Mattheyses (FM) algorithm** for two-way hypergraph partitioning.

The implementation performs:

1. initial feasible partitioning,
2. gain calculation,
3. legal vertex selection,
4. vertex locking,
5. move-cost tracking,
6. best-prefix selection,
7. rollback to the best partition,
8. repeated improvement passes.

Main function:

```python
partitionFM(V, E, Amin, Amax)
```

### Main concepts

- hypergraph partitioning
- cutsize minimization
- gain computation
- area-balance constraints
- greedy local improvement

---

## Assignment 3 — Sequence-Pair Floorplanning

Assignment 3 implements **sequence-pair based floorplanning with simulated annealing**.

The implementation uses:

- positive and negative module sequences,
- horizontal and vertical constraint graphs,
- longest-path calculations,
- module aspect-ratio choices,
- simulated-annealing perturbations.

Perturbations include:

- swapping two modules in one sequence,
- swapping two modules in both sequences,
- changing a module's aspect ratio.

### Main concepts

- sequence pairs
- constraint graphs
- longest-path computation
- floorplan coordinates
- simulated annealing

---

## Assignment 4 — DPLL SAT Solver

Assignment 4 implements the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm for SAT problems represented in DIMACS CNF format.

The implementation includes:

- clause evaluation,
- unit propagation,
- pure-literal handling,
- conflict detection,
- branching,
- recursive search,
- DIMACS CNF parsing.

Example CNF inputs are included in the assignment directory.

### Main concepts

- Boolean satisfiability
- CNF representation
- unit propagation
- pure-literal elimination
- recursive backtracking

---

## Assignment 5 — Graph Isomorphism

Assignment 5 implements graph isomorphism for **undirected simple graphs with vertex attributes**.

The main function is:

```python
is_isomorphic(G, H)
```

The implementation performs compatibility checks before searching for a valid vertex mapping, including:

- vertex-count comparison,
- edge-count comparison,
- vertex-attribute compatibility.

It then verifies whether a candidate mapping preserves the required graph structure.

### Main concepts

- graph isomorphism
- vertex attributes
- graph invariants
- permutation-based search

---

## Assignment 6 — Branch and Bound for ILP

Assignment 6 implements **Branch and Bound for Integer Linear Programming**, using an LP/simplex routine to solve the relaxations.

The implementation:

1. solves the LP relaxation,
2. checks integrality of the decision variables,
3. updates the incumbent solution,
4. selects a fractional variable,
5. creates branching subproblems,
6. recursively solves the subproblems,
7. prunes subproblems using their bounds.

### Main concepts

- LP relaxation
- integer feasibility
- branching
- bounding
- pruning
- recursive optimization

---

# End-Semester Project — Detailed Routing

The End-Semester project implements a **detailed router for standard-cell physical designs**.

The project works with:

- **LEF** technology data,
- **DEF** placed-design data,
- **GUIDE** routing regions.

The router generates routed DEF files, which are then checked for:

- connectivity/open nets,
- spacing violations.

## Project Inputs

Seven benchmark designs were evaluated:

```text
add5
c17
c432
c499
c6288
c7552
spm
```

Each benchmark has a corresponding DEF and GUIDE file, and the project uses the supplied:

```text
sky130.lef
```

technology LEF.

## Project Source

The implementation is located under:

```text
project/scr/
```

Important files include:

- `detailed_router.py` — detailed-routing implementation
- `checker.py` — spacing and connectivity checker
- `writeSol.py` — DEF solution-writing utility

## Project Flow

```text
LEF + DEF + GUIDE
        |
        v
detailed_router.py
        |
        v
Generated routed DEF
        |
        v
checker.py
        |
        +----> Connectivity / open-net check
        |
        +----> Spacing DRC check
```

## Project Setup

Project-specific installation and execution instructions are maintained in:

```text
project/README.md
```

The project uses a course-provided `LEFDEFParser` package and `rtree`. The parser is supplied as a Windows CPython 3.12 wheel in the project repository.

For the exact installation commands and benchmark execution commands, follow `project/README.md`.

## Project Results

The final implementation was evaluated on all seven supplied benchmarks.

| Benchmark | Guide Nets | Routed Nets | Open Nets | Routing Time (s) | Spacing Violations |
|---|---:|---:|---:|---:|---:|
| add5 | 61 | 60 | 0 | 0.29 | 52 |
| c17 | 23 | 22 | 0 | 0.22 | 20 |
| c432 | 198 | 197 | 0 | 0.63 | 291 |
| c499 | 363 | 362 | 0 | 1.48 | 564 |
| c6288 | 1526 | 1525 | 0 | 4.08 | 3236 |
| c7552 | 1592 | 1591 | 0 | 11.77 | 3991 |
| spm | 308 | 307 | 0 | 1.09 | 873 |

The most important connectivity result is:

```text
Open nets = 0
```

for every evaluated benchmark.

The checker still reports spacing violations, so the final implementation should **not** be described as completely DRC-clean. The results demonstrate successful connectivity routing, while spacing enforcement and congestion handling remain areas for improvement.

A detailed discussion is provided in:

```text
REPORT.md
project/REPORT.md
```

---

# Skills and Topics Covered

The complete repository demonstrates work across:

### Optimization

- Integer Linear Programming
- Mixed-Integer Programming
- LP relaxation
- Branch and Bound
- simulated annealing

### Graph Algorithms

- graph optimization
- graph colouring
- hypergraph partitioning
- graph isomorphism

### Algorithms and AI

- DPLL SAT solving
- recursive search
- heuristic optimization

### VLSI Physical Design

- partitioning
- floorplanning
- detailed routing
- LEF/DEF data
- routing guides
- design-rule checking
- connectivity verification

### Software Development

- Python
- algorithm implementation
- Jupyter notebooks
- solver integration
- physical-design data processing
- experimental benchmarking

---

# Documentation

| Document | Purpose |
|---|---|
| `README.md` | Overview and navigation for the complete repository |
| `REPORT.md` | Consolidated coursework and project technical report |
| `assignments/assignment_*/README.md` | Assignment-specific instructions and descriptions |
| `project/README.md` | Detailed project setup and execution instructions |
| `project/REPORT.md` | Detailed project implementation and experimental report |

