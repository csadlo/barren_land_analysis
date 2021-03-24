# Barren Land Analysis

A program to solve the following problem:

You have a farm of 400m by 600m where coordinates of the field are from (0, 0) to (399, 599). A portion of the farm is barren, and all the barren land is in the form of rectangles. Due to these rectangles of barren land, the remaining area of fertile land is in no particular shape. An area of fertile land is defined as the largest area of land that is not covered by any of the rectangles of barren land. 
Read input from STDIN. Print output to STDOUT 


### Input 
You are given a set of rectangles that contain the barren land. These rectangles are defined in a string, which consists of four integers separated by single spaces, with no additional spaces in the string. The first two integers are the coordinates of the bottom left corner in the given rectangle, and the last two integers are the coordinates of the top right corner. 

### Output 
Output all the fertile land area in square meters, sorted from smallest area to greatest, separated by a space. 

### Sample Data:
Input: {“0 292 399 307”}

Output: 116800  116800


Input: {“48 192 351 207”, “48 392 351 407”, “120 52 135 547”, “260 52 275 547”} 

Output: 22816 192608
 	

## Deployment

Project can be run on any machine that supports Python 3. 

## Getting Started

Simply write a file containing the input lines of barren rectangles and send it to barren_land_analysis.py through STDIN. If the user is on a linux machine and wishes to use a different grid size than the default 399 x 599, they can execute the command 'export OVERRIDE_DEFAULT_GRID_SIZE="1"' first. Then include the desired grid size in the first line of their input file. To undo this change, execute 'unset OVERRIDE_DEFAULT_GRID_SIZE"

### Sample Of Default Grid Size:

Input File (input.txt):
[source]
--
48 192 351 207
48 392 351 407
120 52 135 547
260 52 275 547
--

Command:
cat input.txt | python barren_land_analysis.py

Output:
[source]
--
22816 192608
--


### Sample Of Custom Grid Size:

Input File (input.txt):
[source]
--
99 99
20 60 39 79
60 20 79 39
60 60 79 79
--

Command:
export OVERRIDE_DEFAULT_GRID_SIZE=1
cat input.txt | python barren_land_analysis.py

Output:
[source]
--
8800
--


## Testing

unittest_modules.py contains basic unit test cases for the helper functions (ie. used by algorithms but not algorithmic themselves) that are used by the main program, barren_land_analysis.py.

The bash shell script test_BLA.sh performs all unit testing of the modules and tests barren_land_analysis.py using a many different input sets. Executing all the tests is as simple as:

./test_BLA.sh

at the command line and should take about a minute to complete. Successful execution means that no messages are printed.

