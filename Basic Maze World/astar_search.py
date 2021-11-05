from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # you write this part
        return self.heuristic + self.transition_cost # the priority is the sum of the heuristic and the cost
        

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = start_node.priority()
    
    

    # you write the rest:
    
    repeats = 0 # this will be used to ensure that the loop doesn't keep repeating if no solutions are found 
    
    while len(pqueue) > 0:
        
        solution.nodes_visited += 1 # increment the number of nodes visited by 1
        curr = heappop(pqueue) # pop the minimum cost action from the queue
        if curr.state in visited_cost and curr.priority() > visited_cost[curr.state]:
            continue
            
        if search_problem.goalTest(curr.state) == True: # if the current state is the goal
            solution.path = backchain(curr) # return the path to the goal
            solution.cost = len(solution.path) # the path cost is the length of the path (not including heuristic)
            return solution
        
        
        else:
            children = search_problem.get_successors(curr.state) # get all of the successors of a state
            
            if len(children) == 0: # if the current robot cannot move
                repeats += 1 # increase the number of times no solutions were found
                if repeats > search_problem.numRobots: # if all robots didn't find a solution
                    break # end the loop
                heappush(pqueue, curr) # repeat the state
                continue # try again with the next robot
            
            repeats = 0 # if a solution is found reset the amount of repeats
            
            
            for succState in children: # for all of the successorStates
                
                # pack each child into a node
                childNode = AstarNode(succState, heuristic_fn(succState), curr, curr.transition_cost+1)
            
                visitCost = childNode.priority() # determining the cost of visiting the node
                
                if childNode.state not in visited_cost: # if the child has not been visited yet
                    visited_cost[childNode.state] = visitCost # mark it as visited with its cost
                    heappush(pqueue, childNode) # add it to the frontier
                    
                elif visitCost < visited_cost[childNode.state]: # if the child has a lower cost than the originally visited node
                        heappush(pqueue, childNode) # add the child to the frontier
                        visited_cost[childNode.state] = visitCost # update the node's cost
                # otherwise don't add it to the frontier
                    
         
    
    return solution # return a solution either has a proper path or has no solution
                
    

                
