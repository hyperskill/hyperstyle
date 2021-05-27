from enum import Enum, unique

from transformers import RobertaTokenizer


@unique
class MarkingArgument(Enum):
    ID = 'id'
    IN_ID = 'inspection_id'
    INSPECTIONS = 'inspections'
    INPUT_IDS = 'input_ids'
    ATT_MASK = 'attention_mask'
    LABELS = 'labels'
    DATASET_PATH = 'dataset_path'
    STEPS = 'steps'
    SEED = 42


@unique
class CustomTokens(Enum):
    NOC = ['NOC']  # no context token to add when there are no lines for the context


tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
