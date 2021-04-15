from pathlib import Path

from src.python import MAIN_FOLDER
from src.python.evaluation.support_functions import create_folder


class ApplicationConfig:
    def __init__(self, args):
        self.tool_path = args.tool_path
        self.output_format = args.format
        self.data_path = args.data_path
        self.traceback = args.traceback
        self.folder_path = args.folder_path
        self.file_name = args.file_name

    def build_command(self, file_path, lang):
        command = ['python3', self.tool_path, file_path, '-f', self.output_format]
        if lang == 'java8' or lang == 'java11':
            command.extend(['--language_version', lang])
        return command

    def get_data_path(self):
        return self.data_path

    def get_traceback(self):
        return self.traceback

    def get_file_path(self):
        if self.folder_path is None:
            self.folder_path = MAIN_FOLDER.parent / 'evaluation/results'
            create_folder(self.folder_path)

        return Path(self.folder_path) / self.file_name
