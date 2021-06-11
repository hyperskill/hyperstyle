import logging.config
import os
from argparse import Namespace
from pathlib import Path
from typing import List, Optional, Union

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.util import EvaluationArgument
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import (
    Extension,
    get_parent_folder,
    get_restricted_extension,
)

logger = logging.getLogger(__name__)


class EvaluationConfig:
    def __init__(self, args: Namespace):
        self.tool_path: Union[str, Path] = args.tool_path
        self.format: str = args.format
        self.solutions_file_path: Union[str, Path] = args.solutions_file_path
        self.traceback: bool = args.traceback
        self.with_history: bool = args.with_history
        self.output_folder_path: Union[str, Path] = args.output_folder_path
        self.extension: Extension = get_restricted_extension(self.solutions_file_path, [Extension.XLSX, Extension.CSV])
        self.__init_output_file_name(args.output_file_name)

    def __init_output_file_name(self, output_file_name: Optional[str]):
        if output_file_name is None:
            self.output_file_name = f'{EvaluationArgument.RESULT_FILE_NAME.value}{self.extension.value}'
        else:
            self.output_file_name = output_file_name

    def build_command(self, inspected_file_path: Union[str, Path], lang: str, history: Optional[str]) -> List[str]:
        command = [LanguageVersion.PYTHON_3.value,
                   self.tool_path,
                   inspected_file_path,
                   RunToolArgument.FORMAT.value.short_name, self.format]

        if self.with_history and history is not None:
            command.extend([RunToolArgument.HISTORY.value.long_name, history])

        if lang == LanguageVersion.JAVA_8.value or lang == LanguageVersion.JAVA_11.value:
            command.extend([RunToolArgument.LANG_VERSION.value.long_name, lang])
        return command

    def get_output_file_path(self) -> Path:
        if self.output_folder_path is None:
            try:
                self.output_folder_path = get_parent_folder(Path(self.solutions_file_path))
                os.makedirs(self.output_folder_path, exist_ok=True)
            except FileNotFoundError as e:
                logger.error('XLSX-file or CSV-file with the specified name does not exists.')
                raise e
        return Path(self.output_folder_path) / self.output_file_name
