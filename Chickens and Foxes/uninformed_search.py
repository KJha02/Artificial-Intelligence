# Code edited by Kunal Jha, CS76 21F


from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.parent = parent 
        self.state = state

# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def bfs_search(search_problem):
    frontier = deque([]) # initialize frontier
    start = SearchNode(search_problem.start_state) # pack start state into node    
    frontier.append(start) # add start node to frontier
    visited = set([]) # keeping track of which states have been visited
    res = SearchSolution(search_problem, "BFS") # the solution to the problem
    
    
    while len(frontier) > 0: # while the frontier is not empty
        currNode = frontier.popleft() # get the current node from the frontier
        currState = currNode.state # get the current state from current node
        
        if currState not in visited: # if the current state hasn't been visited
            visited.add(currState) # marking the current state as visited
            res.nodes_visited += 1 # increase the count of nodes visited
            
            
            if search_problem.goalTest(currState): # if the current state is the goal
                res.path = backchain(currNode) # backchain
                return res # return the solution
            
            for child in search_problem.get_successors(currState): # for the successors of the current state
                childNode = SearchNode(child, currNode) # pack the child into a node with a pointer to the current node
                frontier.append(childNode) # add the child node to the frontier
    return res

def backchain(currentNode):
    chain = deque([])
    while currentNode.parent != None:
        chain.appendleft(currentNode.state)
        currentNode = currentNode.parent

    return chain

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # you write this part
    # this nested function either returns None if there is no solution or the solution if there is one    
    def dfs(search_problem, depth_limit=100, node=None, solution=None):
        # base case
        if search_problem.goalTest(node.state): # if the node is the goal 
            solution.path = backchain(node) # backchain and overwrite to determine the path
            return solution # return the solution
        if depth_limit == 0:
            res = SearchSolution(search_problem, solution.search_method)
            res.nodes_visited = solution.nodes_visited
            return res
        
        # recursive case
        for child in search_problem.get_successors(node.state): # for all of the children
            if child not in solution.path: # if a child is not in the current solution path
                solution.nodes_visited += 1 # increase the number of nodes visited by one
                temp = solution # create a copy of the solution
                temp.path.append(child) # add the child to the current potential solution
                
                childNode = SearchNode(child, node) # pack the child into a node
                
                temp = dfs(search_problem, depth_limit-1, childNode, temp) # recurse with dfs
                
                if temp != None: # return the solution if found
                    return temp
        return None # if none of the children have a solution return none

    final = dfs(search_problem, depth_limit, node, solution) # call the nested function
    if final == None: # if there is no solution
        final = SearchSolution(search_problem, solution.search_method) # the final answer becomes the default
        final.nodes_visited = solution.nodes_visited # the number of nodes explored is updated
    return final # return the final answer as a SearchSolution object
                
    

def ids_search(search_problem, depth_limit=100):
    # you write this part
    i = 0 # start at depth 0
    
    solution = SearchSolution(search_problem, "IDS") # initialize the solution
    node = SearchNode(search_problem.start_state) # initialize the node
    
    while i < depth_limit: # while the current depth is less than the maximum depth
        solution = dfs_search(search_problem, i, node,solution) # run dfs on the current depth
        if len(solution.path) == 0: # if there is no solution
            i += 1 # increase the current depth by 1 and continue
        else: # if a solution is found
            return solution # return the solution
    return solution # return the failed solution with the number of nodes visited
