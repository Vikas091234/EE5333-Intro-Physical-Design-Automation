# Assignment 6 – Branch and Bound for ILP

## Course

EE5333 – Introduction to Physical Design Automation

## Objective

This assignment implements the Branch and Bound algorithm
for solving Integer Linear Programming (ILP) problems.

The provided simplex routine is used to solve the linear
programming relaxation at each node of the branch and bound
search tree.

The objective is to find the optimal integer solution and
corresponding objective value.

## Approach

The implementation follows these steps:

1. Solve the LP relaxation using the simplex algorithm.
2. Check whether the solution is integer-valued.
3. If the solution is integer-valued, update the best solution.
4. If the solution contains fractional variables, select a
   fractional variable for branching.
5. Create two subproblems:
   - `x <= floor(x*)`
   - `x >= ceil(x*)`
6. Recursively solve both subproblems.
7. Prune branches whose LP bound cannot improve the current
   best integer solution.

## Integer Check

Only the original decision variables are required to be
integer-valued.

Slack variables introduced by the simplex formulation are
not required to be integers.

A tolerance of:

```python
eps = 1e-6