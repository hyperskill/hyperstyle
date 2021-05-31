# Qodana imitation model 

## Architecture 
`RobertaForSequenceClassification` model with `BCEWithLogitsLoss` solve multilabel classification task. 

Model outputs is a tensor of size: `batch_size` x `num_classes`. Class probabilities are recieved by taking `sigmoid` and final predictions are computed by comparing the probability of each class with the `threshold`. 

As classes might be unbalanced the used metric is `f1-score`.
## What it does

Model has two use cases:
- It can be trained to predict a unique number of errors in a **block** of code, unfixed length. 
- It can be trained to predict a unique number of errors in a **line** of code. 
___
## Data preprocessing

Please address to the [`following documentation`](https://github.com/hyperskill/hyperstyle/tree/roberta-model/src/python/evaluation/qodana) for labeling dataset and to the [`following documentation`](https://github.com/hyperskill/hyperstyle/tree/roberta-model/src/python/model/preprocessing) to preprocess data for model training and evaluation afterwards. 

___

## How to train model

Run [`train.py`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/train.py) script from the command line with the following arguments:

Required arguments:

`train_dataset_path`, `val_dataset_path` &#8209; path to the `train.csv` and `val.csv` dataset received by running [`split_dataset.py`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/preprocessing/split_dataset.py) script.

Optional arguments:

Argument | Description
--- | ---
|**&#8209;o**, **&#8209;&#8209;output_directory_path**| Path to the directory where model weights will be saved. If not set, folder will be created in the `train` folder where `train.csv` dataset is stored.|
|**&#8209;c**, **&#8209;&#8209;context_length**| Sequence length or embedding size of tokenized samples. Available values are any `positive integers`. **Default is 40**.|
|**&#8209;e**, **&#8209;&#8209;epoch**| Number of epochs to train model. **Default is 2**.|
|**&#8209;bs**, **&#8209;&#8209;batch_size**| Batch size for training and validation dataset. Available values are any `positive integers`. **Default is 16**.|
|**&#8209;lr**, **&#8209;&#8209;learning_rate**| Optimizer learning rate. **Default is 2e-5**.|
|**&#8209;w**, **&#8209;&#8209;weight_decay**| Weight decay parameter for an optimizer. **Default is 0.01**.|
|**&#8209;th**, **&#8209;&#8209;threshold**| Is used to compute predictions. Available values: 0 < `threshold` < 1. If the probability of inspection is greater than `threshold`, sample will be classified with the inspection. **Default is 0.5**.|
|**&#8209;ws**, **&#8209;&#8209;warm_up_steps**| A number of steps when optimizer uses constant learning rate before applying scheduler policy. **Default is 300**.|
|**&#8209;sl**, **&#8209;&#8209;save_limit**| Total amount of checkpoints limit. Default is 1.|

To inspect the rest of default training parameters please, address to the [`TrainingArguments`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/common/train_config.py).

## How to evaluate model

Run [`evaluation.py`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/evaluation.py) script from the command line with the following arguments:

Required arguments:

`test_dataset_path` &#8209; path to the `test.csv` received by running [`split_dataset.py`](https://github.com/hyperskill/hyperstyle/blob/roberta-model/src/python/model/preprocessing/split_dataset.py) script.

`model_weights_directory_path` &#8209; path to the folder where trained model weights are saved.
Optional arguments:

Argument | Description
--- | ---
|**&#8209;o**, **&#8209;&#8209;output_directory_path**| Path to the directory where labeled dataset will be saved. Default is the `test` folder.|
|**&#8209;c**, **&#8209;&#8209;context_length**| Sequence length or embedding size of tokenized samples. Available values are any `positive integers`. **Default is 40**.|
|**&#8209;bs**, **&#8209;&#8209;batch_size**| Batch size for training and validation dataset. Available values are any `positive integers`. **Default is 16**.|
|**&#8209;th**, **&#8209;&#8209;threshold**| Is used to compute predictions. Available values: 0 < `threshold` < 1. If the probability of inspection is greater than `threshold`, sample will be classified with the inspection. **Default is 0.5**.|

Output is a `predictions.csv` file with the column names matches the number of classes. Each sample has a binary label: 

- `0` &#8209; if the model didn't found an error in a sample.

- `1` &#8209; if the error was found in a sample.
