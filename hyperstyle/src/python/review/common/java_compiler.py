import logging
import subprocess
from pathlib import Path
from typing import Union

from hyperstyle.src.python.review.common.file_system import Encoding, Extension

logger = logging.getLogger(__name__)


# TODO it cannot compile gradle-based projects
def javac_project(dir_path: Path) -> bool:
    return javac(f'$(find {dir_path} -name "*{Extension.JAVA.value}")')


def javac(javac_args: Union[str, Path]) -> bool:
    try:
        output_bytes: bytes = subprocess.check_output(
            f'javac {javac_args}',
            shell=True,
            stderr=subprocess.STDOUT,
        )
        output_str = str(output_bytes, Encoding.UTF_ENCODING.value)

        if output_str:
            logger.debug(output_str)

        return True
    except subprocess.CalledProcessError as error:
        logger.error(f'Failed compile java code with error: '
                     f'{str(error.stdout, Encoding.UTF_ENCODING.value)}')
        return False
