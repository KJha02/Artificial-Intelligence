# Code edited by Kunal Jha, CS76 21F


class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.totalChickens = start_state[0]
        self.totalFoxes = start_state[1]
        self.numBoats = start_state[2]
        self.actionSpace = set([])
        for i in range(-2, 3): # can gain or lose a chicken
            for j in range(-2, 3): # can gain or lose a fox
                for k in [-1, 1]: # can gain or lose a boat
                    action = (i, j ,k) # action is a tuple of how many chickens, foxes, and boats are changed
                    self.actionSpace.add(action)
        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list
        successors = set([])
        for action in self.actionSpace: # for all possible actions
            if self.validAction(state, action): # if it is a valid action
                newState = (state[0] + action [0], state[1] + action[1], state[2] + action[2])
                successors.add(newState) # add the new state to a list
        return successors # return the set of all valid next states
            
        
    def validAction(self, state, action):
        m, c, b = state
        i, j, k = action
        oppM = self.totalChickens - m - i
        oppC = self.totalFoxes - c - j
        if ((c+j) > self.totalFoxes) or ((m+i) > self.totalChickens): return False # don't move people that don't exist 
        if (oppC > self.totalFoxes) or (oppM > self.totalChickens): return False # don't move people that don't exist
        
        if (k == 1): # if the boat is moving right to left
            if (b != 0): return False # the boat should initially be on the right side
            if (i < 0 or j < 0): return False # no one should be moving to the right
            if ((i + j) > 2): return False # no more than two people should be moving
            if ((i + j) < 1): return False # no less than 1 person should be moving
        if (k == -1): # if the boat is moving left to right
            if (b != 1): return False # the boat should initially be on the left side
            if (i > 0 or j > 0): return False # no one should be moving to the left
            if ((i + j) < -2): return False # no more than two people should be moving
            if ((i + j) > -1): return False # no less than 1 person should be moving
        
        if (c+j > 0) and (m+i > 0): # if you have at least one chicken and fox on the left after the action
            if ((c+j) - (m+i) > 0): return False # there shouldn't be more foxes than chickens on the left
        if (oppC > 0) and (oppM > 0): # if you have at least one chicken and fox on the right after the action
            if ((oppC - oppM) > 0): return False # there shouldn't be more foxes than chickens on the right
        
        return True # if you pass all of the above conditions the action is valid

    # I also had a goal test method. You should write one.
    def goalTest(self, state):
        return state == (0,0,0) # if all of the foxes and chickens and boats are on the other side
    
    def __str__(self):
        string =  "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((3, 3, 1))
    print(test_cp.get_successors((3, 3, 1)))
    print(test_cp)
