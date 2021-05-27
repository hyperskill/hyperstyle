import logging

import pandas as pd
import torch
from src.python.model.common.util import MarkingArgument, tokenizer

logger = logging.getLogger(__name__)


class SimpleDataset(torch.utils.data.Dataset):
    """ MarkingArgument.ID.value is a an id of the solution that corresponds to the line
        MarkingArgument.INSPECTIONS.value is a is a target column name in dataset
        ColumnName.CODE.value is an observation column name in dataset where lines of code are stored
    """
    def __init__(self, df: pd.DataFrame):
        code = list(map(str, df['code']))
        target = df.iloc[:, 1:]
        code_encoded = tokenizer(code, padding=True, truncation=True, max_length=400)
        self.examples = []
        for inputs, attention_mask, label in zip(code_encoded[MarkingArgument.INPUT_IDS.value],
                                                 code_encoded[MarkingArgument.ATT_MASK.value],
                                                 target.values):
            self.examples.append({
                MarkingArgument.INPUT_IDS.value: torch.tensor(inputs),
                MarkingArgument.ATT_MASK.value: torch.tensor(attention_mask),
                MarkingArgument.LABELS.value: torch.tensor(label.astype(int)),
            })

    def __getitem__(self, idx):
        return self.examples[idx]

    def __len__(self):
        return len(self.examples)
