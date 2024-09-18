from dataclasses import dataclass, field
from pathlib import Path

from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from test.python import TEST_DATA_FOLDER
from typing import List, Optional

import pytest
from hyperstyle.src.python import MAIN_FOLDER
from hyperstyle.src.python.common.tool_arguments import RunToolArgument

DATA_PATH = TEST_DATA_FOLDER / 'functional_tests'


@dataclass
class LocalCommandBuilder:
    verbosity: int = 2
    disable: List[str] = field(default_factory=lambda: [])
    allow_duplicates: bool = False
    language_version: Optional[str] = None
    n_cpu: int = 1
    format = 'text'
    # format: Literal['json', 'text'] = 'text' take it from Py3.8
    path: Optional[Path] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    new_format: bool = False
    group_by_difficulty: bool = False
    history: Optional[str] = None
    ij_config: Optional[str] = None

    def build(self) -> List[str]:
        assert self.path is not None

        command = [
            'python3', (MAIN_FOLDER.parent / 'review/run_tool.py'),
            RunToolArgument.VERBOSITY.value.long_name, str(self.verbosity),
        ]

        # TODO: remove after adding a test server
        self.disable.append(InspectorType.IJ_PYTHON.value)
        self.disable.append(InspectorType.IJ_KOTLIN.value)

        if self.disable:
            command.extend([RunToolArgument.DISABLE.value.long_name, ','.join(self.disable)])

        if self.allow_duplicates:
            command.append(RunToolArgument.DUPLICATES.value.long_name)

        if self.language_version is not None:
            command.extend([RunToolArgument.LANG_VERSION.value.long_name, self.language_version])

        if self.new_format:
            command.append(RunToolArgument.NEW_FORMAT.value.long_name)

        if self.history is not None:
            command.extend([RunToolArgument.HISTORY.value.long_name, self.history])

        if self.ij_config is not None:
            command.extend([RunToolArgument.IJ_CONFIG.value.long_name, self.ij_config])

        if self.group_by_difficulty:
            command.append(RunToolArgument.GROUP_BY_DIFFICULTY.value.long_name)

        command.extend([
            RunToolArgument.CPU.value.long_name, str(self.n_cpu),
            RunToolArgument.FORMAT.value.long_name, self.format,
            str(self.path),
        ])

        if self.start_line is not None:
            command.extend([RunToolArgument.START_LINE.value.long_name, str(self.start_line)])

        if self.end_line is not None:
            command.extend([RunToolArgument.END_LINE.value.long_name, str(self.end_line)])

        return command


@pytest.fixture
def local_command() -> LocalCommandBuilder:
    return LocalCommandBuilder()
