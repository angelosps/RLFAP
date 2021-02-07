import sys
import time
import itertools
import random
import re
import string

import csp

# Some globals
# ____________________________________________________________________

constraintsChecked = 0
weight = {}     # for dom/wdeg heuristic
conf_set = {}   # for fc-cbj
order = {}      # for fc-cbj

# Functions that I have changed a little bit from csp.py
# ____________________________________________________________________


def AC3(csp, queue=None, removals=None, arc_heuristic=csp.dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    if not csp.curr_domains[Xi]: # if dom(X) emptied
        weight[(Xi, Xj)] += 1
        weight[(Xj, Xi)] += 1
    return revised, checks

def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                conf_set[B].add(var)    # domain wipe out for B, because of some value of var
                weight[(var, B)] += 1
                weight[(B, var)] += 1
                return False
    return True

def min_conflicts(c, max_steps=1000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    c.current = current = {}
    ans = 0
    for var in c.variables:
        val = csp.min_conflicts_value(c, var, current)
        c.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = c.conflicted_vars(current)
        if not conflicted:
            return current
        if i == max_steps-1:      # last time is also the best assignment for algorithm because every time improves the solution (minimizes the conflicts)
            ans = len(conflicted) # get the number of conflicted variables (constraints violated at the moment)
        var = random.choice(conflicted)
        val = csp.min_conflicts_value(c, var, current)
        c.assign(var, val, current)
    print("Constraints violated: %d" % ans)
    return None


''' The FC-CBJ hybrid '''

counter = 1
def hybrid(csp, select_unassigned_variable=csp.first_unassigned_variable,
                        order_domain_values=csp.unordered_domain_values, inference=forward_checking):
    visited = set()
    for var in csp.variables:
        conf_set[var] = set()
        order[var] = 0

    def fc_cbj(assignment):
        global counter
        if len(assignment) == len(csp.variables):
            return assignment, None
        var = select_unassigned_variable(assignment, csp)
        order[var] = counter
        counter += 1
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result, h = fc_cbj(assignment)
                    if result is not None:
                        return result, None
                    elif var in visited and var != h:
                        conf_set[var].clear()
                        visited.discard(var)
                        csp.restore(removals)
                        csp.unassign(var, assignment)
                        return None, h   
                csp.restore(removals)
        csp.unassign(var, assignment)
        visited.add(var)
        h = None
        maxi = 0
        if len(conf_set[var]):
            for c in conf_set[var]:
                if order[c] > maxi:
                    maxi = order[c]
                    h = c
            conf_set[h].union(conf_set[var])
            conf_set[h].discard(h)             
        return None, h

    result, h = fc_cbj({})
    assert result is None or csp.goal_test(result)
    return result    


# _______________________________________________________________
# dom/wdeg heuristic function for dynamic variable ordering

def dom_wdeg_heuristic(assignment, csp):
    """The dom/wdeg heuristic."""
    wdeg = {}
    minVal = float('inf')
    bestVar = 0
    for var in csp.variables:
        wdeg[var] = 1
        if var in assignment:
            continue
        for y in CSPNeighbors[var]:
            wdeg[var] += weight[(var, y)]
        if csp.curr_domains:
            domX = csp.curr_domains[var]
        else:
            domX = CSPDomains[var]
        ratio = (float) (len(domX) / wdeg[var])
        if ratio < minVal:
            minVal = ratio
            bestVar = var     
    return bestVar


#_______________________________________________________________________________
# Defining the RLFAP 

CSPVariables = []
CSPDomains = {}
CSPNeighbors = {}
CSPConstraints = {}

def rlfap_constraint(A, a, B, b):
    global constraintsChecked
    constraintsChecked += 1
    pair = CSPConstraints[(A,B)]
    op = pair[0]    # is the operator
    k = pair[1]     # the k value
    if op == 0:     # operator '=' 
        return abs(a-b) == k
    if op == 1:
        return abs(a-b) > k

def rlfap_parse():
    args = list(sys.argv)
    myfiles = []
    myfiles.append(str('var'+args[1]+'.txt'))
    myfiles.append(str('dom'+args[1]+'.txt'))
    myfiles.append(str('ctr'+args[1]+'.txt'))

    # reading the variables from file var<instanceID>.txt
    variables = []
    with open(myfiles[0]) as f:
        h = [int(x) for x in next(f).split()] # read first line
        for line in f: # read rest of lines
           variables.append([int(x) for x in line.split()])
    
    # reading the domains from file dom<instanceID>.txt
    domains = []
    with open(myfiles[1]) as f:
        h = [int(x) for x in next(f).split()] # read first line
        for line in f: # read rest of lines
            domains.append([int(x) for x in line.split()[2:]])
    
    # reading the constraints from file ctr<instanceID>.txt
    for v in range(len(variables)):
        CSPNeighbors[v] = []
    
    with open(myfiles[2]) as f:
        h = [int(x) for x in next(f).split()] # read first line
        for line in f: # read rest of lines
            line = line[:-1]
            ln = line.split()
            # x[0] = x, x[1] = y, x[2] = operator, x[3] = k
            x = int(ln[0]) 
            y = int(ln[1])
            op = ln[2]
            k = int(ln[3])
            if op == "=":
                opcode = 0
            else:
                opcode = 1    
            CSPConstraints[(x,y)] = (opcode, k)
            CSPConstraints[(y,x)] = (opcode, k)
            CSPNeighbors[x].append(y)
            CSPNeighbors[y].append(x)
    
    CSPVariables = []
    for v in variables:
        CSPVariables.append(v[0])

    for v in variables:
        # v = [variable, variable's domain]
        CSPDomains[v[0]] = domains[v[1]]


def rlfap():
    rlfap_parse() # get the data from the txt files and put them into the appropriate data structures
    return csp.CSP(CSPVariables, CSPDomains, CSPNeighbors, rlfap_constraint)


def main():
    c = rlfap() # construct the RLFA CSP problem
    for constr in CSPConstraints:
        weight[constr] = 1    
    for var in c.variables:
        conf_set[var] = set()
        order[var] = 0
    
    args = list(sys.argv)
    instance = args[1]
    method = args[2]
    tic = time.perf_counter()
    if method == "FC":
        print("Trying to solve the instance \"%s\" using %s + dom/wdeg heuristic...\n" % (instance, method))
        sol = csp.backtracking_search(c, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=forward_checking)
    elif method == "MAC":
        print("Trying to solve the instance \"%s\" using %s + dom/wdeg heuristic...\n" % (instance, method))
        sol = csp.backtracking_search(c, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=mac)
    elif method == "FC-CBJ":
        print("Trying to solve the instance \"%s\" using %s + dom/wdeg heuristic...\n" % (instance, method))
        sol = hybrid(c, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=forward_checking)
    elif method == "Min-Conflicts":
        print("Trying to solve the instance \"%s\" using %s...\n" % (instance, method))
        sol = min_conflicts(c)
    else: 
        exit('Invalid method. Choose between: FC/MAC/FC-CBJ/Min-Conflicts')

    toc = time.perf_counter()

    print("UNSAT" if sol == None else sol)    
    print("\nAssignments: %d" % c.nassigns)
    print("Constraint checks: %d\n" % constraintsChecked)
    print(f"Time: {toc - tic:0.4f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3: exit('Command line argument: <instanceID> <Method>:FC/MAC/FC-CBJ/Min-Conflicts')
    main()
    