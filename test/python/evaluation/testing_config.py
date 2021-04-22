import argparse
import enum

from src.python import MAIN_FOLDER
from src.python.evaluation.common.util import EvaluationProcessNames
from src.python.review.reviewers.perform_review import OutputFormat


def get_parser(run_tool_arguments: enum.EnumMeta, n_args=2) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_folder_path', '--output_folder_path', default=None)
    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value)
    if n_args > 2:
        parser.add_argument('--output_file_name', '--output_file_name',
                            default=EvaluationProcessNames.RESULTS_EXT.value)
        parser.add_argument('--traceback', '--traceback', default=False)

        if n_args == 5:
            parser.add_argument('-tool_path', '--tool_path',
                                default=MAIN_FOLDER.parent / 'review/run_tool.py')
    return parser
