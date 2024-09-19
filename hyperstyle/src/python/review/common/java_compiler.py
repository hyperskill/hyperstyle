from __future__ import annotations

import logging
import subprocess
from typing import TYPE_CHECKING

from hyperstyle.src.python.review.common.file_system import Encoding, Extension

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


# TODO: it cannot compile gradle-based projects
def javac_project(dir_path: Path) -> bool:
    return javac(f'$(find {dir_path} -name "*{Extension.JAVA.value}")')


def javac(javac_args: str | Path) -> bool:
    try:
        output_bytes: bytes = subprocess.check_output(
            f"javac {javac_args}",
            shell=True,
            stderr=subprocess.STDOUT,
        )
        output_str = str(output_bytes, Encoding.UTF_ENCODING.value)

        if output_str:
            logger.debug(output_str)
    except subprocess.CalledProcessError as error:
        logger.exception(
            f"Failed compile java code with error: " f"{str(error.stdout, Encoding.UTF_ENCODING.value)}"
        )
        return False
    else:
        return True
