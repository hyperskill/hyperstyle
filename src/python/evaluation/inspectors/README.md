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
- [print_inspectors_statistics.py](print_inspectors_statistics.py) allows printing statistics 
  that were found by [diffs_between_df.py](diffs_between_df.py)
- [get_worse_public_examples.py](get_worse_public_examples.py) allows getting 
  top N worse public examples from a dataset. The measure is to count unique new inspections.

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

___

### Print statistics

[print_inspectors_statistics.py](print_inspectors_statistics.py) allows print statistics 
  that were calculated by [diffs_between_df.py](diffs_between_df.py)

#### Usage

Run the [print_inspectors_statistics.py](print_inspectors_statistics.py) with the arguments from command line.

Required arguments:

- `diffs_file_path` — path to a `pickle` file, that was calculated by [diffs_between_df.py](diffs_between_df.py).

Optional arguments:
Argument | Description
--- | ---
|**&#8209;&#8209;categorize**| If True, statistics will be categorized by several categories. By default is disabled.|
|**&#8209;n**, **&#8209;&#8209;top_n**| The top N items will be printed. Default value is 10.|
|**&#8209;&#8209;full_stat**| If True, full statistics (with all issues) will be printed. By default is disabled.|

The statistics will be printed into console.

The output contains:
- was found incorrect grades or not;
- how many fragments has additional issues;
- how many unique issues was found;
- top N issues in the format: (issue_key, frequency);
- short categorized statistics: for each category how many issues were found and how many 
  fragments have these issues;
- \[Optional\] full categorized statistics: for each category for each issue how many 
  fragments have this issue

An example of the printed statistics (without full categorized statistics):

```json
SUCCESS! Was not found incorrect grades.
______
39830 fragments has additional issues
139 unique issues was found
______
Top 10 issues:
SC200: 64435 times
WPS432: 17477 times
WPS221: 10618 times
WPS336: 4965 times
H601: 3826 times
SC100: 2719 times
WPS319: 2655 times
WPS317: 2575 times
WPS515: 1783 times
WPS503: 1611 times
______
CODE_STYLE: 28 issues, 26171 fragments
BEST_PRACTICES: 76 issues, 88040 fragments
ERROR_PRONE: 17 issues, 2363 fragments
COMPLEXITY: 17 issues, 13928 fragments
COHESION: 1 issues, 3826 fragments
______
```

---

### Get worse public examples

[get_worse_public_examples.py](get_worse_public_examples.py) allows getting 
  top N worse public examples from a dataset. The measure is to count unique new inspections.

#### Usage

Run the [get_worse_public_examples.py](get_worse_public_examples.py) with the arguments from command line.

Required arguments:

- `solutions_file_path` — path to xlsx-file or csv-file with graded code samples;
- `diffs_file_path` — path to a `pickle` file, that was calculated by [diffs_between_df.py](diffs_between_df.py).

Please, note that your `solutions_file_path` file with code fragments should consist of at least 2 obligatory columns:

- `code`,
- `traceback`,
- `is_public`,
- `id`.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;n**, **&#8209;&#8209;n**| The N worse fragments will be saved.|

The resulting file will be stored in the same folder as the `solutions_file_path` input file.
