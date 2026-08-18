# Assignment 1 – Physical Design Automation

## Course

EE5333 – Introduction to Physical Design Automation

## Objective

This assignment formulates two graph problems as Integer Linear
Programs (ILPs) and solves them using the `mip` optimization library:

- Minimum Dominating Set (MDS)
- Minimum-weighted Independent Set (MWIS)

## Problems

### Minimum Dominating Set

The objective is to find the smallest set of vertices such that
every vertex in the graph is either part of the set or adjacent
to a vertex in the set.

### Minimum-weighted Independent Set

The objective is to find an independent set of vertices with
maximum total weight, where no two selected vertices are adjacent.

## Implementation

The assignment contains two functions:

```text
mds(N, E)
mwis(N, E, W)