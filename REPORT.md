# EE5333 — Introduction to Physical Design Automation
## Consolidated Coursework and End-Semester Project Report

## 1. Overview

This repository contains coursework and the End-Semester project for **EE5333 — Introduction to Physical Design Automation at IIT Madras**.

The coursework covers six algorithmic problems related to optimization, graph algorithms, satisfiability, and physical design:

1. ILP-based graph optimization
2. Fiduccia–Mattheyses hypergraph partitioning
3. Sequence-pair floorplanning
4. DPLL SAT solving
5. Graph isomorphism
6. Branch and Bound for ILP

The End-Semester project extends the physical-design focus to **detailed routing**, using LEF, DEF, and routing-guide data.

This report consolidates the purpose, implementation approach, and observations for the assignments and the final routing project.

---

# 2. Assignment 1 — ILP-Based Graph Optimization

## 2.1 Objective

The first assignment formulates graph optimization problems as Integer Linear Programs.

The submitted implementation primarily addresses:

- Minimum Dominating Set (MDS)
- Minimum-Weighted Independent Set (MWIS)

The repository also contains an additional graph-colouring formulation.

## 2.2 Minimum Dominating Set

For a graph G=(V,E), a dominating set contains vertices such that every vertex is either selected or adjacent to a selected vertex.

The implementation uses binary decision variables to represent whether each vertex is selected and minimizes the number of selected vertices subject to the domination constraints.

## 2.3 Minimum-Weighted Independent Set

The independent-set formulation selects vertices while ensuring that adjacent vertices are not simultaneously selected.

The objective incorporates the supplied vertex weights.

## 2.4 Observations

The assignment demonstrates how graph problems can be expressed using:

- binary variables,
- linear constraints,
- objective functions,
- a MIP solver.

The important conceptual step is translating combinatorial conditions into algebraic constraints that can be handled by an optimization solver.

---

# 3. Assignment 2 — Fiduccia–Mattheyses Partitioning

## 3.1 Objective

Assignment 2 implements the **Fiduccia–Mattheyses (FM) algorithm** for two-way hypergraph partitioning.

The objective is to minimize the cut cost while maintaining the specified partition-size constraints.

## 3.2 Algorithm

The implementation follows the standard FM improvement process:

```text
Initial feasible partition
        |
        v
Calculate gains
        |
        v
Select legal move
        |
        v
Lock moved vertex
        |
        v
Continue until no legal moves
        |
        v
Find best prefix
        |
        v
Rollback moves after best point
        |
        v
Start another pass if useful
```

The main implementation entry point is:

```python
partitionFM(V, E, Amin, Amax)
```

## 3.3 Observations

The assignment demonstrates the difference between a locally greedy move sequence and the best partition encountered during that sequence. Recording the intermediate costs and rolling back after the best prefix is therefore an important part of the FM algorithm.

---

# 4. Assignment 3 — Sequence-Pair Floorplanning

## 4.1 Objective

Assignment 3 implements sequence-pair based floorplanning combined with simulated annealing.

A sequence pair represents relative ordering between modules. The positive and negative sequences are converted into horizontal and vertical precedence relationships.

## 4.2 Implementation

The implementation constructs:

- horizontal constraint relationships,
- vertical constraint relationships.

Longest-path calculations are then used to determine module coordinates and the resulting floorplan dimensions.

The optimization process explores:

- sequence permutations,
- module aspect-ratio choices.

The documented perturbations include:

1. swapping two modules in the positive sequence,
2. swapping two modules in both sequences,
3. changing a module's aspect ratio.

## 4.3 Observations

The assignment demonstrates how a discrete representation such as a sequence pair can be combined with simulated annealing to search a large floorplanning space.

The constraint-graph representation separates the combinatorial ordering problem from coordinate computation.

---

# 5. Assignment 4 — DPLL SAT Solver

## 5.1 Objective

Assignment 4 implements the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm for Boolean satisfiability.

The input is represented in DIMACS CNF format.

## 5.2 Implementation

The solver includes the main components of DPLL:

- clause evaluation,
- unit-clause propagation,
- pure-literal handling,
- conflict detection,
- variable branching,
- recursive search.

The repository contains example CNF instances for testing.

## 5.3 Observations

DPLL demonstrates how logical simplification can reduce the search space before branching.

Unit propagation and pure-literal processing can eliminate variables and clauses without requiring a full search. Branching is then used when deterministic simplification cannot decide the formula.

---

# 6. Assignment 5 — Graph Isomorphism

## 6.1 Objective

Assignment 5 determines whether two undirected simple graphs with vertex attributes are isomorphic.

The main function is:

```python
is_isomorphic(G, H)
```

## 6.2 Implementation

The implementation first checks inexpensive graph invariants, including:

- number of vertices,
- number of edges,
- vertex-attribute compatibility.

For compatible graphs, it searches for a vertex mapping and verifies that the mapping preserves the graph's edge relationships.

## 6.3 Observations

The initial invariant checks are important because they reject many non-isomorphic graph pairs before the more expensive mapping search.

The assignment illustrates the difference between necessary conditions for isomorphism and a complete verification of a candidate mapping.

---

# 7. Assignment 6 — Branch and Bound for ILP

## 7.1 Objective

Assignment 6 implements Branch and Bound for Integer Linear Programming.

The LP relaxation is solved using the simplex routine, and fractional solutions are recursively partitioned into integer-constrained subproblems.

## 7.2 Algorithm

The main process is:

```text
Solve LP relaxation
        |
        v
Is solution integral?
   /             yes             no
 |                |
Update          Select fractional
incumbent       variable
                  |
             +----+----+
             |         |
             v         v
        Branch 1    Branch 2
             |         |
             +----+----+
                  |
                  v
             Bound / prune
```

A branch is pruned when its relaxation cannot improve the current best integer solution.

## 7.3 Observations

The assignment demonstrates why LP relaxations are useful for integer optimization: they provide both candidate solutions and bounds that can be used to eliminate parts of the search tree.

---

# 8. End-Semester Project — Detailed Routing

## 8.1 Objective

The End-Semester project implements a detailed routing workflow for standard-cell physical designs.

The router takes:

- LEF technology information,
- a placed DEF design,
- routing GUIDE information,

and produces a routed DEF file.

The resulting design is then evaluated using a checker for:

- connectivity,
- spacing-rule violations.

---

# 9. Project Inputs

The final evaluation uses seven benchmark designs:

```text
add5
c17
c432
c499
c6288
c7552
spm
```

Each benchmark has a corresponding:

```text
DEF
GUIDE
```

file.

The technology information is provided by:

```text
sky130.lef
```

---

# 10. Router Architecture

The main implementation is in:

```text
project/scr/detailed_router.py
```

The implementation includes the following major components.

## 10.1 GUIDE parsing

Routing-guide files are parsed into guide regions associated with individual nets.

These regions constrain where the router should search for routes.

## 10.2 Track-grid construction

The router derives routing-track information from the DEF track definitions and maps tracks to preferred routing directions.

The supplied layer configuration uses alternating routing directions across the routing stack.

## 10.3 Pin-shape extraction

Cell and boundary pin geometry is extracted from the LEF/DEF information.

This geometry is used to construct routing access points.

## 10.4 Obstruction handling

Cell obstructions and existing geometry are represented so that candidate routes can avoid blocked regions.

## 10.5 Occupancy tracking

The router maintains an occupancy representation of committed wire segments.

The implementation includes explicit spacing-aware checks rather than relying only on geometric center distances.

## 10.6 Route construction

The router creates access points and connects them using a routing strategy based on a minimum spanning tree for multi-terminal nets.

Candidate routing segments are evaluated using geometric and guide-related criteria.

## 10.7 DEF generation

After routing, the resulting wire rectangles are added to the DEF representation and written to an output DEF file.

---

# 11. Important Implementation Fixes

The final router contains several fixes made during development.

The implementation documents fixes including:

### Occupancy overlap

The original interval-overlap logic could incorrectly accept conflicting segments. It was replaced with an explicit running-axis overlap test.

### Edge-to-edge spacing

The occupancy test was changed from an overly aggressive center-distance condition to an edge-to-edge spacing interpretation.

### Pin-access trimming

Pin-access stubs are trimmed against obstructions without subsequently restoring unsafe geometry.

### Obstruction-boundary handling

Near-boundary obstructions are handled when trimming access ranges.

### Layer-specific stub handling

Access stubs on multiple layers are routed through obstruction-aware trimming.

### Guide-aware candidate ordering

Candidate ordering was adjusted so that DRC-safe candidates and guide preference influence selection in the intended order.

### Correct occupancy-axis registration

Vertical and horizontal layers use the appropriate fixed coordinate and running extent when registering geometry.

### LEF spacing

Layer spacing values are updated from the LEF data rather than relying only on default constants.

### Routed wires as obstacles

Committed routed wires are added to the obstruction representation so subsequent nets can treat them as hard obstacles.

### Pre-existing wires

Existing wires in the input DEF are considered during routing rather than being treated as empty routing space.

These changes were aimed primarily at improving geometric correctness and preventing newly routed nets from conflicting with existing or previously committed geometry.

---

# 12. Routing and Checking Flow

The complete project flow is:

```text
LEF
 │
 ├──────────────┐
 │              │
DEF           GUIDE
 │              │
 └──────┬───────┘
        ▼
 detailed_router.py
        │
        ▼
  Routed DEF
        │
        ▼
    checker.py
     /           ▼         ▼
Open nets   Spacing violations
```

The project README contains the exact installation and execution commands.

---

# 13. Experimental Method

Each of the seven supplied benchmarks was routed using the final implementation.

For each benchmark, the measured quantities were:

- number of nets in the GUIDE,
- number of nets routed by the implementation,
- routing runtime,
- number of open nets reported by the checker,
- number of spacing violations reported by the checker.

The routing command writes a benchmark-specific output DEF. The checker is then run on the generated output.

---

# 14. Final Experimental Results

| Benchmark | Guide Nets | Routed Nets | Open Nets | Routing Time (s) | Spacing Violations |
|---|---:|---:|---:|---:|---:|
| add5 | 61 | 60 | 0 | 0.29 | 52 |
| c17 | 23 | 22 | 0 | 0.22 | 20 |
| c432 | 198 | 197 | 0 | 0.63 | 291 |
| c499 | 363 | 362 | 0 | 1.48 | 564 |
| c6288 | 1526 | 1525 | 0 | 4.08 | 3236 |
| c7552 | 1592 | 1591 | 0 | 11.77 | 3991 |
| spm | 308 | 307 | 0 | 1.09 | 873 |

---

# 15. Connectivity Results

The most consistent result across all seven benchmarks is:

```text
Open nets = 0
```

This means the checker found no disconnected nets in the generated routed outputs.

The routed-net count is one less than the number of GUIDE nets for every benchmark in the recorded output. This is consistent across the entire benchmark set.

Therefore, the strongest demonstrated property of the final implementation is **successful connectivity routing across all evaluated benchmarks**.

---

# 16. Runtime Results

The measured routing times were:

| Benchmark | Routing Time |
|---|---:|
| c17 | 0.22 s |
| add5 | 0.29 s |
| c432 | 0.63 s |
| spm | 1.09 s |
| c499 | 1.48 s |
| c6288 | 4.08 s |
| c7552 | 11.77 s |

The smallest measured runtime was:

```text
c17 = 0.22 s
```

The largest was:

```text
c7552 = 11.77 s
```

The larger benchmarks generally require more routing time. This is expected because they contain substantially more routed nets and more complex geometric interactions.

The relationship is not purely a function of net count, however. Physical layout geometry, routing-guide regions, obstructions, and congestion also influence runtime.

---

# 17. Spacing-DRC Results

The checker reported spacing violations for every evaluated benchmark.

| Benchmark | Spacing Violations |
|---|---:|
| c17 | 20 |
| add5 | 52 |
| c432 | 291 |
| c499 | 564 |
| spm | 873 |
| c6288 | 3236 |
| c7552 | 3991 |

The reported violations include both:

- net-to-net conflicts,
- net-to-obstruction conflicts.

The violation count grows substantially for the larger designs.

For example:

```text
c17   : 20
c499  : 564
c6288 : 3236
c7552 : 3991
```

This indicates that geometric congestion becomes a significant challenge as the design size increases.

---

# 18. Important Interpretation of the Results

The results should be interpreted carefully.

The final router demonstrates:

- successful routing connectivity,
- zero open nets on all seven evaluated benchmarks,
- practical runtime on the supplied benchmark suite.

However, the checker still reports spacing violations.

Therefore, the project should **not** be described as achieving complete DRC-clean routing.

A more accurate characterization is:

> The implementation successfully establishes connectivity for all evaluated benchmarks, while spacing-rule violations remain and represent the primary area for further routing improvement.

This distinction is important because zero open nets and zero DRC violations measure different properties.

---

# 19. Congestion and Scaling Observations

The benchmark results show a clear increase in spacing conflicts for the larger designs.

For example:

- `c17` routes 22 nets and reports 20 spacing violations.
- `c499` routes 362 nets and reports 564 spacing violations.
- `c6288` routes 1525 nets and reports 3236 spacing violations.
- `c7552` routes 1591 nets and reports 3991 spacing violations.

The increase is not perfectly linear because routing difficulty depends on the physical distribution of cells, obstacles, guide regions, and existing wires.

The results nevertheless indicate that congestion-aware route selection becomes increasingly important for larger designs.

---

# 20. Project Limitations

The current implementation has several demonstrated limitations.

## 20.1 Remaining spacing violations

All evaluated benchmarks contain spacing violations.

Further improvements are required in:

- route candidate selection,
- congestion handling,
- interaction between existing and newly routed wires,
- geometric spacing enforcement.

## 20.2 Benchmark dependence

The reported performance is based on the supplied benchmark set and technology LEF. Performance and DRC behavior may differ on other designs or technology libraries.

## 20.3 Platform-specific parser dependency

The supplied `LEFDEFParser` dependency is distributed as a Windows CPython 3.12 wheel. The current documented setup therefore targets that environment.

---

# 21. Overall Conclusions

The coursework demonstrates a progression from individual optimization and algorithmic techniques toward a complete physical-design application.

The assignments cover:

```text
ILP
  ↓
Hypergraph Partitioning
  ↓
Floorplanning
  ↓
SAT
  ↓
Graph Isomorphism
  ↓
Branch and Bound
  ↓
Detailed Routing
```

The End-Semester project applies several of these ideas in a physical-design setting where geometry, constraints, routing guides, and design-rule requirements interact.

The final router was evaluated on seven supplied benchmarks and achieved:

```text
7 / 7 benchmarks with zero open nets
```

with routing times between:

```text
0.22 s and 11.77 s
```

The primary remaining issue is spacing-rule compliance, with the checker reporting:

```text
20 to 3991 spacing violations
```

across the evaluated benchmarks.

Thus, the final implementation demonstrates effective connectivity routing and practical execution time, while also providing a clear basis for future improvement in DRC-aware routing and congestion management.

---

# 22. Repository Documentation

The repository contains separate documentation at different levels:

```text
README.md
    └── High-level overview of assignments and project

REPORT.md
    └── Consolidated technical report

assignments/assignment_*/README.md
    └── Assignment-specific documentation

project/README.md
    └── Detailed project setup and execution instructions

project/REPORT.md
    └── Detailed project-specific report
```

The root report intentionally provides a consolidated view of the complete coursework and project rather than duplicating every implementation detail from the assignment-specific documentation.
