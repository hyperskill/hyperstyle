import logging
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def run_in_subprocess(command: List[str]) -> str:
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout = process.stdout.decode()
    stderr = process.stderr.decode()

    if stdout:
        logger.debug('%s\'s stdout:\n%s' % (command[0], stdout))
    if stderr:
        logger.debug('%s\'s stderr:\n%s' % (command[0], stderr))

    return stdout
