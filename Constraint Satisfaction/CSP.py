#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 17:48:24 2021

@author: kunal
"""

from typing import Generic, TypeVar
V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

class CSP(Generic[V, D]):
    def __init__(self, var, domain, MRV = False, DH = False, AC3=False):
        self.var = var # variables to be constrained
        self.domain = domain # domain of each variable
        self.constraints = {} # constraints for each variable
        for variable in self.var: # initialize constraints
            self.constraints[variable] = []
        self.MRV = MRV # is MRV heuristic enable
        self.DH = DH # is DH heuristic enable
        self.AC3Enabled = AC3

    def add_constraint(self, constraint): # takes in a constraint object
        for variable in constraint.variables: # add the constraint to all variables involved in constraint
            self.constraints[variable].append(constraint)

    def isConsistent(self, variable, assignment): # checks whether all constraints are satisfied given an assignment
        for constraint in self.constraints[variable]:
            if not constraint.isSatisfied(assignment):
                return False
        return True

    def backTrack(self, assignment = {}, LCV=False): # recursive back checking
        if len(assignment) == len(self.var): # this is a little hacky but indicates the solution is found
            return assignment

        unassigned = [v for v in self.var if v not in assignment] # determine all unassigned variables
        
        first = unassigned[0] # unassigned vars is the default 

        if self.MRV:
            first = self.MRVvar(unassigned) # MRV heuristic
        elif self.DH: # if MRV not enabled
            first = self.DHvar(unassigned) # Degree heuristic
        
        
        if LCV == True:
            self.domain[first] = self.orderDomainValues(first)
        
        for value in self.domain[first]: # iterate through all values
            localAssign = assignment.copy()
            localAssign[first] = value
            if self.isConsistent(first, localAssign): # see whether value is consistent
                if self.AC3Enabled: # calling AC3 if it's enabled
                    self.AC3()
                res = self.backTrack(localAssign, LCV) # if it is then backtrack
                if res != None:
                    return res # return a solution if one exists
            
        return None # no solution then return None
    

    def orderDomainValues(self, variable):
        def sortDomains(value): # sort function ranks by number of neighbor values still satisfiable
            count = 0
            tempAssignment = {variable: value}
            for neighbors in self.constraints[variable]:
                otherVar = None
                for other in neighbors.variables:
                    if other != variable:
                        otherVar = other
                for vals in self.domain[otherVar]:
                    tempAssignment[otherVar] = vals
                    if neighbors.isSatisfied(tempAssignment):
                        count += 1
            return count
                        
        tempVar = self.domain[variable]
        tempVar.sort(key = sortDomains, reverse=True)
        return tempVar
    
    def MRVvar(self, unassigned):
        shortestLength = float("inf") # initialize shortest length of domain
        shortestVar = None
        for var in unassigned: # determine variable with sortest domain length
            if len(self.domain[var]) < shortestLength:
                shortestVar = var
                shortestLength = len(self.domain[var])
        return shortestVar # return var
    
    def DHvar(self, unassigned):
        maxDegree = -1 # initialize biggest constraint list
        maxVar = None
        for var in unassigned: # determine variable that is most constrained
            if len(self.constraints[var]) > maxDegree:
                maxVar = var
                maxDegree = len(self.constraints[var])
        return maxVar # return most constrained var
    
    def AC3(self):
        q = [] # initialize queue by adding all arcs
        for var in self.constraints:
            for arcConstraint in self.constraints[var]:
                q.append((var, arcConstraint))
                
        while len(q) > 0: # while queue is not empty
            xi, constraint = q.pop() # remove xi and a constraint
            xj = None # determine the variable xj
            for i in constraint.variables:
                if i != xi:
                    xj = i
            
            if self.Revise(xi, xj, constraint):
                if len(self.domain[xi]) == 0: # if domain is empty
                    return False
                for arc in self.constraints[xi]: # neighbors
                    xk = None
                    for i in arc.variables:
                        if i != xi:
                            xk = i
                    if arc != constraint: # if xk != xj
                        q.append((xk, constraint)) # add arc to queue
        return True
    
    def Revise(self, xi, xj, constraint):
        revised = False
        for x in self.domain[xi]: # for all x in the domain of xi
            tempAssignment = {xi: x} 
            satisfiableY = False
            for y in self.domain[xj]: # for all y in the domain of xj
                tempAssignment[xj] = y
                if constraint.isSatisfied(tempAssignment):
                    satisfiableY = True
            if satisfiableY == False: # if there is no satisfiable assignment
                self.domain[xi].remove(x) # remove x from the domain of xi
                revised = True
        return revised
    
    
    