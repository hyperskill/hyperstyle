import argparse

from src.python.review.common.file_system import Extension


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--dataset_path',
                        type=str,
                        help='Path to the dataset received by either'
                             f' src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('--model_weights',
                        type=str,
                        help='Path to the directory where trained model weights are stored.')

    parser.add_argument('--output_dir',
                        default=None,
                        type=str,
                        help='Path to the directory where labeled dataset will be saved. Default is the same'
                             'directory where test dataset is.')

    parser.add_argument('-bs', '--batch_size',
                        type=int,
                        default=8,
                        help='Batch_size – default is 8.')

    parser.add_argument('-th', '--threshold',
                        type=float,
                        default=0.5,
                        help='If the probability of inspection on code sample is greater than threshold,'
                             'inspection id will be assigned to the sample. '
                             'Default is 0.5.')
