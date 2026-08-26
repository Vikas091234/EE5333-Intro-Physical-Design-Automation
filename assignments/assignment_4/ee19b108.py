"""
Course      : EE5333 - Introduction to Physical Design Automation
Assignment  : 4
Program     : DPLL SAT Solver

Description :
Implements the Davis-Putnam-Logemann-Loveland (DPLL)
algorithm for solving Boolean satisfiability problems
in DIMACS CNF format.

Author      : Vikas Raj
"""



class Clause:
    def __init__(self, vl):
        self._vars = [v for v in vl]
        self._vact = [True for v in vl]
        self._nact = len(self._vars)
        self._val  = None 

    def eval(self, m):
        """
        Evaluates the clause based on assignment m.
        Returns: True (satisfied), False (unsatisfied/conflict), or None (unresolved).
        """
        has_undecided = False
        for lit in self._vars:
            var = abs(lit)
            val = m[var]
            
            if val is None:
                has_undecided = True
                continue
            
            # If literal is x and assignment is True, or literal is -x and assignment is False
            if (lit > 0 and val is True) or (lit < 0 and val is False):
                return True
        
        return None if has_undecided else False

    def getUnitVal(self):
        """Returns the literal of a unit clause."""
        if self._nact == 1:
            for i in range(len(self._vars)):
                if self._vact[i]:
                    return self._vars[i]
        return None
  
    def propagate(self, m):
        """Updates internal state based on assignment m."""
        new_vact = []
        for lit in self._vars:
            var = abs(lit)
            # Literal is active if its variable is unassigned
            if m[var] is None:
                new_vact.append(True)
            else:
                new_vact.append(False)
        
        self._vact = new_vact
        self._nact = sum(1 for v in self._vact if v)
        self._val = self.eval(m)
        return self._val

    def __repr__(self):
        return '[' + str(self._vars) + ' ' + str(self._vact) + ' ' + str(self._nact) + ' ' + str(self._val) + ']'


def unitClauses(f, m):
    """Finds clauses that have exactly one unassigned literal and are not yet satisfied."""
    units = []
    for c in f:
        # Re-evaluate internal state
        status = c.propagate(m)
        if status is None and c._nact == 1:
            units.append(c.getUnitVal())
    return units
        

def pureLiterals(f, m):
    """Finds literals that appear with only one polarity in all unresolved clauses."""
    literals_found = {} # var -> set of polarities seen
    
    for c in f:
        if c.eval(m) is True: continue # Skip satisfied clauses
        for lit in c._vars:
            var = abs(lit)
            if m[var] is None:
                if var not in literals_found:
                    literals_found[var] = set()
                literals_found[var].add(1 if lit > 0 else -1)
    
    pure = []
    for var, polarities in literals_found.items():
        if len(polarities) == 1:
            polarity = list(polarities)[0]
            pure.append(var if polarity > 0 else -var)
    return pure


def pickBranchingLiteral(m):
    l = [i for i in range(1, len(m)) if m[i] is None]
    return l[0] if len(l) else None


def dpll(f, m):
    # 1. Unit Propagation [cite: 49-53]
    while True:
        units = unitClauses(f, m)
        if not units: break
        l = units[0]
        m[abs(l)] = (l > 0)
    
    # 2. Pure Literal Elimination [cite: 54-56]
    pures = pureLiterals(f, m)
    for p in pures:
        m[abs(p)] = (p > 0)

    # 3. Check Status [cite: 57-61]
    all_satisfied = True
    for c in f:
        val = c.propagate(m)
        if val is False: return False, m # Conflict
        if val is None: all_satisfied = False
    
    if all_satisfied: return True, m

    # 4. Branching [cite: 62-63]
    l = pickBranchingLiteral(m)
    if l is None: return True, m

    # Try True
    m_true = list(m)
    m_true[l] = True
    res, final_m = dpll(f, m_true)
    if res: return True, final_m

    # Try False
    m_false = list(m)
    m_false[l] = False
    return dpll(f, m_false)


def loadCNFFile(fn):
    numvars = 0
    numclauses = 0
    clauses = []
    current_clause = []

    with open(fn, 'r') as fs:

        for line in fs:

            line = line.strip()

            # Ignore blank lines and comments
            if not line or line.startswith('c'):
                continue

            # End of DIMACS file
            if line.startswith('%'):
                break

            # Problem description
            if line.startswith('p'):
                parts = line.split()
                numvars = int(parts[2])
                numclauses = int(parts[3])
                continue

            # Read literals
            for value in line.split():

                literal = int(value)

                if literal == 0:

                    # End of current clause
                    clauses.append(Clause(current_clause))
                    current_clause = []

                else:
                    current_clause.append(literal)

    return numvars, clauses

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cnf", type=str, default="", help='<cnf file>')
    args = ap.parse_args()
    if args.cnf != "":
        print(f"CNF file  : {args.cnf}")
        numvars, clauses = loadCNFFile(args.cnf)
        m = [None for i in range(numvars + 1)]
        ret, final_m = dpll(clauses, m)
        if ret:
            print("Satisfiable")
            print([(i if final_m[i] == True else -i) for i in range(1, len(final_m))])
        else:
            print("Unsatisfiable")