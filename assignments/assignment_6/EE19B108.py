"""
Course      : EE5333 - Introduction to Physical Design Automation
Assignment  : 6
Program     : Branch and Bound for Integer Linear Programming

Description :
Implements the branch and bound algorithm to find
the optimal solution of an integer linear program
using the provided simplex routine.

Author      : Vikas Raj
"""

from mip import Model, maximize, INTEGER
import numpy as np

eps = 1e-6
# define a value as integer if it is withing eps of its rounded value
# Nvar are the number of original variables
# The slack variables need not be integers and hence don’t need to be checked
def is_sol_integer(sol, Nvar):
    for i in range(Nvar):
        if abs(round(sol[i]) - sol[i]) > eps: return False
    return True

# Helper function for branch and bound
def bb_solve(m, obj, best_sol=None, best_f=-np.inf):
    # Solve current LP relaxation
    sol, f = simplex(m, obj)
    Nvar = len(m.vars)
    
    # If infeasible or worse than best, prune
    if np.isnan(f) or f <= best_f:  # assuming simplex returns nan or something for infeas, adjust if needed
        return best_sol, best_f
    
    # Check if integer solution
    if is_sol_integer(sol, Nvar) and f > best_f:
        return sol[:Nvar].copy(), f
    
    # Find branching variable (first fractional)
    branch_var = -1
    for i in range(Nvar):
        if abs(round(sol[i]) - sol[i]) > eps:
            branch_var = i
            break
    if branch_var == -1:
        # Should be integer, but anyway
        return sol[:Nvar].copy(), f
    
    # Branch
    floor_val = np.floor(sol[branch_var])
    ceil_val = np.ceil(sol[branch_var])
    
    # Left branch: x <= floor
    m_left = m.copy()
    x_var = m_left.vars[branch_var]
    m_left += x_var <= floor_val
    
    # Right branch: x >= ceil
    m_right = m.copy()
    x_var = m_right.vars[branch_var]
    m_right += x_var >= ceil_val
    
    # Recurse left
    left_sol, left_f = bb_solve(m_left, obj, best_sol, best_f)
    if left_f > best_f:
        best_sol = left_sol
        best_f = left_f
    
    # Recurse right
    right_sol, right_f = bb_solve(m_right, obj, best_sol, best_f)
    if right_f > best_f:
        best_sol = right_sol
        best_f = right_f
    
    return best_sol, best_f

def solve_ilp(m, obj):
    Nvar = len(m.vars)
    # Call branch and bound
    sol, f = bb_solve(m, obj)
    return sol, f