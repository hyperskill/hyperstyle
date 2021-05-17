from pathlib import Path
from typing import Union

import pandas as pd

from src.python.review.common.file_system import Encoding


def write_dataframe_to_csv(csv_file_path: Union[str, Path], df: pd.DataFrame) -> None:
    df.to_csv(csv_file_path, encoding=Encoding.ISO_ENCODING.value, index=False)