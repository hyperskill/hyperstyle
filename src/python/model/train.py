import argparse
import sys
from pathlib import Path

import pandas as pd
from src.python.model.common.metrics import Metrics
from src.python.model.common.train_config import configure_arguments, MultilabelTrainer, TrainingArgs
from src.python.model.common.util import MarkingArgument, tokenizer
from src.python.model.preprocessing.dataset import SimpleDataset
from src.python.review.common.file_system import create_directory
from transformers import RobertaForSequenceClassification


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    train_dataset = SimpleDataset(pd.read_csv(args.train_dataset_path))
    val_dataset = SimpleDataset(pd.read_csv(args.val_dataset_path))
    train_steps_to_be_made = len(train_dataset) // args.batch_size
    val_steps_to_be_made = train_steps_to_be_made // 5
    print(f'Steps to be made: {train_steps_to_be_made}, validate each '
          f'{val_steps_to_be_made}th step.')

    num_labels = train_dataset[0][MarkingArgument.LABELS.value].shape[0]
    model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_labels)

    metrics = Metrics(args.threshold)
    if args.output_dir is None:
        args.output_dir = Path(args.train_dataset_path).parent / "weights"
        create_directory(args.output_dir)

    train_args = TrainingArgs(args)

    trainer = MultilabelTrainer(model=model,
                                tokenizer=tokenizer,
                                args=train_args.get_training_args(val_steps_to_be_made),
                                train_dataset=train_dataset,
                                eval_dataset=val_dataset,
                                compute_metrics=metrics.compute_metrics)
    trainer.train()


if __name__ == '__main__':
    sys.exit(main())
