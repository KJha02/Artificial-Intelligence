# Kunal Jha, CS76, Fall 2021, PA3

To run this code, go to either *test_chess.py* or *gui_chess.py*. You can modify the **player1** and **player2** variables to be any of the designed algorithms (MinimaxAI, AlphaBetaAI, HumanPlayer, RandomAI). If you are instantiating a MinimaxAI or AlphaBetaAI object, they take in a maximum depth as a parameter. This value should be a positive integer. The bigger the depth, the longer it will take the algorithm to search for a move. From there, simply run either of the Python files using your editor of choice or the terminal.

In a code demo, it is

```
player1 = YOUR_ALGORITHM_HERE(maxDepth_if_Minimax_or_AlphaBeta)
player2 = YOUR_ALGORITHM_HERE(maxDepth_if_Minimax_or_AlphaBeta)
```

If you'd like to not use iterative deepening for Alpha-Beta search, go to *AlphaBetaAI.py*, and at line 12 change

```
choice = self.deepening(temp)
```
to
```
choice = self.noDeepening(temp)
```
