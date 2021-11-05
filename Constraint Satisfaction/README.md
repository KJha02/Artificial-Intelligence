# CS76 PA4, Fall 2021, Kunal Jha

To run this code, open the file *CSPDriver.py* in your preferred editor of choice. To run the Map Coloring problem, type 
```
MapDriver(DH=False, MRV=False, LCVEnabled=False, AC3=False)
```
You will notice that each of the parameters are false. DH, MRV, LCVEnabled all represent heuristics for the program, and AC3 represents the inference method. To test the MapDriver with any of these enabled, simply replace the False keyword with True. An example with AC3 and DH enabled would be 
```
MapDriver(DH=True, MRV=False, LCVEnabled=False, AC3=True)
```
From there, simply run the Python file through the standard procedure of your editor, which can typically be done by clicking the "run" button at the top of the screen. 

To run the Circuit problem, you will need to type
```
var = [TUPLES_OF_VARIOUS_(WIDTH,HEIGHT)_PAIRS_HERE]
CircuitDriver(maxWidth=YOUR_MAX_WIDTH_HERE, maxHeight=YOUR_MAX_HEIGHT_HERE, var, DH=False, MRV=False, AC3 = False, LCVEnabled = False)
```
var should be a list of tuples separated by commas, with each tuple representing a different box's height and width. Within the CircuitDriver() line, you should input the maximum width and height of the box at the parameters specified. Similar to the MapDriver function, you should be able to specify what heuristics you want to use by switching the parameters from False to True. One of the sample test cases is below
```
var = [(3,2), (5,2), (2,3), (7,1)]
CircuitDriver(maxWidth=10, maxHeight=3, variables=var, DH=True, MRV=True, AC3 = True, LCVEnabled = False)
```

As a quick implementation note, the backtrack algorithm will prefer the MRV heuristic over the DH one, so toggling both to True is equivalent to making DH=False and MRV=True.