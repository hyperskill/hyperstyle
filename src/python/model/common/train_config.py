import argparse

import torch
from src.python.model.common.util import MarkingArgument
from src.python.review.common.file_system import Extension
from transformers import Trainer, TrainingArguments


class MultilabelTrainer(Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop(MarkingArgument.LABELS.value)
        outputs = model(**inputs)
        logits = outputs.logits
        loss_bce = torch.nn.BCEWithLogitsLoss()
        loss = loss_bce(logits.view(-1, self.model.config.num_labels),
                        labels.float().view(-1, self.model.config.num_labels))

        return (loss, outputs) if return_outputs else loss


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--train_dataset_path',
                        type=str,
                        help=f'Path to the dataset received by either'
                             f' src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             f'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('--val_dataset_path',
                        type=str,
                        help=f'Path to the dataset received by either'
                             f' src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             f'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('--output_dir',
                        default=None,
                        type=str,
                        help='Path to the directory where to save model weights. Default is the directory'
                             'where train dataset is.')

    parser.add_argument('-bs', '--batch_size',
                        type=int,
                        default=16,
                        help='Batch_size for training, default is 16.')

    parser.add_argument('-lr', '--learning_rate',
                        type=int,
                        default=2e-5,
                        help='Learning rate.')

    parser.add_argument('-w', '--weight_decay',
                        type=int,
                        default=0.01,
                        help='Wight decay parameter for optimizer.')

    parser.add_argument('-e', '--epoch',
                        type=int,
                        default=1,
                        help='Number of epochs to train model.')

    parser.add_argument('-th', '--threshold',
                        type=float,
                        default=0.5,
                        help='Is used while compute f1-score. If the probability of inspection is greater '
                             'than threshold, sample will be classified with the inspection. '
                             'Default is 0.5.')

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
        return TrainingArguments(learning_rate=self.args.learning_rate,
                                 weight_decay=self.args.weight_decay,
                                 num_train_epochs=self.args.epoch,
                                 per_device_train_batch_size=self.args.batch_size,
                                 per_device_eval_batch_size=self.args.batch_size,
                                 save_steps=val_steps_to_be_made,
                                 eval_steps=val_steps_to_be_made,
                                 logging_steps=val_steps_to_be_made,
                                 save_total_limit=self.args.save_limit,
                                 overwrite_output_dir=True,
                                 output_dir=self.args.output_dir,
                                 evaluation_strategy=MarkingArgument.STEPS.value,
                                 logging_strategy=MarkingArgument.STEPS.value,
                                 warmup_steps=self.args.warm_up_steps,
                                 seed=MarkingArgument.SEED.value,
                                 load_best_model_at_end=True,
                                 greater_is_better=True)
