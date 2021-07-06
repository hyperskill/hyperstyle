# Qodana imitation model 
## Description
The general purpose of the model is to simulate the behavior of [`Qodana`](https://github.com/JetBrains/Qodana/tree/main) – 
a code quality monitoring tool that identifies and suggests fixes for bugs, security vulnerabilities, duplications, and imperfections.

Motivation for developing a model:
- acceleration of the code analysis process by training the model to recognize a certain class of errors;
- the ability to run the model on separate files without the need to create a project (for example, for the Java language)


## Architecture 
[`RobertaForSequenceClassification`](https://huggingface.co/transformers/model_doc/roberta.html#robertaforsequenceclassification) model with [`BCEWithLogitsLoss`](https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html) solve multilabel classification task. 

Model outputs is a tensor of size: `batch_size`  x `num_classes`. Where `batch_size` is the number of training examples utilized in one iteration, 
and `num_classes` is the number of error types met in the dataset. By model class here, we mean a unique error type.
Class probabilities are received by taking `sigmoid` and final predictions are computed by comparing the probability of each class with the `threshold`. 

As classes might be unbalanced the used metric is `f1-score`.
## What it does

Model has two use cases:
- It can be trained to predict a unique number of errors in a **block** of code, unfixed length. 
  
**Example**: 

code | inspections
--- | ---
|`import java.util.Scanner; class Main {public static void main(String[] args) {Scanner scanner = new Scanner(System.in);// put your code here int num = scanner.nextInt(); System.out.println((num / 10 ) % 10);}}`| 1, 2|


- It can be trained to predict a unique number of errors in a **line** of code. 

**Example**

code | inspections
--- | ---
|`import java.util.Scanner;`| 0|
|`\n`|0|
|`class Main {`|1|
|`public static void main(String[] args`) {|1|
|`Scanner scanner = new Scanner(System.in);`|0|
|`// put your code here`|0|
|`int num = scanner.nextInt();`|0|
|`System.out.println((num / 10 ) % 10);`|2|
|`}`|0|
|`}`|0|


## Data preprocessing

Please address to the [`following documentation`](src/python/evaluation/qodana) for labeling dataset and to the [`following documentation`](preprocessing) to preprocess data for model training and evaluation afterwards. 

After completing the 3d preprocessing step you should have 3 folders:
`train`, `val`, `test` with `train.csv`, `val.csv` and `test.csv` respectively.

Each file has the same structure, it should consist of 4+ columns:
- `id` – solutions id;
- `code` – line od code or block of code;
- `lang` - language version;
- `0`, `1`, `2` ... `n` – several columns, equal to the unique number of errors detected by Qodana in the dataset.
The values in the columns are binary numbers: `1` if inspection is detected and `0` otherwise.
  

## How to train the model

Run [`train.py`](train.py) script from the command line with the following arguments:

Required arguments:

- `train_dataset_path`  &#8209; path to the `train.csv` – file that consists of samples
that model will use for training.

- `val_dataset_path` &#8209; path to the `val.csv` – file that consists of samples
that model will use for evaluation during training.
  
Both files are received by running [`split_dataset.py`](preprocessing/split_dataset.py) script and has the structure as described above.

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

To inspect the rest of default training parameters please, address to the [`TrainingArguments`](common/train_config.py).

## How to evaluate model

Run [`evaluation.py`](evaluation.py) script from the command line with the following arguments:

Required arguments:

`test_dataset_path` &#8209; path to the `test.csv` received by running [`split_dataset.py`](preprocessing/split_dataset.py) script.

`model_weights_directory_path` &#8209; path to the folder where trained model weights are saved.

Optional arguments:

Argument | Description
--- | ---
|**&#8209;o**, **&#8209;&#8209;output_directory_path**| Path to the directory where labeled dataset will be saved. Default is the `test` folder.|
|**&#8209;c**, **&#8209;&#8209;context_length**| Sequence length or embedding size of tokenized samples. Available values are any `positive integers`. **Default is 40**.|
|**&#8209;sf**, **&#8209;&#8209;save_f1_score**| If enabled report with f1 scores by classes will be saved to the `csv` file in the parent directory of labeled dataset. **Disabled by default**.|
|**&#8209;bs**, **&#8209;&#8209;batch_size**| The number of training examples utilized in one training and validation iteration. Available values are any `positive integers`. **Default is 16**.|
|**&#8209;th**, **&#8209;&#8209;threshold**| Is used to compute predictions. Available values: 0 < `threshold` < 1. If the probability of inspection is greater than `threshold`, sample will be classified with the inspection. **Default is 0.5**.|

Output is a `predictions.csv` file with the column names matches the number of classes. Each sample has a binary label: 

- `0` &#8209; if the model didn't found an error in a sample.

- `1` &#8209; if the error was found in a sample.


## How to use model, pretrained on Java code snippets from Stepik

There are 2 trained models available for the usage and 2 datasets on which models were trained and evaluated. 
Access to the datasets is restricted. 
### Model that uses program text as an input:
- [`train_dataset`](https://drive.google.com/drive/folders/1bdLExLIbY53SVobT0y4Lnz9oeZENqLmt?usp=sharing) – private access;
- [`evaluation_dataset`](https://drive.google.com/file/d/1hZlP7q3gVoIl8vmOur0UFpEyFDYyVZko/view?usp=sharing) – private access;
- [`test_dataset`](https://drive.google.com/file/d/1oappcDcH-p-2LwjdOfZHRSiRB9Vi39mc/view?usp=sharing) – private access;
- [`model_weights`](https://drive.google.com/file/d/1PFVHVd4JDjFUD3b5fDSGXoYBWEDlaEAg/view?usp=sharing) – public access.
  
The model was trained to detect 110 Qodana inspections. The whole
list of inspections can be found via the link [here](https://drive.google.com/file/d/1PVqjx7QEot1dIXyiYP_-dJnWGup2Ef7v/view?usp=sharing). 
   
Evaluation results are:
   
Inspection | Description | F1-Score
--- | --- | ---
|No Errors | No errors from the [list](https://docs.google.com/spreadsheets/d/14BTj_lTTRrGlx-GPTcbMlc8zdt--WXLZHRnegKRrZYM/edit?usp=sharing) were detected by Qodana.| 0.73 |
| Syntax Error |Reports any irrelevant usages of java syntax.| 0.99|
| System Out Error | Reports any usages of System.out or System.err. | 0.99 |
| IO Resources | Reports any I/O resource which is not safely closed. | 0.97 |

The rests of the inspections were not learnt by the model due to the class disbalance. 
### Model that uses a line of program text as an input:
- [`train_dataset`](https://drive.google.com/file/d/1c-kJUV4NKuehCoLiIC3JWrJh3_NgTmvi/view?usp=sharing) – private access;
- [`evaluation_dataset`](https://drive.google.com/file/d/1AVN4Uj4omPEquC3EAL6XviFATkYKcY_2/view?usp=sharing) – private access;
- [`test_dataset`](https://drive.google.com/file/d/1J3gz3wS_l63SI0_OMym8x5pCj7-PCIgG/view?usp=sharing) – private access;
- [`model_weights`](https://drive.google.com/file/d/1fc32-5XyUeOpZ5AkRotqv_3cWksHjat_/view?usp=sharing) – public access.
  
One sample in the dataset consists of one line of program in the context. The context is 2 lines of the same
program before and after the target line. When there are not enough lines before or after target, special
token `NOC` is added.

The model was also trained to detect 110 inspections. The whole
list of inspections can be found via the link [here](https://drive.google.com/file/d/1PVqjx7QEot1dIXyiYP_-dJnWGup2Ef7v/view?usp=sharing). 
   
Evaluation results are:
   
Inspection | Description | F1-score
--- | --- | ---
|No Errors | No errors from the [list](https://docs.google.com/spreadsheets/d/14BTj_lTTRrGlx-GPTcbMlc8zdt--WXLZHRnegKRrZYM/edit?usp=sharing) were detected by Qodana.| 0.99 |
| Syntax Error |Reports any irrelevant usages of java syntax.| 0.23|
| System Out Error | Reports any usages of System.out or System.err.| 0.30 |
| IO Resources | Reports any I/O resource which is not safely closed | 0.23 |

The rests of the inspections were not learnt by the model due to the class disbalance.

To use any of the model follow [`fine-tuning`](https://huggingface.co/transformers/training.html) tutorial from HuggingFace. Unarchive `model weights` zip and use absolute path to the root folder instead of built-in name of pretrained model. 

For example: 

    RobertaForSequenceClassification.from_pretrained(<path to the folder with weights>, 
                                                      num_labels=<unique number of inspections in your dataset>)
