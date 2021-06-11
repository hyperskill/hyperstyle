# Data preprocessing

This module transforms filtered and labeled dataset into the files that can be used as input
files for [train](src/python/evaluation/qodana/imitation_model/train.py) and 
[evaluation](src/python/evaluation/qodana/imitation_model/evaluation.py) scripts. 

### Step 1

Run [fragment_to_inspections_list.py](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/evaluation/qodana/fragment_to_inspections_list.py) 
script to get `numbered_ids.csv` file in case of working with code-blocks or alternatively run 
[fragment_to_inspections_list_line_by_line.py](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/evaluation/qodana/fragment_to_inspections_list_line_by_line.py) 
script to get `numbered_ids_line_by_line.csv` file.
  
[Detailed instructions](https://github.com/hyperskill/hyperstyle/tree/roberta-model/src/python/evaluation/qodana) 
on how to run following scripts. 

### Step 2

Run [encode_data.py](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/preprocessing/encode_data.py) with the
following arguments:

Required arguments:

`dataset_path` — path to `numbered_ids_line_by_line.csv` file or `numbered_ids.csv` file.

Optional arguments:

Argument | Description
--- | ---
|**&#8209;o**, **&#8209;&#8209;output_file_path**| Path to the directory where output file will be created. If not set, output file will be saved in the parent directory of `dataset_path`.|
|**&#8209;ohe**, **&#8209;&#8209;one_hot_encoding**| If `True` target column will be represented as one-hot-encoded vector. The length of each vector is equal to the unique number of classes in dataset. Default is `True`.|
|**&#8209;c**, **&#8209;&#8209;add_context**| Should be used only when `dataset_path` is a path to `numbered_ids_line_by_line.csv`. If set to `True` each single line will be substituted by a piece of code – the context created from several lines. Default is `False`.|
|**&#8209;n**, **&#8209;&#8209;n_lines_to_add**| A number of lines to append to the target line before and after it. A line is appended only if it matches the same solution. If there are not enough lines in the solution, special token will be appended instead. Default is 2.|


#### Script functionality overview: 
- creates `one-hot-encoding` vectors matches each samples each sample in the dataset **(default)**.
- substitutes `NaN` values in the dataset by `\n` symbol **(default)**.
- transform lines of code into the `context` from several lines of code **(optional)**.

### Step 3

Run [`split_dataset.py`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/preprocessing/split_dataset.py)
with the following arguments:

Required arguments:

`dataset_path` — path to `encoded_dataset.csv` file obtained by running [encode_data.py](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/preprocessing/encode_data.py) script.

Optional arguments:

Argument | Description
--- | ---
|**&#8209;o**, **&#8209;&#8209;output_directory_path**| Path to the directory where folders for train, test and validation datasets with the corresponding files will be created. If not set, folders will be created in the parent directory of `dataset_path`.|
|**&#8209;ts**, **&#8209;&#8209;test_size**| Proportion of test dataset. Available values: 0 < n < 1. Default is 0.2.|
|**&#8209;vs**, **&#8209;&#8209;val_size**| Proportion of validation dataset that will be taken from train dataset. Available values are: 0 < n < 1. Default is 0.3.|
|**&#8209;sh**, **&#8209;&#8209;shuffle**| If `True` data will be shuffled before split. Default is `True`.|
