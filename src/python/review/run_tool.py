import argparse
import enum
import logging.config
import os
import sys
import traceback
from json import JSONDecodeError
from pathlib import Path
from typing import Set


sys.path.append('')
sys.path.append('../../..')

from src.python.common.tool_arguments import RunToolArgument, VerbosityLevel
from src.python.review.application_config import ApplicationConfig, LanguageVersion
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.logging_config import logging_config
from src.python.review.reviewers.perform_review import (
    OutputFormat,
    PathNotExists,
    perform_and_print_review,
    UnsupportedLanguage,
)

logger = logging.getLogger(__name__)


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


def configure_arguments(parser: argparse.ArgumentParser, tool_arguments: enum.EnumMeta) -> None:
    parser.add_argument(tool_arguments.VERBOSITY.value.short_name,
                        tool_arguments.VERBOSITY.value.long_name,
                        help=tool_arguments.VERBOSITY.value.description,
                        default=VerbosityLevel.DISABLE.value,
                        choices=VerbosityLevel.values(),
                        type=str)

    # Usage example: -d Flake8,Intelli
    parser.add_argument(tool_arguments.DISABLE.value.short_name,
                        tool_arguments.DISABLE.value.long_name,
                        help=tool_arguments.DISABLE.value.description,
                        type=parse_disabled_inspectors,
                        default=set())

    parser.add_argument(tool_arguments.DUPLICATES.value.long_name,
                        action='store_true',
                        help=tool_arguments.DUPLICATES.value.description)

    # TODO: deprecated argument: language_version. Delete after several releases.
    parser.add_argument('--language_version',
                        tool_arguments.LANG_VERSION.value.long_name,
                        help=tool_arguments.LANG_VERSION.value.description,
                        default=None,
                        choices=LanguageVersion.values(),
                        type=str)

    # TODO: deprecated argument: --n_cpu. Delete after several releases.
    parser.add_argument('--n_cpu',
                        tool_arguments.CPU.value.long_name,
                        help=tool_arguments.CPU.value.description,
                        default=1,
                        type=positive_int)

    parser.add_argument(tool_arguments.PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=tool_arguments.PATH.value.description)

    parser.add_argument(tool_arguments.FORMAT.value.short_name,
                        tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=tool_arguments.FORMAT.value.description)

    parser.add_argument(tool_arguments.START_LINE.value.short_name,
                        tool_arguments.START_LINE.value.long_name,
                        default=1,
                        type=positive_int,
                        help=tool_arguments.START_LINE.value.description)

    parser.add_argument(tool_arguments.END_LINE.value.short_name,
                        tool_arguments.END_LINE.value.long_name,
                        default=None,
                        type=positive_int,
                        help=tool_arguments.END_LINE.value.description)

    parser.add_argument(tool_arguments.NEW_FORMAT.value.long_name,
                        action='store_true',
                        help=tool_arguments.NEW_FORMAT.value.description)

    parser.add_argument(tool_arguments.HISTORY.value.long_name,
                        help=tool_arguments.HISTORY.value.help,
                        type=str)


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
    configure_arguments(parser, RunToolArgument)

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
