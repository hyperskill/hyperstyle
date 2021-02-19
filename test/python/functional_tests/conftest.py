from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pytest

from src.python import MAIN_FOLDER
from test.python import TEST_DATA_FOLDER

DATA_PATH = TEST_DATA_FOLDER / 'functional_tests'


@dataclass
class LocalCommandBuilder:
    verbosity: int = 2
    disable: List[str] = field(default_factory=lambda: ['intellij', 'spotbugs'])
    allow_duplicates: bool = False
    language_version: Optional[str] = None
    n_cpu: int = 1
    format = 'text'
    # format: Literal['json', 'text'] = 'text' take it from Py3.8
    path: Optional[Path] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    new_format: bool = False

    def build(self) -> List[str]:
        assert self.path is not None

        command = ['python3', (MAIN_FOLDER.parent / 'review/run_tool.py'), f'-v{self.verbosity}']
        if self.disable:
            command.extend(['-d', ','.join(self.disable)])

        if self.allow_duplicates:
            command.append('--allow-duplicates')

        if self.language_version is not None:
            command.extend(['--language-version', self.language_version])

        if self.new_format:
            command.append('--new-format')

        command.extend([
            '--n_cpu', str(self.n_cpu),
            '-f', self.format,
            str(self.path)
        ])

        if self.start_line is not None:
            command.extend(['-s', str(self.start_line)])

        if self.end_line is not None:
            command.extend(['-e', str(self.end_line)])

        return command


@pytest.fixture
def local_command() -> LocalCommandBuilder:
    return LocalCommandBuilder()
