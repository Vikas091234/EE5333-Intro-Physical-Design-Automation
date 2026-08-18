# EE5333 – Introduction to Physical Design Automation

Coursework and selected physical design automation implementations from **EE5333 at IIT Madras**, including graph optimization, ILP, partitioning, floorplanning, SAT solving, placement, routing, and a LEF/DEF-based detailed routing course project.

## Repository structure

```text
ee5333-physical-design-automation/
├── README.md
├── REPORT.md
├── assignments/
│   ├── assignment_1/    # ILP: Minimum Dominating Set / MWIS
│   ├── assignment_2/    # Fiduccia–Mattheyses partitioning
│   ├── assignment_3/    # Floorplanning
│   ├── assignment_4/    # SAT solving
│   ├── assignment_5/    # Placement
│   └── assignment_6/    # Branch and Bound for ILP
└── project/
    ├── README.md
    ├── data/             # LEF/DEF and routing-guide inputs
    ├── scr/              # router, checker, solution writer
    └── output/           # selected generated DEF results
```

## Course project

The project implements a detailed routing workflow using LEF/DEF design data. The repository includes the routing implementation, DRC/connectivity checker, input benchmarks, routing guides, and selected generated DEF outputs.

### Main components
- LEF/DEF-based design-data handling
- Detailed routing implementation
- Routing-guide processing
- Connectivity checking
- Spacing DRC checking
- DEF solution generation

## Coursework topics

| Assignment | Topic |
|---|---|
| 1 | Integer Linear Programming – graph optimization |
| 2 | Fiduccia–Mattheyses graph partitioning |
| 3 | Floorplanning |
| 4 | Boolean satisfiability / SAT |
| 5 | Placement |
| 6 | Branch and Bound for ILP |

## Note

This repository contains selected implementation files and project data. Course lecture notes, textbooks, assignment handouts, and generated build artifacts are intentionally excluded.
