import argparse
import sys
from pathlib import Path

import torch
from src.python.model.common.metric import Metric
from src.python.model.common.train_config import configure_arguments, MultilabelTrainer, TrainingArgs
from src.python.model.common.util import MarkingArgument
from src.python.model.dataset.dataset import QodanaDataset
from src.python.review.common.file_system import create_directory
from transformers import RobertaForSequenceClassification


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    train_dataset = QodanaDataset(args.train_dataset_path, args.context_length)
    val_dataset = QodanaDataset(args.val_dataset_path, args.context_length)
    train_steps_to_be_made = len(train_dataset) // args.batch_size
    val_steps_to_be_made = train_steps_to_be_made // 5
    print(f'Steps to be made: {train_steps_to_be_made}, validate each {val_steps_to_be_made}th step.')

    num_labels = train_dataset[0][MarkingArgument.LABELS.value].shape[0]
    model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_labels).to(device)

    metrics = Metric(args.threshold)
    if args.output_directory_path is None:
        args.output_directory_path = Path(args.train_dataset_path).parent / MarkingArgument.WEIGHTS.value
        create_directory(args.output_directory_path)

    train_args = TrainingArgs(args)

    trainer = MultilabelTrainer(model=model,
                                args=train_args.get_training_args(val_steps_to_be_made),
                                train_dataset=train_dataset,
                                eval_dataset=val_dataset,
                                compute_metrics=metrics.compute_metric)
    trainer.train()


if __name__ == '__main__':
    sys.exit(main())
