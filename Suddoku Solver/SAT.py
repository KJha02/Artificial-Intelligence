#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:58:46 2021

@author: kunal
"""
import random


class SAT:
    def __init__(self, puzzle):
        self.clauses = []
        self.variables = tuple()
        self.sortClause(puzzle)
        self.statesVisited = 0         
        self.unsolvedClauses = 0      

    def sortClause(self, puzzle): # parses cnf file
        var = []
        with open(puzzle, "r") as file:
            for line in file:
                
                line = line.replace("\n", "") # remove line from clause list
                clause = line.split(" ")
                while "" in clause:
                    clause.remove("")

                newClause = set()
                isNegative = False
                for c in clause:
                    temp = c
                    if c[0] == "-":
                        temp = c[1:]
                        isNegative = True

                    if temp not in var:
                        var.append(temp)

                    if isNegative:
                        newClause.add(-1 * (var.index(temp) + 1))
                    else:
                        newClause.add(var.index(temp) + 1)

                self.clauses.append(newClause)

            self.variables = tuple(var)

    def walk_sat(self, p=.3, maxFlips=100000):
        model = self.getRandomModel() # initialize random model

        for i in range(maxFlips): # iterate until max flips
            self.statesVisited += 1

            solved = self.goalTest(model) # return correct answer if solved
            if solved:
                return self.solToCNF(model)

            # Find the unsolved clauses
            self.unsolvedClauses = 0
            clauseSet = self.clauseSet(model)
            clause = random.choice(clauseSet)

            rand = random.random()
            if rand < p: # deciding if a random choice is made or not
                temp = random.choice(list(clause))
                model.remove(-1 * temp)
                model.add(temp)

            # If no random choice, pick the best candidate
            else:
                scores = {}
                for var in clause:
                    tempModel = set(model)
                    tempModel.remove(-1 * var)
                    tempModel.add(var)

                    score = self.countFulfilled(tempModel)
                    
                    # score is a key
                    if score in scores:
                        scores[score].append(var)
                    else:
                        scores[score] = [var]

                # Get the highest scoring bit
                sort = sorted(scores.keys(), reverse=True)
                maxBit = random.choice(scores[sort[0]])

                model.remove(-1 * maxBit)
                model.add(maxBit)
        return False

    # Creates a list of clause sets that are disjoint from the model
    def clauseSet(self, model):
        clauseSet = []
        for clause in self.clauses:
            if clause.isdisjoint(model):
                clauseSet.append(clause)
                self.unsolvedClauses += 1

        return clauseSet

    # GSAT Algorithm
    def gsat(self, p=.3, starter=None):
        # Starter model is just for testing
        if starter:
            model = starter
        else:
            model = self.getRandomModel()

        answer = self.gsatHelper(model, p) # call the helper to find the answer
        return self.solToCNF(answer)


    def gsatHelper(self, model, p):
        self.statesVisited += 1
        solved = self.goalTest(model) # return the solution if found
        if solved:
            return model

        rand = random.random()
        # Change a random bit if below a threshold and recheck the model
        if rand < p:
            rando = random.choice(list(model))
            model.remove(rando)
            model.add(-1 * rando)

            return self.gsatHelper(model, p)

        # Change the best bit out of all bits if above a threshold
        else:
            scores = {}
            for var in model:
                tempModel = set(model)
                tempModel.remove(var)
                tempModel.add(-1 * var)

                score = self.countFulfilled(tempModel)

                if score in scores: # score is a key
                    scores[score].append(var)
                else:
                    scores[score] = [var]

            # Get the highest scoring bit
            sort = sorted(scores.keys(), reverse=True)
            maxBit = random.choice(scores[sort[0]])

            model.remove(maxBit)
            model.add(-1 * maxBit)

            return self.gsatHelper(model, p)


    def getRandomModel(self): # determine random model to begin SAT
        model = set()

        for var in self.variables:
            alpha = random.random()
            if alpha < .5:
                model.add(-1 * (self.variables.index(var) + 1))
            else:
                model.add(self.variables.index(var) + 1)

        return model


    def countFulfilled(self, model): # number of filfilled clauses
        count = 0
        for clause in self.clauses:
            if not clause.isdisjoint(model):
                count += 1

        return count

    def goalTest(self, model): # check if all clauses are satisfied
        solved = True
        for clause in self.clauses:
            if clause.isdisjoint(model):
                solved = False

        return solved

    def solToCNF(self, answer): # converts solution to cnf
        res = []
        for a in answer:
            if a == abs(a):
                res.append(self.variables[a - 1])  # Accounts for shift
            else:
                res.append("-" + self.variables[abs(a) - 1])

        return res

    # Makes a .sol file
    def write_solution(self, file_name, result):
        with open(file_name, "w") as f:
            f.write(str(result[0]))
            for bit in result:
                f.write("\n" + str(bit))

if __name__ == "__main__":
    sat = SAT("test.cnf")

    model_a = {1, 2, -3, -4, -5, -6, -7, -8, -9}

    check_ans = sat.goalTest(model_a)
    print(check_ans)

    ans = sat.walk_sat()
    print(ans)