from src.python import MAIN_FOLDER
from src.python.evaluation.common.util import EvaluationArgument
from src.python.review.reviewers.perform_review import OutputFormat


def get_testing_arguments(n_args=2) -> dict:
    testing_arguments_dict = {'format': OutputFormat.JSON.value,
                              'output_file_name': EvaluationArgument.RESULT_FILE_NAME_EXT.value,
                              'output_folder_path': None}
    if n_args > 2:
        testing_arguments_dict['traceback'] = True

        if n_args == 5:
            testing_arguments_dict['tool_path'] = MAIN_FOLDER.parent / 'review/run_tool.py'

    return testing_arguments_dict
