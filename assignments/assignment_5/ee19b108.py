"""
Course      : EE5333 - Introduction to Physical Design Automation
Assignment  : 5
Program     : Graph Isomorphism

Description :
Determines whether two attributed undirected simple graphs
are isomorphic and returns a valid vertex mapping if one
exists.

Author      : Vikas Raj
"""

from itertools import permutations

def is_isomorphic(G, H):
    attr_G, edges_G = G
    attr_H, edges_H = H
    
    n = len(attr_G)

    # Step 1: Basic checks
    if n != len(attr_H):
        return None
    
    if len(edges_G) != len(edges_H):
        return None
    
    if sorted(attr_G) != sorted(attr_H):
        return None

    # Convert edges to set (undirected)
    edges_G_set = set()
    for u, v in edges_G:
        edges_G_set.add((u, v))
        edges_G_set.add((v, u))
    
    edges_H_set = set()
    for u, v in edges_H:
        edges_H_set.add((u, v))
        edges_H_set.add((v, u))

    # Step 2: Try all permutations
    for perm in permutations(range(n)):
        
        # Check attribute match
        valid = True
        for i in range(n):
            if attr_G[i] != attr_H[perm[i]]:
                valid = False
                break
        
        if not valid:
            continue
        
        # Check edge consistency
        valid = True
        for u, v in edges_G:
            if (perm[u], perm[v]) not in edges_H_set:
                valid = False
                break
        
        if valid:
            return list(perm)

    return None