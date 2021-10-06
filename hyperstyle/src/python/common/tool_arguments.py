from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional

from hyperstyle.src.python.review.application_config import LanguageVersion
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType


@unique
class VerbosityLevel(Enum):
    """
    Same meaning as the logging level. Should be used in command-line args.
    """
    DEBUG = 3
    INFO = 2
    ERROR = 1
    DISABLE = 0

    @classmethod
    def values(cls) -> List[int]:
        return [member.value for member in VerbosityLevel]


@dataclass(frozen=True)
class ArgumentsInfo:
    short_name: Optional[str]
    long_name: str
    description: str


@unique
class RunToolArgument(Enum):
    VERBOSITY = ArgumentsInfo('-v', '--verbosity',
                              'Choose logging level: '
                              f'{VerbosityLevel.ERROR.value} - ERROR; '
                              f'{VerbosityLevel.INFO.value} - INFO; '
                              f'{VerbosityLevel.DEBUG.value} - DEBUG; '
                              f'{VerbosityLevel.DISABLE.value} - disable logging; '
                              'default is 0')

    inspectors = [inspector.lower() for inspector in InspectorType.available_values()]
    disabled_inspectors_example = f'-d {inspectors[0].lower()},{inspectors[1].lower()}'

    DISABLE = ArgumentsInfo('-d', '--disable',
                            'Disable inspectors. '
                            f'Available values: {", ".join(inspectors)}. '
                            f'Example: {disabled_inspectors_example}')

    DUPLICATES = ArgumentsInfo(None, '--allow-duplicates',
                               'Allow duplicate issues found by different linters. '
                               'By default, duplicates are skipped.')

    LANG_VERSION = ArgumentsInfo(None, '--language-version',
                                 'Specify the language version for JAVA inspectors.'
                                 'Available values are: '
                                 f'{LanguageVersion.PYTHON_3.value}, {LanguageVersion.JAVA_8.value}, '
                                 f'{LanguageVersion.JAVA_11.value}, {LanguageVersion.KOTLIN.value}.')

    CPU = ArgumentsInfo(None, '--n-cpu',
                        'Specify number of cpu that can be used to run inspectors')

    PATH = ArgumentsInfo(None, 'path', 'Path to file or directory to inspect.')

    FORMAT = ArgumentsInfo('-f', '--format',
                           'The output format. Default is JSON.')

    START_LINE = ArgumentsInfo('-s', '--start-line',
                               'The first line to be analyzed. It starts from 1.')

    END_LINE = ArgumentsInfo('-e', '--end-line', 'The end line to be analyzed or None.')

    NEW_FORMAT = ArgumentsInfo(None, '--new-format',
                               'The argument determines whether the tool '
                               'should use the new format')

    HISTORY = ArgumentsInfo(None, '--history',
                            'Json string, which contains lists of issues in the previous submissions '
                            'for other tasks for one user.')

    WITH_ALL_CATEGORIES = ArgumentsInfo(None, '--with-all-categories',
                                        'Without this flag, all issues will be categorized into 5 main categories: '
                                        'CODE_STYLE, BEST_PRACTICES, ERROR_PRONE, COMPLEXITY, INFO.')

    GROUP_BY_DIFFICULTY = ArgumentsInfo(None, '--group-by-difficulty',
                                        'With this flag, the final grade will be grouped by the issue difficulty.')
