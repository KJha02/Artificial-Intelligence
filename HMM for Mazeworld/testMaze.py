#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 22:20:38 2021

@author: kunal
"""

from hmm import HMM
from Maze import Maze
import random
from time import time


# assign random colors to floor spaces
def randColors(maze):
    colorSpace = ['r', 'g', 'b', 'y']
    mazeColorDict = {}

    for x in range(maze.width):
        for y in range(maze.height):
            if maze.is_floor(x, y):
                mazeColorDict[(x, y)] = random.choice(colorSpace)
    return mazeColorDict


# used to animate robot to show HMM vs real path
def move_robot(maze, mazeColorDict, newLoc):
    colorSpace = ['r', 'g', 'b', 'y']  # color options

    # robot gets new location
    maze.robotloc[0] = newLoc[0]
    maze.robotloc[1] = newLoc[1]

    ogCol = mazeColorDict[newLoc]  # actual square color
    otherCol = [x for x in colorSpace if x != ogCol] # others

    # simulates sensor with 0.88 chance of correct color
    sensor = None
    if random.random() < 0.88:
        sensor = ogCol
    elif random.random() < 0.92:
        sensor = otherCol[0]
    elif random.random() < 0.96:
        sensor = otherCol[1]
    elif random.random() <= 1:
        sensor = otherCol[2]

    return maze, ogCol, sensor


# test HMM
def test_HMM(maze, mazeColorDict, path):

    # lists tracking progression through the maze
    locs = [maze]
    og = '0'  # initially no color or sensor
    sensors = '0'

    # reset maze
    ogStartX = maze.robotloc[0]
    ogStartY = maze.robotloc[1]

    # update path tracking
    for loc in path:
        maze, ogCol, senseCol = move_robot(maze, mazeColorDict, loc)
        locs.append(str(maze))
        og += ogCol
        sensors += senseCol

    # reset maze
    maze.robotloc[0] = ogStartX
    maze.robotloc[1] = ogStartY

    # create HMM object
    hmm = HMM(maze, sensors[1:], mazeColorDict)


    start1 = time() # time used to show difference between filtering and distribution
    distribPath = hmm.computeDistrib()  # filtering only
    filterTime = time() - start1
    start2 = time()
    smoothPath = hmm.distribSmoothing()  # forward-backward smoothing
    smoothTime = time() - start2

    # prints maze, readings, colors, distributions
    
    for i, distrib in enumerate(distribPath):
        print('\ntime ' + str(i) + ' -----------')
        print('square color: ' + og[i])  # compare sensor and actual
        print('sensor color: ' + sensors[i])
        print('\nrobot location:')
        print(locs[i])  # actual location (ground truth)
        print('distribution:')
        print(distrib)  # based on filtering
        print('\nsmoothed distribution:')
        print(smoothPath[i])  # based on forward-backward smoothing
    
    print("\n---------Time Analysis---------")
    print("Total time for filtering only: " + str(filterTime))
    print("Total time for forward-backward smoothing: " + str(smoothTime))




# random seed for testing
random.seed(1)

## maze to test on
#maze = Maze('test_maze.maz')
## dictionary of colors of floor spaces
#mazeColorDict = randColors(maze)
## path taken by the robot
#path = [(0,1),(0,2), (1,2), (1,3)]
#test_HMM(maze, mazeColorDict, path)

# maze to test on
maze = Maze('maze1.maz')
# dictionary of colors of floor spaces
mazeColorDict = randColors(maze)
# path taken by the robot
path = [(1,0),(1,1), (1,2), (2,2), (1,2), (1,3)]
test_HMM(maze, mazeColorDict, path)

## maze to test on
#maze = Maze('maze2.maz')
## dictionary of colors of floor spaces
#mazeColorDict = randColors(maze)
## path taken by the robot
#path = [(1,0),(1,1), (2,1), (2,2), (3,2), (3,3)]
#test_HMM(maze, mazeColorDict, path)



