import chess
from math import inf

class AlphaBetaAI:
    def __init__(self, depth):
        self.depth_limit = depth
        self.states_visited = 0
        self.transposeTable = {} 

    def choose_move(self, board):
        temp = board
        choice = self.deepening(temp)
        return choice
        
    
    
    def cutoff_test(self, board, depth, currMax):
        if board.is_checkmate(): # if a king is captured
            return True
        elif board.is_stalemate(): # if the game is a draw
            return True
        elif depth >= currMax: # if you are past the depth limit
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
    
    def AlphaBeta(self, board, depth, alpha, beta, currMax):
        self.states_visited += 1
        # base case
        if hash(str(board)) in self.transposeTable:
            temp = self.transposeTable[hash(str(board))]
            if (self.depth_limit - depth) <= temp[1]:
                return temp[0]
        elif self.cutoff_test(board, depth, currMax):
            return self.Utility(board)
                
        depth += 1
        
        # recursive case
        if board.turn == chess.WHITE:
            v = float("-inf")
            for moves in self.sortBoard(board): # sorted leaves
                board.push(moves)
                v = max(v, self.AlphaBeta(board, depth, alpha, beta, currMax)) # the max value of the recursive version
                alpha = max(alpha, v) # alpha is the max of value and alpha
                board.pop()
                if beta <= alpha: # condition to prune
                    break
            self.transposeTable[hash(str(board))] = [v, self.depth_limit-depth] # store the max value of the board
            return alpha
        else:
            v = float("inf")
            for moves in self.sortBoard(board): # sorted leaves
                board.push(moves)
                v = min(v, self.AlphaBeta(board, depth, alpha, beta, currMax)) # minimizing player has to minimize recursion
                beta = min(beta, v) # beta is the min of value and beta
                board.pop()
                if beta <= alpha: # condition for pruning
                    break
            self.transposeTable[hash(str(board))] = [v, self.depth_limit-depth] # store the min value of the board and the depth
            return beta
                
        
        
    def noDeepening(self, board):
        currMax = self.depth_limit
        largestV = float("-inf")
        bestMove = list(board.legal_moves)[0]
    
        self.states_visited = 0
        for moves in self.sortBoard(board):
            board.push(moves)
            currV = self.AlphaBeta(board, 0, float("-inf"), float("inf"), currMax) # determine value of an action
            if currV > largestV:
                largestV = currV # store the maximum value
                bestMove = moves # update best move
            board.pop()
        return bestMove # return the best move
    
    def deepening(self, board):
        currMax = 0
        largestV = float("-inf")
        bestMove = list(board.legal_moves)[0]
        temp = board
        while currMax < self.depth_limit: # the depth will increment each loop
            self.states_visited = 0 # reset states visited
            print("best move: ", str(bestMove))
            print("score: ", largestV)
            board = temp 
            testLegal = self.sortBoard(board)
            for moves in testLegal: # same as no deepening
                board.push(moves)
                currV = self.AlphaBeta(board, 0, float("-inf"), float("inf"), currMax)
                if currV > largestV:
                    largestV = currV
                    bestMove = moves
                if largestV == float("inf"):
                    print("depth: ", currMax)
                    return bestMove
                board.pop()
            currMax += 1
        
        print("depth: ", currMax)
        return bestMove # return best move
    
    def sortBoard(self, board):
        boardList = list(board.legal_moves)
        moveValue = {}
        for moves in board.legal_moves: # iterate through moves
            board.push(moves)
            moveValue[moves] = self.Utility(board) # determine utility
            board.pop()
        def comparator(move):
            return moveValue[move] # lower utility values are placed earlier
        boardList.sort(reverse=True, key=comparator) # going from greatest to least
        return boardList # sorted list of legal moves
        
        
        

    
    # This function gives the point weighting of a board
    def evaluateMove(self, board):
        whiteP, blackP = len(board.pieces(chess.PAWN, chess.WHITE)), len(board.pieces(chess.PAWN, chess.BLACK))
        whiteN, blackN = len(board.pieces(chess.KNIGHT, chess.WHITE)), len(board.pieces(chess.KNIGHT, chess.BLACK))
        whiteB, blackB = len(board.pieces(chess.BISHOP, chess.WHITE)), len(board.pieces(chess.BISHOP, chess.BLACK))
        whiteQ, blackQ = len(board.pieces(chess.QUEEN, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))
        whiteR, blackR = len(board.pieces(chess.ROOK, chess.WHITE)), len(board.pieces(chess.ROOK, chess.BLACK))
        whiteK, blackK = len(board.pieces(chess.KING, chess.WHITE)), len(board.pieces(chess.KING, chess.BLACK))
        
        return (whiteP - blackP) + 3 * (whiteN - blackN + whiteB- blackB) + 5 * (whiteR - blackR) + 9 * (whiteQ - blackQ) + 200 * (whiteK - blackK)
    
    
        