# Dataset label
This script allows you to label a dataset using the found [Qodana](https://github.com/JetBrains/Qodana) inspections.

The dataset must contain at least three columns: `id`, `code` and `lang`, where `id` is a unique solution number, `lang` is the language in which the code is written in the `code` column. The `lang` must belong to one of the following values: `java7`, `java8`, `java9`, `java11`, `python3`, `kotlin`. If `lang` is not equal to any of the values, the row will be skipped.

The dataset must have the format `csv`. The labeled dataset is also in `csv` format, with a new column `inspections` added, which contains a list of all found inspections.

# Usage
Run the [dataset_labeling.py](dataset_labeling.py) with the arguments from command line.

### Required arguments

`dataset_path` — path to dataset.

### Optional arguments
| Argument | Description |
|-|-|
| **&#8209;c**, **&#8209;&#8209;config** | Path to qodana.yaml. If the path is not specified, Qodana will start without a configuration file. |
| **&#8209;l**, **&#8209;&#8209;limit** | Allows you to read only the specified number of first rows from the dataset. If no limit is specified, the whole dataset will be processed. |
| **&#8209;s**, **&#8209;&#8209;chunk&#8209;size** | The number of files that Qodana will process at a time. Default is `5000`. |
| **&#8209;o**, **&#8209;&#8209;output&#8209;path** | The path where the labeled dataset will be saved. If not specified, the original dataset will be overwritten. |
