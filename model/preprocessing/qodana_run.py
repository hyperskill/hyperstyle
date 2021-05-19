import argparse
import os
from pathlib import Path
import logging.config
import sys

sys.path.append('')
sys.path.append('../../..')

from src.python.review.common.subprocess_runner import run_in_subprocess
logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('input_folder_path',
                        type=lambda value: Path(value).absolute(),
                        help='Absolute path to the directory with Java files')

    parser.add_argument('-ofp', '--output_folder_path',
                        type=lambda value: Path(value).absolute(),
                        help='Absolute path to the directory with output files',
                        # will be input_folder_path if not stated
                        default=None)


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    try:
        args = parser.parse_args()
        output_folder_path = args.output_folder_path
        if output_folder_path is None:
            output_folder_path = args.input_folder_path
        directories = os.listdir(args.input_folder_path)
        for directory in directories:
            command = ['docker', 'run', '--rm', '-v',
                       f'{Path(args.input_folder_path) / directory}/:/data/project/', '-v',
                       f'{Path(output_folder_path) / directory}_res/:/data/results/',
                       'jetbrains/qodana']
            run_in_subprocess(command)
        return 0

    except FileNotFoundError as e:
        logger.error('Specified directory path does not exist.')
        return 2


if __name__ == '__main__':
    main()
