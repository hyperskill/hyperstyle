import json
from pathlib import Path

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import (
    BaseIssue,
    BoolExprLenIssue,
    CodeIssue,
    CohesionIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueData,
    IssueType,
    LineLenIssue,
    MaintainabilityLackIssue,
    Measurable,
)

MEASURE = 'measure'


class RawIssueEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseIssue):
            issue_data = {
                IssueData.ORIGIN_ClASS.value: obj.origin_class,
                IssueData.ISSUE_TYPE.value: obj.type.value,
                IssueData.DESCRIPTION.value: obj.description,
                IssueData.FILE_PATH.value: str(obj.file_path),
                IssueData.LINE_NUMBER.value: obj.line_no,
                IssueData.COLUMN_NUMBER.value: obj.column_no,
                IssueData.INSPECTOR_TYPE.value: obj.inspector_type.value,
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

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.BOOL_EXPR_LEN:
            json_dict[IssueData.BOOL_EXPR_LEN.value] = json_dict.pop(MEASURE)
            return BoolExprLenIssue(**json_dict)

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.FUNC_LEN:
            json_dict[IssueData.FUNCTION_LEN.value] = json_dict.pop(MEASURE)
            return FuncLenIssue(**json_dict)

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.LINE_LEN:
            json_dict[IssueData.LINE_LEN.value] = json_dict.pop(MEASURE)
            return LineLenIssue(**json_dict)

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.CYCLOMATIC_COMPLEXITY:
            json_dict[IssueData.CYCLOMATIC_COMPLEXITY.value] = json_dict.pop(MEASURE)
            return CyclomaticComplexityIssue(**json_dict)

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.COHESION:
            json_dict[IssueData.COHESION_LACK.value] = json_dict.pop(MEASURE)
            return CohesionIssue(**json_dict)

        if json_dict[IssueData.ISSUE_TYPE.value] == IssueType.MAINTAINABILITY:
            json_dict[IssueData.MAINTAINABILITY_LACK.value] = json_dict.pop(MEASURE)
            return MaintainabilityLackIssue(**json_dict)

        return CodeIssue(**json_dict)
