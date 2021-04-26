import argparse
import enum

from src.python import MAIN_FOLDER
from src.python.evaluation.common.util import EvaluationProcessNames
from src.python.review.reviewers.perform_review import OutputFormat


def get_parser(run_tool_arguments: enum.EnumMeta, n_args=2) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-ofp', '--output-folder-path', default=None)
    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value)
    parser.add_argument('-ofn', '--output-file-name',
                        default=EvaluationProcessNames.RESULTS_EXT.value)
    if n_args > 2:
        parser.add_argument('-tr', '--traceback', action='store_true')

        if n_args == 5:
            parser.add_argument('-tp', '--tool-path',
                                default=MAIN_FOLDER.parent / 'review/run_tool.py')
    return parser
