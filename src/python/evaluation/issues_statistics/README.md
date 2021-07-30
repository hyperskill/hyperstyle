# Hyperstyle evaluation: statistics

This module allows you to collect and visualize the statistics of the tool.

## Get raw issues
This script allows you to get raw issues (issues that have not yet been processed by the main algorithm) for each fragment from a dataset (`xlsx` or `csv` file). The dataset must have 3 obligatory columns: 
- `id`
- `code`
- `lang`

Possible values for column `lang` are: `python3`, `kotlin`, `javascript`, `java7`, `java8`, `java9`, `java11`, `java15`.

The output file is a new `xlsx` or `csv` file with all columns from the input file and an additional column: `raw_issues`.

### Usage
Run the [get_raw_issues.py](get_raw_issues.py) with the arguments from command line.

**Required arguments:**
- `solutions_file_path` — path to xlsx-file or csv-file with code samples to inspect.

**Optional arguments:**
| Argument | Description |
|----------|-------------|
| **&#8209;&#8209;allow&#8209;duplicates** | Allow duplicate issues found by different linters. By default, duplicates are skipped. |
| **&#8209;&#8209;allow&#8209;zero&#8209;measure&#8209;issues** | Allow issues with zero measure. By default, such issues are skipped. |
| **&#8209;&#8209;allow&#8209;info&#8209;issues** | Allow issues from the INFO category. By default, such issues are skipped. |
| **&#8209;&#8209;to&#8209;save&#8209;path** | Allows to save the path to the file where the issue was found. By default, the path is not saved. |
| **&#8209;o**, **&#8209;&#8209;output** | Path where the dataset with raw issues will be saved. If not specified, the dataset will be saved next to the original one. |
| **&#8209;l**, **&#8209;&#8209;log-output** | Path where logs will be stored. If not specified, then logs will be output to stderr. |

## Get raw issues statistics
The script takes the dataframe obtained after executing [get_raw_issues.py](get_raw_issues.py) and outputs dataframes with statistics grouped by language.

The input dataset must have 3 obligatory columns: 
- `id`
- `code`
- `lang`
- `raw_issues`

Possible values for column `lang` are: `python3`, `kotlin`, `javascript`, `java7`, `java8`, `java9`, `java11`, `java15`.

The output files is a new `xlsx` or `csv` files which contains the `value` column and the columns responsible for its category statistics.

The `value` column shows the metric value (for measurable issue categories), quantity (for quantitative issue categories) or `ratio * 100` (for `CODE_STYLE` and `LINE_LEN`), where `ratio` is calculated as in the corresponding rules (`CodeStyleRule` and `LineLengthRule`). 

The table cells indicate how often value occurs in one fragment (for quantitative categories) or in all fragments (for measurable categories).

All output datasets are arranged in folders according to language.

### Usage
Run the [get_raw_issues_statistics.py](get_raw_issues_statistics.py) with the arguments from command line.

**Required arguments:**
- `solutions_with_raw_issues` — path to an xlsx- or csv-file with code samples and raw issues, which were received with [get_raw_issues.py](get_raw_issues.py).

**Optional arguments:**
| Argument | Description |
|----------|-------------|
| **&#8209;o**, **&#8209;&#8209;output** | Path to the folder where datasets with statistics will be saved. If not specified, the datasets will be saved in the folder next to the original dataset. |
