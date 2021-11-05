# CS76 PA6, Kunal Jha, Fall 2021

To run this code, open *testMaze.py* in your Python editor of choice. There are three mazes at the bottom of the file you can test the program on. To see *test_maze.maz* in action, uncomment a single *#* symbol from lines 109 to 115. To see *maze1.maz* in action, uncomment a single *#* symbol from lines 117 to 123. To see *maze2.maz* in action, uncomment a single *#* symbol from lines 125 to 131. With all of your selected mazes uncommented, run the program according to the instructions of your editor.

You can make your own mazes to test on as well. They must be 4x4 mazes and follow the format of one of the *.maz* files. You must save your files with the *.maz* extension. Once you have made a maze file, copy the following code format:
```
# maze to test on
maze = Maze('YOUR_FILE_HERE.maz')
# dictionary of colors of floor spaces
mazeColorDict = randColors(maze)
# path taken by the robot
path = [TUPLES OF ROBOT's COORDINATE PATH SEPARATED BY COMMAS]
test_HMM(maze, mazeColorDict, path)
```
From there, you can run your sample maze and the program should try to localize the robot's location.

This code implements both the filtering and smoothing algorithms in parallel and displays the results of both at each timestep, so you do not have to manually toggle this feature. The code also displays the runtime for both methods, and displays this at the end of the program's output.
