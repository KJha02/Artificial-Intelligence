# PA5, Kunal Jha, CS76 2021 Fall

To run this program, open *solve_sudoku.py* in your editor of choice. You will notice on line 18 it says

```
result = sat.walk_sat()
```

This line calls the walk_sat method which solves the the sudoku board. The walk_sat method takes two parameters: p-value and maxFlips. The p value determines the maximum value a random number can be for a random bit to be flipped, and it should be less than or equal to 1 and greater than or equal to 0. It is set to 0.3 by default. The maxFlips determines how many times the walk_sat program can iterate before terminating. It is set to 10000 by default. You can modify both of these parameters by changing line 18 to:

```
result = sat.walk_sat(p=YOUR_VALUE_HERE, maxFlips=YOUR_VALUE_HERE)
```

If you want to test the gsat method, simply comment line 18 and uncomment line 19. You can edit the gsat method similar to walk_sat, by changing line 19 as follows:

```
result = sat.gsat(p=YOUR_VALUE_HERE)
```
gsat only takes a p value as a parameter.

To actually test the code, run the *solve_sudoku.py* file according to the instructions of your preferred editor. You will then be prompted to type in the puzzle you'd like to test the algorithms on. An example of possible puzzles are:
```
puzzle1
puzzle2
rows_and_cols
rows
```
**IMPORTANT**: DO NOT add the *.cnf* extension when prompted with a puzzle. The program automatically accounts for this extension, so adding it manually would cause an error to be thrown.
