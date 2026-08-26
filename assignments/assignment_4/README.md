# Assignment 4 – DPLL SAT Solver

## Course

EE5333 – Introduction to Physical Design Automation

## Objective

This assignment implements the Davis-Putnam-Logemann-Loveland
(DPLL) algorithm for solving Boolean Satisfiability (SAT)
problems represented in Conjunctive Normal Form (CNF).

The implementation reads CNF files in DIMACS format and
determines whether the given Boolean formula is satisfiable.

## Algorithm

The DPLL solver performs the following steps:

1. Unit-clause propagation
2. Pure-literal elimination
3. Conflict detection
4. Satisfiability checking
5. Branching on an unassigned variable
6. Recursive search using both possible assignments

## Implementation

### Clause

The `Clause` class represents a CNF clause and supports:

- Clause evaluation
- Unit-literal detection
- Propagation of assignments

### Unit Propagation

If a clause contains only one unassigned literal, that literal
must take the value that satisfies the clause.

### Pure Literal Elimination

If a variable occurs with only one polarity in all unresolved
clauses, it can be assigned that polarity without affecting
satisfiability.

### Branching

When unit propagation and pure-literal elimination cannot
determine the remaining variables, the solver selects an
unassigned variable and recursively tries:

- Variable = True
- Variable = False

## Files

| File | Description |
|---|---|
| `dpll.py` | DPLL SAT solver implementation |
| `CNF_Examples/` | Example DIMACS CNF input files |
| `README.md` | Assignment documentation |

## Input Format

The solver accepts CNF files in DIMACS format.

Example:

```text
c Example CNF
p cnf 3 2
1 -2 3 0
-1 2 0