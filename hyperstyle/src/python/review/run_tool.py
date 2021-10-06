import argparse
import logging.config
import os
import sys
import traceback
from json import JSONDecodeError
from pathlib import Path
from typing import Set

sys.path.append('')
sys.path.append('../../../..')

from hyperstyle.src.python.common.tool_arguments import RunToolArgument, VerbosityLevel
from hyperstyle.src.python.review.application_config import ApplicationConfig, LanguageVersion
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.logging_config import logging_config
from hyperstyle.src.python.review.reviewers.perform_review import (
    OutputFormat,
    PathNotExists,
    perform_and_print_review,
    UnsupportedLanguage,
)

logger = logging.getLogger(__name__)


def parse_disabled_inspectors(value: str) -> Set[InspectorType]:
    passed_names = value.upper().split(',')
    # TODO: delete it after updating the run configuration in production
    intellij_key_word = 'intellij'.upper()
    if intellij_key_word in passed_names:
        passed_names.remove(intellij_key_word)
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
    parser.add_argument(RunToolArgument.VERBOSITY.value.short_name,
                        RunToolArgument.VERBOSITY.value.long_name,
                        help=RunToolArgument.VERBOSITY.value.description,
                        default=VerbosityLevel.DISABLE.value,
                        choices=VerbosityLevel.values(),
                        type=int)

    # Usage example: -d Flake8,Intelli
    parser.add_argument(RunToolArgument.DISABLE.value.short_name,
                        RunToolArgument.DISABLE.value.long_name,
                        help=RunToolArgument.DISABLE.value.description,
                        type=parse_disabled_inspectors,
                        default=set())

    parser.add_argument(RunToolArgument.DUPLICATES.value.long_name,
                        action='store_true',
                        help=RunToolArgument.DUPLICATES.value.description)

    # TODO: deprecated argument: language_version. Delete after several releases.
    parser.add_argument('--language_version',
                        RunToolArgument.LANG_VERSION.value.long_name,
                        help=RunToolArgument.LANG_VERSION.value.description,
                        default=None,
                        choices=LanguageVersion.values(),
                        type=str)

    # TODO: deprecated argument: --n_cpu. Delete after several releases.
    parser.add_argument('--n_cpu',
                        RunToolArgument.CPU.value.long_name,
                        help=RunToolArgument.CPU.value.description,
                        default=1,
                        type=positive_int)

    parser.add_argument(RunToolArgument.PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.PATH.value.description)

    parser.add_argument(RunToolArgument.FORMAT.value.short_name,
                        RunToolArgument.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=RunToolArgument.FORMAT.value.description)

    parser.add_argument(RunToolArgument.START_LINE.value.short_name,
                        RunToolArgument.START_LINE.value.long_name,
                        default=1,
                        type=positive_int,
                        help=RunToolArgument.START_LINE.value.description)

    parser.add_argument(RunToolArgument.END_LINE.value.short_name,
                        RunToolArgument.END_LINE.value.long_name,
                        default=None,
                        type=positive_int,
                        help=RunToolArgument.END_LINE.value.description)

    parser.add_argument(RunToolArgument.NEW_FORMAT.value.long_name,
                        action='store_true',
                        help=RunToolArgument.NEW_FORMAT.value.description)

    parser.add_argument(RunToolArgument.HISTORY.value.long_name,
                        help=RunToolArgument.HISTORY.value.description,
                        type=str)

    parser.add_argument(RunToolArgument.WITH_ALL_CATEGORIES.value.long_name,
                        help=RunToolArgument.WITH_ALL_CATEGORIES.value.description,
                        action='store_true')

    parser.add_argument(RunToolArgument.GROUP_BY_DIFFICULTY.value.long_name,
                        help=RunToolArgument.GROUP_BY_DIFFICULTY.value.description,
                        action='store_true')


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
            logger.warning('Number of available cpu is %s, but %s was passed', max_n_cpu, n_cpu)

        start_line = args.start_line
        if start_line < 1:
            start_line = 1

        inspectors_config = {
            'language_version': LanguageVersion(args.language_version) if args.language_version is not None else None,
            'n_cpu': n_cpu,
        }

        config = ApplicationConfig(
            args.disable, args.allow_duplicates,
            n_cpu, inspectors_config,
            start_line=start_line,
            end_line=args.end_line,
            new_format=args.new_format,
            history=args.history,
            with_all_categories=args.with_all_categories,
            group_by_difficulty=args.group_by_difficulty,
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

    except JSONDecodeError:
        logger.error('Incorrect JSON')
        return 2

    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error')
        return 2


if __name__ == '__main__':
    sys.exit(main())
