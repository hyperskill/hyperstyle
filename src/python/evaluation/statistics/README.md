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
| **&#8209;&#8209;allow&#8209;info&#8209;issues** | Allows to save the path to the file where the issue was found. By default, the path is not saved. |
| **&#8209;&#8209;to&#8209;save&#8209;path** | Allows to save the path to the file where the issue was found. By default, the path is not saved. |
| **&#8209;o**, **&#8209;&#8209;output** | Path where the dataset with raw issues will be saved. If not specified, the dataset will be saved next to the original one. |
| **&#8209;l**, **&#8209;&#8209;log-output** | Path where logs will be stored. If not specified, then logs will be output to stderr. |
