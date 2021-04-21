import argparse
<<<<<<< HEAD
import enum
=======

>>>>>>> ab62d8a2ed55fab219de28b30526dd13764085a4
from src.python.review.reviewers.perform_review import OutputFormat
from src.python.evaluation.common.util import EvaluationProcessNames


def get_parser(run_tool_arguments: enum.EnumMeta) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_folder_path', '--output_folder_path', default=None)
    parser.add_argument('--output_file_name', '--output_file_name',
                        default=EvaluationProcessNames.RESULTS_EXT.value)
    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value)
    return parser
