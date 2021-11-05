import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        if len(list(board.legal_moves)) > 0:
            
            moves = list(board.legal_moves)
            move = random.choice(moves)
            sleep(1)   # I'm thinking so hard.
            print("Random AI recommending move " + str(move))
            return move
        else:
            return chess.Move.null()
