import json
from pathlib import Path

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import (
    BaseIssue,
    CodeIssue,
    get_issue_class_by_issue_type,
    IssueData,
    IssueDifficulty,
    IssueType,
    Measurable,
    MEASURABLE_ISSUE_TYPE_TO_MEASURE_NAME,
)

MEASURE = 'measure'


class RawIssueEncoder(json.JSONEncoder):
    to_safe_path: bool

    def __init__(self, to_safe_path: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.to_safe_path = to_safe_path

    def default(self, obj):
        if isinstance(obj, BaseIssue):
            issue_data = {
                IssueData.ORIGIN_ClASS.value: obj.origin_class,
                IssueData.ISSUE_TYPE.value: obj.type.value,
                IssueData.DESCRIPTION.value: obj.description,
                IssueData.FILE_PATH.value: str(obj.file_path) if self.to_safe_path else "",
                IssueData.LINE_NUMBER.value: obj.line_no,
                IssueData.COLUMN_NUMBER.value: obj.column_no,
                IssueData.INSPECTOR_TYPE.value: obj.inspector_type.value,
                IssueData.DIFFICULTY.value: obj.difficulty.value,
            }

            if isinstance(obj, Measurable):
                issue_data[MEASURE] = obj.measure()

            return issue_data

        return json.JSONEncoder.default(self, obj)


class RawIssueDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, json_dict):
        json_dict[IssueData.ISSUE_TYPE.value] = IssueType(json_dict[IssueData.ISSUE_TYPE.value])
        json_dict[IssueData.INSPECTOR_TYPE.value] = InspectorType(json_dict[IssueData.INSPECTOR_TYPE.value])
        json_dict[IssueData.FILE_PATH.value] = Path(json_dict[IssueData.FILE_PATH.value])
        # TODO: remove get after analyzing raw issue statistics
        json_dict[IssueData.DIFFICULTY.value] = IssueDifficulty(
            json_dict.get(IssueData.DIFFICULTY.value, IssueDifficulty.HARD.value),
        )

        issue_type = json_dict[IssueData.ISSUE_TYPE.value]
        if issue_type in MEASURABLE_ISSUE_TYPE_TO_MEASURE_NAME.keys():
            measure_name = MEASURABLE_ISSUE_TYPE_TO_MEASURE_NAME[issue_type]
            json_dict[measure_name] = json_dict.pop(MEASURE)
            measurable_issue_class = get_issue_class_by_issue_type(issue_type)
            return measurable_issue_class(**json_dict)

        return CodeIssue(**json_dict)
