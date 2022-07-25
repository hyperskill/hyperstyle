import logging
import subprocess
from pathlib import Path
from typing import List, Optional, Union

logger = logging.getLogger(__name__)


def run_in_subprocess(command: List[str], working_directory: Optional[Union[str, Path]] = None) -> str:
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_directory,
    )

    stdout = process.stdout.decode()
    stderr = process.stderr.decode()

    if stdout:
        logger.debug('%s\'s stdout:\n%s' % (command[0], stdout))
    if stderr:
        logger.debug('%s\'s stderr:\n%s' % (command[0], stderr))

    return stdout
