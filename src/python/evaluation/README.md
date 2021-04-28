# Hyperstyle evaluation

This tool allows running the `Hyperstyle` tool on an xlsx table to get code quality for all code fragments. Please, note that your input file should consist of at least 2 obligatory columns to run xlsx-tool on its code fragments:

- `code`
- `lang`

Possible values for column `lang` are: python3, kotlin, java8, java11.

Output file is a new xlsx file with 3 columns:
- `code`
- `lang`
- `grade`
Grade assesesment is condicted by [`run_tool.py`](https://github.com/hyperskill/hyperstyle/blob/main/README.md) with default arguments. Avaliable values for column  `grade` are: BAD, MODERATE, GOOD, EXCELLENT. It is also possible add fourth column: `traceback` to get full inspectors feedback on each code fragment. More details on enabling traceback column in **Optional Arguments** table.

## Usage

Run the xlsx_run_tool.py with the arguments from command line.

Required arguments:

`xlsx_file_path` — path to xlsx-file with code samples to inspect.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;f**, **&#8209;&#8209;format**| The output format. Available values: `json`, `text`. The default value is json . Use this argument when `traceback` is enabled, otherwise it will not be used.|
|**&#8209;tp**, **&#8209;&#8209;tool_path**| Path to run-tool. Default is src/python/review/run_tool.py .|
|**&#8209;tr**, **&#8209;&#8209;traceback**| If true column with errors traceback is included to an output file. Default is `False`.|
|**&#8209;ofp**, **&#8209;&#8209;output_folder_path**| An explicit folder path to store file with results. Default is a parent directory of a folder with xlsx-file sent for inspection. |
|**&#8209;ofn**, **&#8209;&#8209;output_file_name**| A name of an output file where evaluation results will be stored. Default is `results.xlsx`.|
