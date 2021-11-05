from MazeworldProblem import MazeworldProblem
from Maze import Maze

#from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems

#test_maze3 = Maze("maze3.maz")
#print(test_maze3)
#test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
#print(test_mp.start_state)
#print(test_mp.goal_locations)

#print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
#result = astar_search(test_mp, null_heuristic)
#print(result)

# this should do a bit better:
#result = astar_search(test_mp, test_mp.manhattan_heuristic)
#print(result)
#test_mp.animate_path(result.path)

# Your additional tests here:

def test(maze, goalLocations):
    testMaze = Maze(maze)
    problem = MazeworldProblem(testMaze, goalLocations)
    result = astar_search(problem, problem.manhattan_heuristic)
    print(result)
    problem.animate_path(result.path)
    
#test("maze3.maz", (1,4,1,3,1,2))
    
#test("maze4.maz", (1,4,9,4)) # two robots have to make room to get to opposite sides of map
#test("maze5.maz", (2,4,2,3,2,2)) # three robots have to navigate single column
#test("maze6.maz",(119,0)) # large, single agent maze
#test("maze7.maz", (3,2,0,6)) # two agents have to work out of spiral with only one block of leeway
test("maze8.maz", (8,0,1,0)) # two agents have criss-crossing paths to the goal