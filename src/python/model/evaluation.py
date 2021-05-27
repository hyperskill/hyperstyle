import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.model.common.evaluation_config import configure_arguments
from src.python.model.common.util import MarkingArgument
from src.python.model.preprocessing.dataset import SimpleDataset
from src.python.review.common.file_system import Extension
from torch.utils.data import DataLoader
from transformers import RobertaForSequenceClassification


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = Path(args.dataset_path).parent / f'predictions{Extension.CSV.value}'

    df = pd.read_csv(args.dataset_path)
    val_dataset = SimpleDataset(df)
    num_labels = len(val_dataset[0][MarkingArgument.LABELS.value])
    eval_dataloader = DataLoader(val_dataset, batch_size=args.batch_size)
    predictions = np.zeros([len(val_dataset), num_labels], dtype=object)

    model = RobertaForSequenceClassification.from_pretrained(args.model_weights, num_labels=num_labels)
    model.eval()

    start_ind = 0
    for batch in eval_dataloader:
        with torch.no_grad():
            ids = batch[MarkingArgument.INPUT_IDS.value].detach()
            logits = model(input_ids=ids).logits
            logits = logits.sigmoid().detach().numpy()
            batch_predictions = (logits > args.threshold).astype(int)
            predictions[start_ind:start_ind + args.batch_size, :num_labels] = batch_predictions
            start_ind += args.batch_size

    predictions = pd.DataFrame(predictions, dtype=int)
    predicted_true = 0
    df = df.iloc[:, 1:]
    for i in range(num_labels):
        predicted_true += np.sum((
            predictions.iloc[:, i].to_numpy().astype(int) == df.iloc[:, i].to_numpy().astype(int)))
    print(f"Accuracy: {predicted_true / (df.shape[0] * df.shape[1])}")
    write_dataframe_to_csv(args.output_dir, predictions)


if __name__ == '__main__':
    sys.exit(main())
