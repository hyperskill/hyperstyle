import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.model.common.evaluation_config import configure_arguments
from src.python.model.common.metric import Metric
from src.python.model.common.util import MarkingArgument
from src.python.model.dataset.dataset import QodanaDataset
from src.python.review.common.file_system import Extension
from torch.utils.data import DataLoader
from transformers import RobertaForSequenceClassification


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    if args.output_directory_path is None:
        args.output_directory_path = Path(args.test_dataset_path).parent / f'predictions{Extension.CSV.value}'

    test_dataset = QodanaDataset(args.test_dataset_path, args.context_length)
    num_labels = test_dataset[0][MarkingArgument.LABELS.value].shape[0]
    eval_dataloader = DataLoader(test_dataset, batch_size=args.batch_size)
    predictions = np.zeros([len(test_dataset), num_labels], dtype=object)

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model = RobertaForSequenceClassification.from_pretrained(args.model_weights_directory_path,
                                                             num_labels=num_labels).to(device)
    model.eval()

    start_index = 0

    for batch in eval_dataloader:
        with torch.no_grad():
            logits = model(input_ids=batch[MarkingArgument.INPUT_IDS.value].detach()).logits
            logits = logits.sigmoid().detach().cpu().numpy()
            predictions[start_index:start_index + args.batch_size, :num_labels] = (logits > args.threshold).astype(int)
            start_index += args.batch_size

    predictions = pd.DataFrame(predictions, columns=range(num_labels), dtype=int)
    true_labels = pd.read_csv(args.test_dataset_path).iloc[:, 1:]
    metric = Metric(args.threshold)
    print(f"f1_score: {metric.get_f1_score(predictions, true_labels)}")
    write_dataframe_to_csv(args.output_directory_path, predictions)


if __name__ == '__main__':
    sys.exit(main())
