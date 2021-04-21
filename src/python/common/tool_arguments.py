from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Union
from src.python.review.inspectors.inspector_type import InspectorType


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


@dataclass(frozen=True)
class ArgumentsCharacteristics:
    short_name: Union[str, None]
    long_name: str
    description: str


inspectors = [inspector.lower() for inspector in InspectorType.available_values()]
example = f'-d {inspectors[0].lower()},{inspectors[1].lower()}'


@unique
class RunToolArguments(Enum):
    VERBOSITY = ArgumentsCharacteristics('-v',
                                         '--verbosity',
                                         'Choose logging level: '
                                         f'{VerbosityLevel.ERROR.value} - ERROR; '
                                         f'{VerbosityLevel.INFO.value} - INFO; '
                                         f'{VerbosityLevel.DEBUG.value} - DEBUG; '
                                         f'{VerbosityLevel.DISABLE.value} - disable logging; '
                                         'default is 0')

    DISABLE = ArgumentsCharacteristics('-d', '--disable',
                                       'Disable inspectors. '
                                       f'Allowed values: {", ".join(inspectors)}. '
                                       f'Example: {example}')

    DUPLICATES = ArgumentsCharacteristics(None, '--allow-duplicates',
                                          'Allow duplicate issues found by different linters. '
                                          'By default, duplicates are skipped.')

    LANG_VERSION = ArgumentsCharacteristics('--language_version', '--language_version',
                                            'Specify the language version for JAVA inspectors.')

    CPU = ArgumentsCharacteristics('--n_cpu', '--n-cpu',
                                   'Specify number of cpu that can be used to run inspectors')

    PATH = ArgumentsCharacteristics(None, 'path', 'Path to file or directory to inspect.')

    FORMAT = ArgumentsCharacteristics('-f', '--format',
                                      'The output format. Default is JSON.')

    START_LINE = ArgumentsCharacteristics('-s', '--start-line',
                                          'The first line to be analyzed. It starts from 1.')

    END_LINE = ArgumentsCharacteristics('-e', '--end-line', 'The end line to be analyzed or None.')

    NEW_FORMAT = ArgumentsCharacteristics(None, '--new-format',
                                          'The argument determines whether the tool '
                                          'should use the new format')
