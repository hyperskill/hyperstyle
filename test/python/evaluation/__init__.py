from test.python import TEST_DATA_FOLDER

from src.python import MAIN_FOLDER

CURRENT_TEST_DATA_FOLDER = TEST_DATA_FOLDER / 'evaluation'

XLSX_DATA_FOLDER = CURRENT_TEST_DATA_FOLDER / 'xlsx_files'

TARGET_XLSX_DATA_FOLDER = CURRENT_TEST_DATA_FOLDER / 'xlsx_target_files'

RESULTS_DIR_PATH = MAIN_FOLDER.parent / 'evaluation/results'
