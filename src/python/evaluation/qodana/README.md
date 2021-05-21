# Dataset label

[This](dataset_marking.py) script allows you to mark up a dataset using the found [Qodana](https://github.com/JetBrains/Qodana) inspections.

The dataset must contain at least three columns: `id`, `code` and `lang`, where `id` is a unique solution number, `lang` is the language in which the code is written in the `code` column. The `lang` must belong to one of the following values: `java7`, `java8`, `java9`, `java11`, `python3`, `kotlin`. If `lang` is not equal to any of the values, the row will be skipped.

The dataset must have the format `csv`. The marked dataset is also in `csv` format, with a new column `inpection_ids` added, which contains a list of id's of all found inspections. The table with found inspections, consists of two columns: `id` and `inspection`, and is also in `csv` format.

# Usage
Run the [dataset_marking.py](dataset_marking.py) with the arguments from command line.

### Required arguments

`dataset_path` — path to dataset.

`inspections_output_path` — path where id of all found inspections will be saved.

### Optional arguments
| Argument | Description |
|-|-|
| **&#8209;c**, **&#8209;&#8209;config** | Path to qodana.yaml. If the path is not specified, Qodana will start without a configuration file|
| **&#8209;l**, **&#8209;&#8209;limit** | Allows you to read only the specified number of first rows from the dataset. If no limit is specified, the whole dataset will be processed. |
| **&#8209;s**, **&#8209;&#8209;chunk&#8209;size** | The number of files that Qodana will process at a time. Default is `5000`. |
| **&#8209;o**, **&#8209;&#8209;dataset&#8209;output&#8209;path** | The path where the marked dataset will be saved. If not specified, the original dataset will be overwritten. |

---

# Postprocessing

The model that imitates Qodana analysis gets input from a dataset in a special format. 
This module allows preparing datasets that were graded by [dataset_marking.py](dataset_marking.py) script.

Data processing consists of several stages:
- union several `csv` files that were graded by [dataset_marking.py](dataset_marking.py) script 
  and filter inspections list if it is necessary;
- get all unique inspections from the dataset;
- convert `csv` file into a special format.

## Filter inspections

This stage allow you to union several `csv` files that were graded by [dataset_marking.py](dataset_marking.py) script 
  and filter inspections list if it is necessary.

Please, note that your all input files must be graded by [dataset_marking.py](dataset_marking.py) script 
and have `inspections` column.

Output file is a new `csv` file with the all columns from the input files.

#### Usage

Run the [filter_inspections.py](filter_inspections.py) with the arguments from command line.

Required arguments:

`dataset_folder` — path to a folder with csv files graded by Qodana. Each file must have `inspections` column.

Optional arguments:
Argument | Description
--- | ---
|**&#8209;i**, **&#8209;&#8209;inspections**| Set of inspections ids to exclude from the dataset separated by comma. By default all inspections remain. |

The resulting file will be stored in the `dataset_folder`.

___

## Get all unique inspections

This stage allow you to get all unique inspections from a `csv` file graded by Qodana. 
Please, note that your input file must be graded by [dataset_marking.py](dataset_marking.py) script 
and has `inspections` column.

Output file is a new `csv` file with two columns: `id` and `inspection_id`. 
`id` is unique number for each inspection, minimal value is 1.
`inspection_id` is unique Qoadana id for each inspection.

#### Usage

Run the [get_unique_inspectors.py](get_unique_inspectors.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to csv-file with code samples graded by [dataset_marking.py](dataset_marking.py) script.

The resulting file will be stored in the same folder as the input file.
