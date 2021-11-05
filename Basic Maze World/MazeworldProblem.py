from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.actionSpace = set([(-1,0), (1,0), (0,-1), (0,1)]) # can move left, right, down, or up
        
        
        self.numRobots = len(self.maze.robotloc) // 2
        
        self.start_state = [] # initialize start state
        for i in range(0, len(self.maze.robotloc), 2): # iterate through robot locations
            loc = (self.maze.robotloc[i], self.maze.robotloc[i+1]) 
            self.start_state.append(loc) # add each x, y, pair for robots to the start state as a tuple
        self.start_state = tuple(self.start_state) # convert the list into a tuple because it should be immutable
        
        
        self.goal_locations = [] # initialize goal locations 
        for i in range(0, len(goal_locations), 2): # iterate through goal locations
            goal = (goal_locations[i], goal_locations[i+1]) 
            self.goal_locations.append(goal) # add each x,y goal pair to the goal locations list
        self.goal_locations = tuple(self.goal_locations) # convert the list to a tuple to make sure it's iterable
        
        
        self.currIdx = 0 # used to keep track of current robots
        
    
    def get_successors(self, state): # take in state with multi robots and index of robotX in state
        x, y = state[self.currIdx] # curr robot's x and y
        children = set([])
        
        for actions in self.actionSpace: # for all possible actions (left, right, up, down)
                dx, dy = actions # get change in x and y
                newX = x + dx # get new X
                newY = y + dy # get new Y
                
                # if the newX and newY are on a floor and there is no robot there
                if self.isValid(state, newX, newY): 
                    succState = list(state)
                    succState[self.currIdx] = (newX, newY) # update the state with the new X and Y's
                    children.add(tuple(succState)) # add the updated state to the set of possible next states
        self.currIdx = (self.currIdx + 1) % self.numRobots # making sure index doesn't get past length
                
        return children # if none of the robots can move, there is no solution
    
    
    
    def isValid(self, state, x, y):
        if self.maze.is_floor(x, y): # if the new position is on a floor
            for i in range(len(state)): # iterate through all robots in state
                if state[i] == (x,y) and i != self.currIdx: # check that there are no robots in the new position and that the current robot is not being compared
                    return False
            return True # otherwise it's valid
        return False # if it's not on the floor at all it's invalid
    
    
    def manhattan_heuristic(self, state):
        manhattanDistance = 0
        for i in range(len(state)):
            goalX, goalY = self.goal_locations[i]
            currX, currY = state[i]
            
            manhattanDistance += abs(goalX - currX) + abs(goalY - currY)
        return manhattanDistance
            
                            
            
    
    def goalTest(self, state):
        return state == self.goal_locations
        

    def __str__(self):
        string =  "Mazeworld problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            stateTuple = []
            for loc in state:
                x, y = loc
                stateTuple.append(x)
                stateTuple.append(y)
            self.maze.robotloc = tuple(stateTuple)
            sleep(1)

            print(str(self.maze))


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_maze3)
    
    print(test_mp.start_state)
    print(test_mp.get_successors(test_mp.start_state))
    print(test_mp.get_successors(test_mp.start_state))
