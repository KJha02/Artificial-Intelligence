#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 17:46:06 2021

@author: kunal
"""

from typing import Generic, TypeVar
from abc import ABC, abstractmethod

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables):
        self.variables = variables
        
    @abstractmethod
    def isSatisfied(self, assignment):
        ...