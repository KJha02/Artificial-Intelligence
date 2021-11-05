# COSC76, 2021 Fall Term, PA2, Kunal Jha

## How to Run this Code

### Multi-Agent Mazeworld

To run the multi-agent maze world problem, open *test_mazeworld.py* in your Python editor of choice. From there, you will see a **test(maze, goalLocations)** function. The *maze* parameter takes in the filename of the maze you'd like to load, inputted as a string. Make sure the maze you are loading is within the same folder as *test_mazeworld.py*. The *goalLocations* parameter is a single tuple representing all of the goal coordinates for as many robots are on the maze. It's important that you format your goal locations as follows:

*(goalX1, goalY1, goalX2, goalY2, ... , goalXn, goalYn)*

That is, input one contiguous tuple and NOT a tuple of tuples.

Once you make a call to the **test** function, the program will conduct A* search using the manhattan heuristic, and animate the results. If you'd like to change the heuristic, simply go to line 35 and replace

```
result = astar_search(problem, problem.manhattan_heuristic)
```

with

```
result = astar_search(problem, YOUR_HEURISTIC_HERE)
```

Null heuristic has been provided as a function called **null_heuristic** If you'd like to see the results of the test cases mentioned in the results, simply uncomment lines 41-45.

### Sensorless-Problem

The sensor-less problem is implemented similar to the multi-agent problem. Open the file *test_sensorless.py* in your Python editor of choice. From there, make a call to the function **driver(maze)**. Once again, the *maze* parameter takes in the filename of the maze you'd like to load, inputted as a string. Make sure the maze you are loading is within the same folder as *test_sensorless.py*.

Once you make a call to **driver** the program will output a solution to your sensor-less problem if one exists using the length of the state as a heuristic. If you'd like to change this, simply replace line 33 from

```
result = testAStar(problem, problem.heuristic)
```

to

```
result = testAStar(problem, YOUR_HEURISTIC_HERE)
```

Null heuristic has been provided as a function called **null_heuristic**. If you'd like to see the results of the test cases mentioned in the results, simply uncomment lines 37-41.
