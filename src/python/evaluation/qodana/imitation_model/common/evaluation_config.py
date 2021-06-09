import argparse

from src.python.evaluation.qodana.imitation_model.common.util import ModelCommonArgument
from src.python.review.common.file_system import Extension


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('test_dataset_path',
                        type=str,
                        help='Path to the dataset received by either'
                             f' src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('model_weights_directory_path',
                        type=str,
                        help='Path to the directory where trained imitation_model weights are stored.')

    parser.add_argument('-o', '--output_directory_path',
                        default=None,
                        type=str,
                        help='Path to the directory where labeled dataset will be saved. Default is the parent folder'
                             'of test_dataset_path.')

    parser.add_argument('-sf', '--save_f1_score',
                        default=None,
                        action="store_true",
                        help=f'If enabled report with f1 scores by class will be saved to the {Extension.CSV.value}'
                             ' File will be saved to the labeled dataset parent directory. Default is False.')

    parser.add_argument(ModelCommonArgument.CONTEXT_LENGTH.value.short_name,
                        ModelCommonArgument.CONTEXT_LENGTH.value.long_name,
                        type=int,
                        default=40,
                        help=ModelCommonArgument.CONTEXT_LENGTH.value.description)

    parser.add_argument(ModelCommonArgument.BATCH_SIZE.value.short_name,
                        ModelCommonArgument.BATCH_SIZE.value.long_name,
                        type=int,
                        default=8,
                        help=ModelCommonArgument.BATCH_SIZE.value.description)

    parser.add_argument(ModelCommonArgument.THRESHOLD.value.short_name,
                        ModelCommonArgument.THRESHOLD.value.long_name,
                        type=float,
                        default=0.5,
                        help=ModelCommonArgument.THRESHOLD.value.description)
