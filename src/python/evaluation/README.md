**Usage**

Run the xlsx_run_tool.py with the arguments.

Required arguments:

xlsx_file_path — path to xlsx-file with code samples to inspect.
Please, note that your file should consist of at least 2 obligatory columns:
- **code** 
- **lang** 

Possible values for column lang: python3, kotlin, java8, java11.

Original arguments:
|Argument | Description|
| --- | --- |
|‑f, ‑‑format| the output format. Available values: json, text. The default value is json .|
|-tool_path, --tool_path| path to run-tool. Default is src/python/review/run_tool.py .|
|--traceback, --traceback| If true column with errors traceback is included to the output file. Default is False.|
|--output_folder_path, --output_folder_path| path to the folder to store file with results. Default is a parent directory of a folder with xlsx-file sent for inspection. |
|--output_file_name, --output_file_name| the name of the output file where evaluation results will be stored. Default is results.xlsx .|