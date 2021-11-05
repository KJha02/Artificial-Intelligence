from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
        
    def __init__(self, maze):
        self.maze = maze
        self.actionSpace = set([(-1,0), (1,0), (0,-1), (0,1)])
        self.actionToWord = {(-1,0):"west", (1,0):"east", (0,-1):"south", (0,1):"north"}
        
        self.start_state = []
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                if self.maze.is_floor(i, j):
                    self.start_state.append((i,j)) # initially add every possible legal location to the board
        self.start_state = tuple(self.start_state)
        
    
    
    def get_successors(self, state):
        children = set([]) # the set of all sets containing next possible states
        
        for actions in self.actionSpace: # iterate over all of the actions
            dx, dy = actions 
            nextStates = set([])
            for s in state:
                x, y = s
                newX, newY = x + dx, y + dy # determine what the next x and y will be
                
                if self.maze.is_floor(newX, newY): # if it is a legal action
                    nextStates.add((newX, newY)) # add that legal action to the set of next possible states
                else: # if it hit a wall
                    nextStates.add(s) # add the same position to the set of next states
            children.add(tuple(nextStates)) # add all possible states given an action
        return tuple(children)
    
    
    def goalTest(self, state):
        return len(state) == 1
    
            
    
    def statesToPath(self, state, nextState):
        for actions in self.actionSpace: # iterate over all actions
            dx, dy = actions
            temp = set([]) # initialize the set of possible next states
            for s in state:
                x, y = s
                newX, newY = x + dx, y + dy # determine what the next x and y will be
                
                if self.maze.is_floor(newX, newY): # if it is a legal action
                    temp.add((newX, newY)) # add that legal action to the set of next possible states
                else: # if it hit a wall
                    temp.add(s) # add the same position to the set of next states
            if tuple(temp) == nextState:
                return self.actionToWord[(dx,dy)]
    
    def backchainToPath(self, backchain):
        path = []
        for i in range(len(backchain) -1):
            path.append(self.statesToPath(backchain[i], backchain[i+1]))
        return path
            
            

    def heuristic(self, state):
        return len(state) - 1

    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = []
            for states in state:
                if len(states) == 2:
                    self.maze.robotloc.append(states[0])
                    self.maze.robotloc.append(states[1])
            self.maze.robotloc = tuple(self.maze.robotloc)
            sleep(1)

            print(str(self.maze))
