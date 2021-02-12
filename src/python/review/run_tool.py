import argparse
import logging.config
import os
import sys
import traceback
from enum import Enum, unique
from pathlib import Path
from typing import Set, List

sys.path.append('')
sys.path.append('../../..')

from src.python.review.application_config import ApplicationConfig, LanguageVersion
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.logging_config import logging_config
from src.python.review.reviewers.perform_review import OutputFormat, PathNotExists, perform_and_print_review, \
    UnsupportedLanguage

logger = logging.getLogger(__name__)


@unique
class VerbosityLevel(Enum):
    """
    Same meaning as the logging level. Should be used in command-line args.
    """
    DEBUG = '3'
    INFO = '2'
    ERROR = '1'
    DISABLE = '0'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for _, member in VerbosityLevel.__members__.items()]


def parse_disabled_inspectors(value: str) -> Set[InspectorType]:
    passed_names = value.upper().split(',')
    allowed_names = {inspector.value for inspector in InspectorType}
    if not all(name in allowed_names for name in passed_names):
        raise argparse.ArgumentError('disable', 'Incorrect inspectors\' names')

    return {InspectorType(name) for name in passed_names}


def positive_int(value: str) -> int:
    value_int = int(value)
    if value_int <= 0:
        raise ValueError

    return value_int


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('-v', '--verbosity',
                        help='Choose logging level: '
                             f'{VerbosityLevel.ERROR.value} - ERROR; '
                             f'{VerbosityLevel.INFO.value} - INFO; '
                             f'{VerbosityLevel.DEBUG.value} - DEBUG; '
                             f'{VerbosityLevel.DISABLE.value} - disable logging; '
                             'default is 0',
                        default=VerbosityLevel.DISABLE.value,
                        choices=VerbosityLevel.values(),
                        type=str)

    # Usage example: -d Flake8,Intelli
    inspectors = [inspector.lower() for inspector in InspectorType.available_values()]
    example = f'-d {inspectors[0].lower()},{inspectors[1].lower()}'

    parser.add_argument('-d', '--disable',
                        help='Disable inspectors. '
                             f'Allowed values: {", ".join(inspectors)}. '
                             f'Example: {example}',
                        type=parse_disabled_inspectors,
                        default=set())

    parser.add_argument('--allow_duplicates', action='store_true',
                        help='Allow duplicate issues found by different linters. '
                             'By default, duplicates are skipped.')

    parser.add_argument('--language_version',
                        help='Specify the language version for JAVA inspectors.',
                        default=None,
                        choices=LanguageVersion.values(),
                        type=str)

    parser.add_argument('--n_cpu',
                        help='Specify number of cpu that can be used to run inspectors',
                        default=1,
                        type=positive_int)

    parser.add_argument('path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to file or directory to inspect.')

    parser.add_argument('-f', '--format',
                        default=OutputFormat.JSON,
                        choices=OutputFormat.values(),
                        type=str,
                        help='The output format. Default is JSON.')

    parser.add_argument('-s', '--start_line',
                        default=1,
                        type=positive_int,
                        help='The first line to be analyzed. It starts from 1.')

    parser.add_argument('-e', '--end_line',
                        default=None,
                        type=positive_int,
                        help='The end line to be analyzed or None.')

    parser.add_argument('--new_format',
                        action='store_true',
                        help='The argument determines whether the tool '
                             'should use the new format')


def configure_logging(verbosity: VerbosityLevel) -> None:
    if verbosity is VerbosityLevel.ERROR:
        logging_config['loggers']['']['level'] = logging.ERROR
    elif verbosity is VerbosityLevel.INFO:
        logging_config['loggers']['']['level'] = logging.INFO
    elif verbosity is VerbosityLevel.DEBUG:
        logging_config['loggers']['']['level'] = logging.DEBUG
    elif verbosity is VerbosityLevel.DISABLE:
        logging_config['loggers']['']['level'] = logging.CRITICAL

    logging.config.dictConfig(logging_config)


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        configure_logging(VerbosityLevel(args.verbosity))

        n_cpu = args.n_cpu
        max_n_cpu = os.cpu_count()
        if n_cpu > max_n_cpu:
            n_cpu = max_n_cpu
            logger.warning(f'Number of available cpu is {max_n_cpu}, '
                           f'but {n_cpu} was passed')

        start_line = args.start_line
        if start_line < 1:
            start_line = 1

        inspectors_config = {
            'language_version': LanguageVersion(args.language_version) if args.language_version is not None else None,
            'n_cpu': n_cpu
        }

        config = ApplicationConfig(
            args.disable, args.allow_duplicates,
            n_cpu, inspectors_config,
            start_line=start_line,
            end_line=args.end_line,
            new_format=args.new_format,
        )

        n_issues = perform_and_print_review(args.path, OutputFormat(args.format), config)
        if not n_issues:
            return 0

        return 1
    except PathNotExists:
        logger.error('Path not exists')
        return 2
    except UnsupportedLanguage:
        logger.error('Unsupported language. Supported ones are Java, Kotlin, Python')
        return 2
    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error')
        return 2


if __name__ == '__main__':
    sys.exit(main())
