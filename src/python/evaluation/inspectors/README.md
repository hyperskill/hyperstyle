# Hyperstyle evaluation: inspectors

This module allows comparing two different versions of `Hyperstyle` tool. 
This module contains _preprocessing_ stage and _analysing_ stage. 
`Preprocessing` stage includes:
- [filter_solutions.py](filter_solutions.py) script, that allows keeping only necessary languages in 
  the `csv` or `xslx` file with student solutions and drop duplicates of code fragments (optional);
- [distribute_grades.py](distribute_grades.py) allows distributing calculated grades and traceback 
  for unique solutions into all solutions.

`Analysing` stage includes:
- [diffs_between_df.py](diffs_between_df.py) allows finding a difference between 
  old and new grades and collect issues that were found in new data

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

and must have all fragments from the input file with all code fragments.

Output file is a new `xlsx` or `csv` (the same format with the input files) file with the all columns 
from the input file with unique solutions.

#### Usage

Run the [distribute_grades.py](distribute_grades.py) with the arguments from command line.

Required arguments:

- `solutions_file_path_all` — path to xlsx-file or csv-file with all code samples,
- `solutions_file_path_uniq` — path to xlsx-file or csv-file with unique code samples,

The resulting file will be stored in the same folder as the input file with all samples.

___

## Analysing

### Find diffs

[diffs_between_df.py](diffs_between_df.py) allows finding a difference between 
  old and new grades and collect issues that were found in new data.

Please, note that your input files should consist of at least 3 obligatory columns:

- `id`,
- `grade`,
- `traceback`.

Output file is a `pickle` file with serialized dictionary with the result. 


#### Usage

Run the [diffs_between_df.py](diffs_between_df.py) with the arguments from command line.

Required arguments:

- `solutions_file_path_old` — path to xlsx-file or csv-file with code samples that was graded by the old version of the tool,
- `solutions_file_path_new` — path to xlsx-file or csv-file with code samples that was graded by the new version of the tool.

The resulting file will be stored in the same folder as the `solutions_file_path_old` input file. 

An example of the pickle` file is:

```json
{
    grade: [2, 3],
    traceback: {
        1: {
            BaseIssue(
                origin_class='C0305',
                description='Trailing newlines',
                line_no=15,
                column_no=1,
                type=IssueType('CODE_STYLE'),
        
                file_path=Path(),
                inspector_type=InspectorType.UNDEFINED,
            ), BaseIssue(
                origin_class='E211',
                description='whitespace before \'(\'',
                line_no=1,
                column_no=6,
                type=IssueType('CODE_STYLE'),
        
                file_path=Path(),
                inspector_type=InspectorType.UNDEFINED,
            ),
          }
    },
}
```
In the `grade` field are stored fragments ids for which grade was increased in the new data.
In the `traceback` field for fragments ids are stored set of issues. These issues were found in the new data and were not found in the old data.