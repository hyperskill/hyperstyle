import json
from typing import List

from src.python.evaluation.qodana.util.models import QodanaIssue, QodanaJsonField


def to_json(issues: List[QodanaIssue]) -> str:
    issues_json = {
        QodanaJsonField.ISSUES.value: list(map(lambda i: i.to_json(), issues)),
    }
    return json.dumps(issues_json)
