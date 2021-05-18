# Hyperstyle evaluation: inspectors

This module allows comparing two different versions of `Hyperstyle` tool. 
This module contains _preprocessing_ stage and _analysing_ stage. 
`Preprocessing` stage includes:
- [filter_solutions.py](filter_solutions.py) script, that allows keeping only necessary languages in 
  the `csv` or `xslx` file with student solutions and drop duplicates of code fragments (optional);
- [distribute_grades.py](distribute_grades.py) allows distributing calculated grades and traceback 
  for unique solutions into all solutions.

`Analysing` stage includes:
**TODO**

___

## Preprocessing

### Filter solutions

[filter_solutions.py](filter_solutions.py) script allows keeping only necessary languages in 
  the `csv` or `xslx` file with student solutions and drop duplicates of code fragments (optional).

Please, note that your input file must meet the requirements to [evaluation](./../evaluation_run_tool.py) tool. 
You can find all requirements in the evaluation [README](./../README.md) file.

Output file is a new `xlsx` or `csv` (the same format with the input file) file with the all columns 
from the input file.

#### Usage

Run the [filter_solutions.py](filter_solutions.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to xlsx-file or csv-file with code samples.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;l**, **&#8209;&#8209;languages**| Set of languages to keep in the dataset. Available values: `java7`, `java8`, `java9` `java11`, `python3`, `kotlin`. The default value is set of all languages.|
|**&#8209;&#8209;duplicates**| If True, drop duplicates in the "code" column. By default is disabled.|

The resulting file will be stored in the same folder as the input file.

___

### Distribute grades

[distribute_grades.py](distribute_grades.py) allows distributing calculated grades and traceback 
  for unique solutions into all solutions.

Please, note that your input file with all code fragments should consist of at least 1 obligatory columns:

- `code`.

Please, note that your input file with unique code fragments should consist of at least 2 obligatory columns:

- `code`,
- `grade`,
- `traceback` (optional),

and must have all fragments from the input file with all code fragments

Output file is a new `xlsx` or `csv` (the same format with the input files) file with the all columns 
from the input file with unique solutions.

#### Usage

Run the [distribute_grades.py](distribute_grades.py) with the arguments from command line.

Required arguments:

- `solutions_file_path_all` — path to xlsx-file or csv-file with all code samples,
- `solutions_file_path_uniq` — path to xlsx-file or csv-file with unique code samples,

The resulting file will be stored in the same folder as the input file with all samples.

___
