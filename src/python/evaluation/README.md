**Usage**

Run the xlsx_run_tool.py with the arguments.

Required arguments:

xlsx_file_path — path to xlsx-file with code samples to inspect.
Please, note that your file should consist of at least 2 obligatory columns:
- **code** 
- **lang** 

Possible values for column **lang** are: python3, kotlin, java8, java11.

Optional arguments:
|Argument | Description|
| --- | --- |
|‑f, ‑‑format| The output format. Available values: `json`, `text`. The default value is json .|
|-tp, --tool_path| Path to run-tool. Default is src/python/review/run_tool.py .|
|--tr, --traceback| If true column with errors traceback is included to an output file. Default is `False`.|
|--ofp, --output_folder_path| An explicit folder path to store file with results. Default is a parent directory of a folder with xlsx-file sent for inspection. |
|--ofn, --output_file_name| A name of an output file where evaluation results will be stored. Default is `results.xlsx`.|