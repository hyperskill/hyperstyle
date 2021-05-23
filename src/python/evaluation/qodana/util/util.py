import json
from typing import Dict, List

import pandas as pd
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue, QodanaJsonField


def to_json(issues: List[QodanaIssue]) -> str:
    issues_json = {
        QodanaJsonField.ISSUES.value: list(map(lambda i: i.to_json(), issues)),
    }
    return json.dumps(issues_json)


# Get a dictionary: Qodana inspection_id -> inspection_id from csv file with two columns: id, inspection_id
def get_inspections_dict(inspections_path: str) -> Dict[str, int]:
    inspections_df = pd.read_csv(inspections_path)
    inspections_dict = inspections_df.set_index(QodanaColumnName.INSPECTION_ID.value).T.to_dict('list')
    for qodana_id, id_list in inspections_dict.items():
        inspections_dict[qodana_id] = id_list[0]
    return inspections_dict


def replace_inspections_on_its_ids(issues_list: List[QodanaIssue], inspections_dict: Dict[str, int]) -> str:
    if len(issues_list) == 0:
        inspections = '0'
    else:
        issues_list.sort(key=lambda x: x.problem_id)
        inspections = ','.join(str(inspections_dict[i.problem_id]) for i in issues_list)
    return inspections
