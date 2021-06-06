import argparse

import torch
from src.python.evaluation.qodana.imitation_model.common.util import DatasetColumnArgument, ModelCommonArguments
from transformers import Trainer, TrainingArguments


class MultilabelTrainer(Trainer):
    """ By default RobertaForSequence classification does not support
        multi-label classification.

        Target and logits tensors should be represented as torch.FloatTensor of shape (1,).
        https://huggingface.co/transformers/model_doc/roberta.html#transformers.RobertaForSequenceClassification

        To fine-tune the model for the multi-label classification task we can simply modify the trainer by
        changing its loss function. https://huggingface.co/transformers/main_classes/trainer.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop(DatasetColumnArgument.LABELS.value)
        outputs = model(**inputs)
        logits = outputs.logits
        loss_bce = torch.nn.BCEWithLogitsLoss()
        loss = loss_bce(logits.view(-1, self.model.config.num_labels),
                        labels.float().view(-1, self.model.config.num_labels))

        return (loss, outputs) if return_outputs else loss


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('train_dataset_path',
                        type=str,
                        help='Path to the train dataset.')

    parser.add_argument('val_dataset_path',
                        type=str,
                        help='Path to the dataset received by either')

    parser.add_argument('-wp', '--trained_weights_directory_path',
                        default=None,
                        type=str,
                        help='Path to the directory where to save imitation_model weights. Default is the directory'
                             'where train dataset is.')

    parser.add_argument(ModelCommonArguments.CONTEXT_LENGTH.value.short_name,
                        ModelCommonArguments.CONTEXT_LENGTH.value.long_name,
                        type=int,
                        default=40,
                        help=ModelCommonArguments.CONTEXT_LENGTH.value.description)

    parser.add_argument(ModelCommonArguments.BATCH_SIZE.value.short_name,
                        ModelCommonArguments.BATCH_SIZE.value.long_name,
                        type=int,
                        default=16,
                        help=ModelCommonArguments.BATCH_SIZE.value.description)

    parser.add_argument(ModelCommonArguments.THRESHOLD.value.short_name,
                        ModelCommonArguments.THRESHOLD.value.long_name,
                        type=float,
                        default=0.5,
                        help=ModelCommonArguments.THRESHOLD.value.description)

    parser.add_argument('-lr', '--learning_rate',
                        type=int,
                        default=2e-5,
                        help='Learning rate.')

    parser.add_argument('-wd', '--weight_decay',
                        type=int,
                        default=0.01,
                        help='Wight decay parameter for optimizer.')

    parser.add_argument('-e', '--epoch',
                        type=int,
                        default=1,
                        help='Number of epochs to train imitation_model.')

    parser.add_argument('-ws', '--warm_up_steps',
                        type=int,
                        default=300,
                        help='Number of steps used for a linear warmup, default is 300.')

    parser.add_argument('-sl', '--save_limit',
                        type=int,
                        default=1,
                        help='Total amount of checkpoints limit. Default is 1.')


class TrainingArgs:
    def __init__(self, args):
        self.args = args

    def get_training_args(self, val_steps_to_be_made):
        return TrainingArguments(num_train_epochs=self.args.epoch,
                                 per_device_train_batch_size=self.args.batch_size,
                                 per_device_eval_batch_size=self.args.batch_size,
                                 learning_rate=self.args.learning_rate,
                                 warmup_steps=self.args.warm_up_steps,
                                 weight_decay=self.args.weight_decay,
                                 save_total_limit=self.args.save_limit,
                                 output_dir=self.args.trained_weights_directory_path,
                                 overwrite_output_dir=True,
                                 load_best_model_at_end=True,
                                 greater_is_better=True,
                                 save_steps=val_steps_to_be_made,
                                 eval_steps=val_steps_to_be_made,
                                 logging_steps=val_steps_to_be_made,
                                 evaluation_strategy=DatasetColumnArgument.STEPS.value,
                                 logging_strategy=DatasetColumnArgument.STEPS.value,
                                 seed=DatasetColumnArgument.SEED.value,
                                 report_to=[DatasetColumnArgument.WANDB.value])
