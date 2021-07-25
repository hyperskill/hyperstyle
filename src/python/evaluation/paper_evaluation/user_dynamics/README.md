# Dynamics of student usage

This module allows getting statistics about students dynamics in code quality issues improvements.

## Usage

Run the [dynamics_gathering.py](dynamics_gathering.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to csv-file with code samples.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;fb**, **&#8209;&#8209;freq-boundary**| The boundary of solutions count for one student to analyze. The default value is 100.|
|**&#8209;n**, **&#8209;&#8209;n**| Top n popular issues in solutions. The default value is 100. |

In the result a file with students issues dynamics will be created.
Also, the top of issues for all students will be printed into the terminal. This statistics has key of issue and frequency for all students.

An example of issues dynamics:
```text
user,traceback
0,"0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,0,0,0,0,2,0,4,0,6,3,0,3,0,0,0,1,1,0,0,0,1,0,0,0,2,0,0,0,0,0,0,4,0,0,0,1,6,0,1,0,1,3,0,0,1,1,0,0,0,0,0,3,6,1,0,0,0,0,0,0,0,4,1,0,0,1,0,8,0,2,8,0,0,0,0,1,1,1,1,3,7,23,0,9"
1,"0,0,0,3,0,0,2,1,0,0,0,0,4,1,0,0,1,1,0,0,0,0,0,6,0,1,1,0,8,1,2,1,1,0,0,1,0,4,10,1,1,1,3,0,1,0,0,0,1,0,0,0,0,0,0,2,0,3,0,0,2,2,3,2,0,0,0,1,0,1,1,0,0,1,0,4,6,2,0,0,1,0,0,0,0,2,0,0,0,2,1,2,1,0,1,7,1,0,1,1,0,1,0"
```
Each number in the traceback column is the count of issues in one solution. 
The numbers of issues sorted by timestamps.