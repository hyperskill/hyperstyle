from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pytest
from src.python import MAIN_FOLDER


@dataclass
class EvalLocalCommandBuilder:
    path: Optional[Path] = None
    xlsx_tool_path: Optional[Path] = MAIN_FOLDER.parent / 'evaluation/xlsx_run_tool.py'
    tool_path: Optional[Path] = MAIN_FOLDER.parent / 'review/run_tool.py'
    traceback: Optional[str] = None

    def build(self) -> List[str]:
        assert self.path is not None
        command = ['python3', self.xlsx_tool_path, str(self.path), '-t', self.tool_path]
        if self.traceback is not None:
            command.extend(['--traceback', self.traceback])
        return command


@pytest.fixture
def eval_command_builder() -> EvalLocalCommandBuilder:
    return EvalLocalCommandBuilder()


@dataclass
class BrokenLocalCommandBuilder:
    path: Optional[Path] = None
    tool_path: Optional[Path] = MAIN_FOLDER.parent / 'evaluation/do_not_exist.py'

    def build(self) -> List[str]:
        assert self.path is not None
        command = ['python3', str(self.path), '-t', self.tool_path]
        return command


@pytest.fixture
def broken_command_builder() -> BrokenLocalCommandBuilder:
    return BrokenLocalCommandBuilder()
