# Assignment 2 – Physical Design Automation

## Course

EE5333 – Introduction to Physical Design Automation

## Objective

This assignment implements the Fiduccia-Mattheyses (FM) algorithm
for bi-partitioning a hypergraph.

The objective is to divide the vertices into two partitions while
satisfying the specified area constraints and minimizing the number
of cut hyperedges.

## Algorithm

The implementation follows the FM partitioning approach:

1. Create an initial balanced partition.
2. Calculate the gain of moving each unlocked vertex.
3. Select the highest-gain legal move.
4. Lock the moved vertex.
5. Continue until no legal moves remain.
6. Identify the best intermediate partition from the sequence of moves.
7. Roll back moves after the best point.
8. Repeat the process for additional passes until no improvement occurs.

## Function

```python
partitionFM(V, E, Amin, Amax)