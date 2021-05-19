import os
from typing import Optional, Union
from pathlib import Path


def save_labels_csv(input_directory: Union[Path, str], output_directory: Optional[Path] = None) -> Path:
    if output_directory is None:
        output_directory = Path(input_directory).parent

    target_file_path = os.path.join(output_directory, 'target.csv')
    files = os.listdir(input_directory)
    target_file = Path(target_file_path)

    for file in files:
        source_file = Path(input_directory) / file
        with open(target_file, 'a') as t, open(source_file, 'r') as f:
            to_append = f.readlines()
            for line in to_append:
                t.write(line)

    return Path(target_file)
