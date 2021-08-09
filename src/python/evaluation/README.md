# Hyperstyle evaluation

This tool allows running the `Hyperstyle` tool on a `xlsx` or `csv` table to get code quality for all code fragments. 
Please, note that your input file should consist of at least 2 obligatory columns to run the tool on its code fragments:

- `code`
- `lang`

Possible values for column `lang` are: `python3`, `kotlin`, `java8`, `java11`.

Output file is a new `xlsx` or `csv` file with the all columns from the input file and two additional ones:
- `grade`
- `traceback` (optional)

Grade assessment is conducted by [`run_tool.py`](https://github.com/hyperskill/hyperstyle/blob/main/README.md) with default arguments. 
  Avaliable values for column  `grade` are: BAD, MODERATE, GOOD, EXCELLENT. 
  `traceback` column stores full inspectors feedback on each code fragment. 
  More details on enabling traceback column in **Optional Arguments** table.

## Usage

Run the [evaluation_run_tool.py](evaluation_run_tool.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to xlsx-file or csv-file with code samples to inspect.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;f**, **&#8209;&#8209;format**| The output format. Available values: `json`, `text`. The default value is `json` . Use this argument when `traceback` is enabled, otherwise it will not be used.|
|**&#8209;tp**, **&#8209;&#8209;tool&#8209;path**| Path to run-tool. Default is `src/python/review/run_tool.py` .|
|**&#8209;&#8209;traceback**| To include a column with errors traceback into an output file. Default is `False`.|
|**&#8209;ofp**, **&#8209;&#8209;output&#8209;folder&#8209;path**| An explicit folder path to store file with results. Default is a parent directory of a folder with xlsx-file or csv-file sent for inspection. |
|**&#8209;ofn**, **&#8209;&#8209;output&#8209;file&#8209;name**| A name of an output file where evaluation results will be stored. Default is `results.xlsx` or `results.csv`.|
|**&#8209;&#8209;to&#8209;drop&#8209;nan**| If True, empty code fragments will be deleted from df. Default is `False`.|
