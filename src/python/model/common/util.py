from enum import Enum, unique


@unique
class MarkingArgument(Enum):
    ID = 'id'
    IN_ID = 'inspection_id'
    INSPECTIONS = 'inspections'
    INPUT_IDS = 'input_ids'
    LABELS = 'labels'
    DATASET_PATH = 'dataset_path'
    STEPS = 'steps'
    WEIGHTS = 'weights'
    WANDB = 'wandb'
    SEED = 42


@unique
class CustomTokens(Enum):
    NOC = '[NOC]'  # no context token to add when there are no lines for the context
