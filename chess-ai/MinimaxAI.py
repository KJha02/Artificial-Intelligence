import chess
import random

class MinimaxAI():
    def __init__(self, depth):
        self.depth_limit = depth
        self.states_visited = 0
        self.miniMaxCalls = 0
        self.currDepth = 0

    def choose_move(self, board):
        temp = board
        self.miniMaxCalls += 1
        choice = self.minimax(temp)
        print("minimax calls: ", self.miniMaxCalls)
        print("max depth: ", self.depth_limit)
        return choice
        
    
    
    def cutoff_test(self, board, depth, currDepthLimit):
        if board.is_checkmate(): # if a king is captured
            return True
        elif board.is_stalemate(): # if the game is a draw
            return True
        elif depth >= currDepthLimit: # if you are past the depth limit
            return True
        return False # if none of those happened

    
    def Utility(self, board):
        MAX = (board.turn == chess.BLACK) # if it was black's turn it is now white's turn
        value = 0
        
        if board.is_checkmate():
            if MAX: # if it's white turn and there's a checkmate white wins
                value = float('inf')
            else: # if it's blacks turn and there's a checkmate black wins
                value = float('-inf')
        elif board.is_stalemate(): # if it's a stalemate then there's no value
            value = 0
        else: # if it's neither, return a random value
            value = self.evaluateMove(board)
            
        return float(value)
    
    
    def maxValue(self, board, depth, currMax):
        self.states_visited += 1 # increase the number of states visited
        
        if self.cutoff_test(board, depth, currMax): # if reached terminal state
            return self.Utility(board) # return utility
        
        value = float('-inf') # initialize value
        depth += 1 # increase depth
        for move in set(board.legal_moves): # for all legal moves
            board.push(move) # do move
            value = max(value, self.minValue(board, depth, currMax)) # get max value of result
            board.pop() # undo move
        return value # return max value
    
    
    def minValue(self, board, depth, currMax):
        self.states_visited += 1 # increase the number of states visited
        
        if self.cutoff_test(board, depth, currMax): # if reached terminal state
            return self.Utility(board) # return utility
        
        value = float('inf') # initialize value
        depth += 1 # increase depth
        for move in set(board.legal_moves): 
            board.push(move) # do move
            value = min(value, self.maxValue(board, depth, currMax)) # get min value of result
            board.pop() # undo move
        return value # return min value
        
    
    def minimax(self, board):
        currValue = 0
        largestValue = float("-inf")
        legMoves = list(board.legal_moves)
        bestMove = legMoves[0]
        legMoves = set(legMoves)
        currMax = 0
        temp = board # copy original board
        
        
        while currMax < self.depth_limit:
            self.states_visited = 0
            board = temp # reset board
            for moves in legMoves:
                board.push(moves)
                currValue = self.minValue(board, 0, currMax) # find best value for a move
                if currValue > largestValue:
                    largestValue = currValue
                    bestMove = moves # update the best move if you find one
                board.pop()
            currMax += 1
        return bestMove
                
    
    # This function gives the point weighting of a board
    def evaluateMove(self, board):
        whiteP, blackP = len(board.pieces(chess.PAWN, chess.WHITE)), len(board.pieces(chess.PAWN, chess.BLACK))
        whiteN, blackN = len(board.pieces(chess.KNIGHT, chess.WHITE)), len(board.pieces(chess.KNIGHT, chess.BLACK))
        whiteB, blackB = len(board.pieces(chess.BISHOP, chess.WHITE)), len(board.pieces(chess.BISHOP, chess.BLACK))
        whiteQ, blackQ = len(board.pieces(chess.QUEEN, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))
        whiteR, blackR = len(board.pieces(chess.ROOK, chess.WHITE)), len(board.pieces(chess.ROOK, chess.BLACK))
        whiteK, blackK = len(board.pieces(chess.KING, chess.WHITE)), len(board.pieces(chess.KING, chess.BLACK))
        
        return (whiteP - blackP) + 3 * (whiteN - blackN + whiteB- blackB) + 5 * (whiteR - blackR) + 9 * (whiteQ - blackQ) + 200 * (whiteK - blackK)
    
    
        