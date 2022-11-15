import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.ij.model import IJCode, IJInspectionResult
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue

LANGUAGE_TO_ID = {
    Language.PYTHON: "Python",
}

CODE_SERVER_HOST = "CODE_SERVER_HOST"
CODE_SERVER_PORT = "CODE_SERVER_PORT"
CODE_SERVER_ROOT = "CODE_SERVER_ROOT"

logger = logging.getLogger(__name__)


class IJInspector(BaseInspector):
    inspector_type = InspectorType.IJ

    def __init__(self, language: Language):
        self.host = os.environ.get(CODE_SERVER_HOST, "0.0.0.0")
        self.port = os.environ.get(CODE_SERVER_PORT, 8080)
        self.root = os.environ.get(CODE_SERVER_PORT, "code/server/api/v1/")
        self.languageId = LANGUAGE_TO_ID[language]

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        with open(path, "r") as code_file:
            code = code_file.read()

        return self.inspect_in_memory(code, config)

    def inspect_in_memory(self, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        try:
            response = requests.get(
                f"http://{self.host}:{self.port}/{self.root}inspect",
                headers={"Content-Type": "application/json"},
                data=IJCode(code, self.languageId).to_json(),
            )

            if response.status_code != 200:
                # TODO: replace with error when ass mock server into tests
                logger.info('Inspector failed to connect to code server.', response)
                return []

            return IJInspectionResult.from_json(response.text).to_base_issues()

        except Exception as e:
            # TODO: replace with error when ass mock server into tests
            logger.info('Inspector failed to connect to code server.', e)
            return []
