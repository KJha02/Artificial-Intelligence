#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 17:59:04 2021

@author: kunal
"""

from Constraint import Constraint

class MapConstraint(Constraint[str, str]):
    def __init__(self, loc1, loc2):
        super().__init__([loc1, loc2])
        self.loc1 = loc1 # the locations are strings
        self.loc2 = loc2

    def isSatisfied(self, assignment):

        if self.loc1 not in assignment or self.loc2 not in assignment: # if neither of the places are assigned, it's satisfied
            return True

        return assignment[self.loc1] != assignment[self.loc2] # if they have different assignments return True

class CircuitConstraint(Constraint[tuple, tuple]):
    def __init__(self, piece1, piece2):
        super().__init__([piece1, piece2])
        self.piece1 = piece1 # pieces are tuples of (width, height)
        self.piece2 = piece2
    def isSatisfied(self, assignment): # assignment maps rectangles to (xcoord, ycoord)
        # either hasn't been mapped to then it's false
        if self.piece1 not in assignment or self.piece2 not in assignment:
            return True
        
        # parsing minimum and maximum x and y coordinates for each piece
        x1 = (assignment[self.piece1][0], self.piece1[0] + assignment[self.piece1][0] - 1)
        x2 = (assignment[self.piece2][0], self.piece2[0] + assignment[self.piece2][0] - 1)
        y1 = (assignment[self.piece1][1], self.piece1[1] + assignment[self.piece1][1] - 1)
        y2 = (assignment[self.piece2][1], self.piece2[1] + assignment[self.piece2][1] - 1)
        
        if x2[0] >= x1[0] and x2[0] <= x1[1] and y2[0] >= y1[0] and y2[0] <= y1[1]: # piece 2 overlaps piece 1
            return False
        if x1[0] >= x2[0] and x1[0] <= x2[1] and y1[0] >= y2[0] and y1[0] <= y2[1]: # piece 1 overlaps piece 2
            return False

        return True # no piece overlaps
    
    