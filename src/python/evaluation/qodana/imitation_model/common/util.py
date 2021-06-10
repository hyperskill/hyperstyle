from enum import Enum, unique

from src.python.common.tool_arguments import ArgumentsInfo


@unique
class DatasetColumnArgument(Enum):
    ID = 'id'
    IN_ID = 'inspection_id'
    INSPECTIONS = 'inspections'
    INPUT_IDS = 'input_ids'
    LABELS = 'labels'
    DATASET_PATH = 'dataset_path'
    STEPS = 'steps'
    WEIGHTS = 'weights'
    WANDB = 'wandb'


@unique
class SeedArgument(Enum):
    SEED = 42


@unique
class CustomTokens(Enum):
    NOC = '[NOC]'  # no context token to add when there are no lines for the context


@unique
class ModelCommonArgument(Enum):
    THRESHOLD = ArgumentsInfo('-th', '--threshold',
                              'If the probability of inspection on code sample is greater than threshold,'
                              'inspection id will be assigned to the sample. '
                              'Default is 0.5.')

    CONTEXT_LENGTH = ArgumentsInfo('-cl', '--context_length',
                                   'Sequence length of 1 sample after tokenization, default is 40.')

    BATCH_SIZE = ArgumentsInfo('-bs', '--batch_size',
                               'Batch size – default values are 16 for training and 8 for evaluation mode.')


@unique
class MeasurerArgument(Enum):
    F1_SCORE = 'f1_score'
    F1_SCORES_BY_CLS = 'f1_scores_by_class'
