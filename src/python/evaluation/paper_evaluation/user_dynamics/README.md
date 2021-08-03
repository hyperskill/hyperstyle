# Dynamics of student usage

This module allows getting statistics about students dynamics in code quality issues improvements.

## Usage

Run the [dynamics_gathering.py](dynamics_gathering.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to csv-file with code samples.

In the result a file with students issues dynamics will be created. 
We have three categories of dynamics:
- all (count of all code quality issues expect INFO issues)
- formatting (count of formatting code quality issues from CODE_STYLE category)
- other (all issues minus formatting issues)

Each type of dynamics will be saved into a separated folder with csv files for each student.
Each csv file has only two columns: fragment id and issues count.

An example of the csv file:
```text
issue_count,time
2,0
20,1
16,2
15,3
5,4
5,5
```