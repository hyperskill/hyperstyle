from __future__ import annotations

import logging
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def run_in_subprocess(
    command: list[str],
    working_directory: str | Path | None = None,
    encoding: str = "utf-8",
    subprocess_input: str | None = None,
) -> str:
    process = subprocess.run(
        command,
        capture_output=True,
        cwd=working_directory,
        encoding=encoding,
        input=subprocess_input,
        check=False,
    )

    stdout = process.stdout
    stderr = process.stderr

    if stdout:
        logger.debug(f"{command[0]}'s stdout:\n{stdout}")
    if stderr:
        logger.debug(f"{command[0]}'s stderr:\n{stderr}")

    return stdout
