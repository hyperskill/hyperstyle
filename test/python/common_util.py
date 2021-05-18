from pathlib import Path
from typing import List, Tuple

import pandas as pd
from src.python.review.common.file_system import (
    Extension, get_all_file_system_items, match_condition, pair_in_and_out_files,
)


def get_in_and_out_list(root: Path,
                        in_ext: Extension = Extension.CSV,
                        out_ext: Extension = Extension.CSV) -> List[Tuple[Path, Path]]:
    in_files = get_all_file_system_items(root, match_condition(rf'in_\d+{in_ext.value}'))
    out_files = get_all_file_system_items(root, match_condition(rf'out_\d+{out_ext.value}'))
    return pair_in_and_out_files(in_files, out_files)


def equal_df(expected_df: pd.DataFrame, actual_df: pd.DataFrame) -> bool:
    return expected_df.reset_index(drop=True).equals(
        actual_df.reset_index(drop=True)) or (expected_df.empty and actual_df.empty)
