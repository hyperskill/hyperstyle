import argparse
import json
import sys
from pathlib import Path

from src.python.evaluation.evaluation_run_tool import logger
from src.python.evaluation.paper_evaluation.survey_handler.survey_statistics import SurveyStatistics, SurveyJsonField
from src.python.review.common.file_system import get_content_from_file


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('questions_json_path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to the JSON with labelled questions')

    parser.add_argument('results_json_path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to the JSON with survey results')


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        questions_json = json.loads(get_content_from_file(args.questions_json_path))
        results_json = json.loads(get_content_from_file(args.results_json_path))
        stat = SurveyStatistics(questions_json[SurveyJsonField.QUESTIONS.value], results_json[SurveyJsonField.QUESTIONS.value])
        stat.print_stat()
        return 0

    except FileNotFoundError:
        logger.error('JSON file did not found')
        return 2

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
