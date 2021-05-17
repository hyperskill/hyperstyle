import logging.config
from argparse import Namespace
from pathlib import Path
from typing import List, Union

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.util import EvaluationArgument
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import create_directory, Extension

logger = logging.getLogger(__name__)


class EvaluationConfig:
    def __init__(self, args: Namespace):
        self.tool_path: Union[str, Path] = args.tool_path
        self.output_format: str = args.format
        self.solutions_file_path: Union[str, Path] = args.solutions_file_path
        self.traceback: bool = args.traceback
        self.output_folder_path: Union[str, Path] = args.output_folder_path
        self.output_file_name: str = args.output_file_name
        self.extension: Extension = self.__get_extension()

    def __get_extension(self) -> Extension:
        if self.solutions_file_path is None:
            return Extension.EMPTY
        ext = Extension.get_extension_from_file(self.solutions_file_path)
        available_values = [Extension.XLSX, Extension.CSV]
        if ext not in available_values:
            raise ValueError(f'Invalid extension. '
                             f'Available values are: {list(map(lambda e: e.value, available_values))}.')
        return ext

    def build_command(self, inspected_file_path: Union[str, Path], lang: str) -> List[str]:
        command = [LanguageVersion.PYTHON_3.value,
                   self.tool_path,
                   inspected_file_path,
                   RunToolArgument.FORMAT.value.short_name, self.output_format]

        if lang == LanguageVersion.JAVA_8.value or lang == LanguageVersion.JAVA_11.value:
            command.extend([RunToolArgument.LANG_VERSION.value.long_name, lang])
        return command

    def get_output_file_path(self) -> Path:
        if self.output_folder_path is None:
            try:
                self.output_folder_path = (
                        Path(self.solutions_file_path).parent.parent / EvaluationArgument.RESULT_FILE_NAME.value
                )
                create_directory(self.output_folder_path)
            except FileNotFoundError as e:
                logger.error('XLSX-file or CSV-file with the specified name does not exists.')
                raise e
        return Path(self.output_folder_path) / self.output_file_name
