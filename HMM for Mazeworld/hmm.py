#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 22:18:07 2021

@author: kunal
"""

import numpy as np


# class that uses a Hidden Markov Model to solve a Mazeworld problem
# has both filtering and smoothing functionality
class HMM:

    def __init__(self, maze, sensorReadings, mazeColors):

        self.maze = maze  # robot's maze
        self.sensorReadings = sensorReadings  # sensor readings
        self.mazeColors = mazeColors  # colors of each square
        self.start_state = self.initializeState() # initialize state distributiopns

        # dictionary for number of colors in a maze
        # used for generating probability of being in a square given color
        self.colorToNum = {'r': 0,'b': 0,'g': 0,'y': 0}
        
        
        for color in self.mazeColors.values():
            self.colorToNum[color] += 1  # update number of each color

        # 16x16 transition model
        self.transitionModel = self.getTransitionModel()

        # sensor models for each color as a 4x4 array
        self.rModel = self.getSenseModel('r')  # r
        self.bModel = self.getSenseModel('b')  # b
        self.yModel = self.getSenseModel('y')  # y
        self.gModel = self.getSenseModel('g')  # g

    # calculate probability distributions given sensor readings
    def computeDistrib(self):

        state = self.initializeState()
        sequence = [np.flipud(state)]  # add start state to state sequence

        for color in self.sensorReadings: # iterate through all colors in reading

            state = np.reshape(state, (1, 16)) # reshape state for multiplication
            state = np.matmul(state, self.transitionModel) # multiple by transition model

            state = np.reshape(state, (self.maze.width, self.maze.height)) # reshape back to 4x4

            if color == 'r':
                state *= self.rModel
            if color == 'g':
                state *= self.gModel
            if color == 'b':
                state *= self.bModel
            if color == 'y':
                state *= self.yModel

            state = self.normalize(state) # normalize state
            sequence.append(np.flipud(state)) # add state to sequence

        return sequence

    # forward-backward smoothing
    def distribSmoothing(self):

        frontState = self.initializeState() # initialize uniform smoothing
        backState = self.initializeState()

        frontSequence = [np.flipud(frontState)]
        backSequence = [np.flipud(backState)]

        # forward loop is like normal filtering
        for color in self.sensorReadings:

            frontState = np.reshape(frontState, (1, 16))
            frontState = np.matmul(frontState, self.transitionModel)

            frontState = np.reshape(frontState, (self.maze.width, self.maze.height))

            if color == 'r':
                frontState *= self.rModel
            if color == 'g':
                frontState *= self.gModel
            if color == 'b':
                frontState *= self.bModel
            if color == 'y':
                frontState *= self.yModel

            frontState = self.normalize(frontState)
            frontSequence.append(np.flipud(frontState))

        # loop backward through readings
        for color in self.sensorReadings[::-1]:

            # sensor model used before transition model in backwards
            if color == 'r':
                backState *= self.rModel
            if color == 'g':
                backState *= self.gModel
            if color == 'b':
                backState *= self.bModel
            if color == 'y':
                backState *= self.yModel

            backState = np.reshape(backState, (1, 16))
            backState = np.matmul(backState, self.transitionModel)

            backState = np.reshape(backState, (self.maze.width, self.maze.height))

            backState = self.normalize(backState)
            backSequence.append(np.flipud(backState))

        # reverse the backward sequence to go from time 0 to n
        backSequence.reverse()

        smoothed = []
        for i, state in enumerate(frontSequence):
            smooth = state * backSequence[i]  # multiply
            smooth = self.normalize(smooth)  # normalize
            smoothed.append(smooth)

        return smoothed

    def initializeState(self):
        start = np.zeros((self.maze.width, self.maze.height)) # empty state

        # iterate through squares and add uniform prob
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    start[y, x] = 1/len(self.mazeColors)

        return start


    def getSenseModel(self, color):
        # initialize sensor probability matrix
        matProbSense = np.zeros((self.maze.width, self.maze.height))

        # iterate through all squares
        for x in range(self.maze.width):
            for y in range(self.maze.height):

                if self.maze.is_floor(x, y):

                    # There is a 0.88 chance that the read color matches the actual color
                    if self.mazeColors[(x, y)] == color:
                        prob = 0.88/self.colorToNum[color]
                        matProbSense[y, x] = prob

                    # otherwise probability = 0.12 it is not that color
                    else:
                        num_color = self.colorToNum[self.mazeColors[(x, y)]]
                        prob = 0.04/num_color
                        matProbSense[y, x] = prob

        return matProbSense

    # transition model
    def getTransitionModel(self):

        # initialize transition matrix
        transMat = np.zeros((16, 16))

        for y, column in enumerate(self.start_state):
            for x, value in enumerate(column):

                # imagine a 1x16 array
                curr = self.oneDimConvert((x, y))

                # get neighbors and track moves from each square
                moves = self.get_moves((x, y))
                netMoves = len(moves)

                # each move's probability increases by 1/total
                for move in moves:
                    next = self.oneDimConvert(move)
                    transMat[next, curr] += 1/netMoves

        return np.transpose(transMat)

    def get_moves(self, square):
        neighbors = []

        # loop through all possible moves
        for i, d in enumerate([-1, 1, -1, 1]):

            # first 2 neighbors will be change in x
            if i < 2:
                neighbor = (square[0] + d, square[1])

            # last 2 will be change in y
            else:
                neighbor = (square[0], square[1] + d)

            # only add moves in maze
            if self.maze.is_floor(neighbor[0], neighbor[1]):
                neighbors.append(neighbor)
                
            # if not floor, the robot doesn't move
            else:
                neighbors.append(tuple(square))

        return neighbors

    # 2d to 1d matrix - used for transition model
    def oneDimConvert(self, square):

        # y value multiplied by items in row + x value
        return self.maze.width * square[1] + square[0]

    # normalizes array values
    def normalize(self, state):
        net = np.sum(state)
        state = state / net
        return state