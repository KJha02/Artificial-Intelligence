#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 18:01:25 2021

@author: kunal
"""
from CSP import CSP
from ConstraintProblems import CircuitConstraint, MapConstraint

def drawBoard(maxWidth, maxHeight, res):
    board = [] # initialize board as 2d array
    for j in range(maxHeight):
        row = []
        for i in range(maxWidth):
            row.append(".")
        board.append(row)
    
    keyToNum = {} # convert keys to numbers for ascii art
    i = 1
    for key in res:
        keyToNum[key] = str(i)
        i += 1
    
    for key in res: # for all keys
        startX, startY = res[key] # get x and y coordinates
        width, height = key
        display = keyToNum[key] 
        
        for i in range(startY, startY+height):
            for j in range(startX, startX+width):
                board[i][j] = display # update board with coordiantes
        
    string = "" # convert array into string by joining rows and concatenating 
    for i in range(len(board)):
        row = "".join(board[i])
        string += row + "\n"
    
    return string

def CircuitDriver(maxWidth, maxHeight, variables, DH=False, MRV=False, AC3=False, LCVEnabled=False):
    domains = {} # initialize domains to be every legal coordinate
    for var in variables:
        potentialLoc = []
        for i in range(maxWidth - var[0] + 1): # x coordinate can't go past border
            for j in range(maxHeight - var[1] + 1): # y coordinate can't go past border
                potentialLoc.append((i, j)) # add coordinate to locations list
        domains[var] = potentialLoc # all possible locations of a variable
        
    csp = CSP(variables, domains, DH = DH, MRV = DH, AC3=AC3) # instantiate CSP
    
    for var in variables:
        for other in variables:
            if var != other:
                csp.add_constraint(CircuitConstraint(var, other)) # no box can overlap with each other
    
    
        
    res = csp.backTrack(LCV=LCVEnabled) # determine result and print if one exists
    if res == None:
        print("No solution found!")
    else:
        print(drawBoard(maxWidth, maxHeight, res))
        
def MapDriver(DH=False, MRV=False, LCVEnabled=False,AC3=False):
    var = ["WA", "NT", "SA", "Q", "NSW", "V", "T"] # all variables in the map
    domains = {} # they can initially be red green or blue
    for variable in var:
        domains[variable] = ["red", "green", "blue"]
        
    csp = CSP(var, domains, DH = DH, MRV = MRV, AC3=AC3) # instantiate CSP
    
    # constraint all neighbors according to diagram
    csp.add_constraint(MapConstraint("WA", "NT")) 
    csp.add_constraint(MapConstraint("WA", "SA"))
    csp.add_constraint(MapConstraint("SA", "NT"))
    csp.add_constraint(MapConstraint("Q", "NT"))
    csp.add_constraint(MapConstraint("Q", "SA"))
    csp.add_constraint(MapConstraint("Q", "NSW"))
    csp.add_constraint(MapConstraint("NSW", "SA"))
    csp.add_constraint(MapConstraint("V", "SA"))
    csp.add_constraint(MapConstraint("V", "NSW"))
    csp.add_constraint(MapConstraint("V", "T"))
    

    res = csp.backTrack(LCV=LCVEnabled) # print a solution if one exists
    if res == None:
        print("No solution found!")
    else:
        print(res)
        
#var = [(3,2), (4,1), (1,6)]
#CircuitDriver(maxWidth=6, maxHeight=6, variables=var, DH=False, MRV=False, AC3 = True, LCVEnabled = False)        

# uncomment to run Map Driver, can follow instructions in README to modify problem
MapDriver(DH=True, MRV=True, LCVEnabled=True, AC3=False) 

# uncomment to run Circuit Problem, can follow instructions in README to modify problem
