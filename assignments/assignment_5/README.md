# Assignment 5 – Graph Isomorphism

## Course

EE5333 – Introduction to Physical Design Automation

## Objective

This assignment implements a graph isomorphism algorithm for
undirected simple graphs with vertex attributes.

The program determines whether two graphs are isomorphic and,
if they are, returns a mapping between the vertices of the two
graphs.

## Problem

Two graphs are isomorphic if there exists a one-to-one mapping
between their vertices such that:

- Corresponding vertices have the same attributes.
- Edges are preserved under the mapping.
- Every vertex in one graph is mapped to exactly one vertex in
  the other graph.

If no such mapping exists, the program returns `None`.

## Input Representation

Each graph is represented as:

```python
(
    [vertex_attributes],
    [(u, v), ...]
)