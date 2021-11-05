# You write this:
from SensorlessProblem import SensorlessProblem
from Maze import Maze

from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


def testAStar(searchProblem, heuristic):
    result = astar_search(searchProblem, heuristic) # determine shortest path to localize at goal
    searchProblem.animate_path(result.path) # animate path
    result.path = searchProblem.backchainToPath(result.path) # convert states into readible actions
    result.cost = len(result.path) # update cost
    return result # return result with action path instead of state path



#result = testAStar(test_sp, null_heuristic) # deterine the shortest path to localize at the target
#print(result) # printing the path in a readible way

# this should do a bit better:
#result = testAStar(test_sp, test_sp.manhattan_heuristic)
#print(result)



def driver(maze):
    testMaze = Maze(maze)
    problem = SensorlessProblem(testMaze)
    result = testAStar(problem, problem.heuristic)
    print(result)
    

#driver("sensorless1.maz") # no solution in a 6x6 maze
#driver("sensorless2.maz") # convergence with a mixed 7x7 maze
#driver("sensorless3.maz") # convergence with an empty 10x10 maze (no walls)
#driver("sensorless4.maz") # 7x9 maze in an H-shape
driver("sensorless5.maz") # 6x6 zig-zag rows
