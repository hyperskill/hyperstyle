import json
import textwrap
from pathlib import Path

import pytest
from src.python.evaluation.issues_statistics.common.raw_issue_encoder_decoder import RawIssueDecoder, RawIssueEncoder
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import (
    BaseIssue,
    BoolExprLenIssue,
    CodeIssue,
    CohesionIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueDifficulty,
    IssueType,
    LineLenIssue,
    MaintainabilityLackIssue,
)

FILE_PATH = 'some_file.py'
DESCRIPTION = 'Some description'

ISSUE_AND_JSON_ISSUE = [
    (
        CodeIssue(
            origin_class='SomeCodeIssueClass',
            type=IssueType.CODE_STYLE,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=656,
            column_no=42,
            inspector_type=InspectorType.CHECKSTYLE,
            difficulty=IssueDifficulty.EASY,
        ),
        f"""
        {{
            "origin_class": "SomeCodeIssueClass",
            "type": "CODE_STYLE",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 656,
            "column_no": 42,
            "inspector_type": "CHECKSTYLE",
            "difficulty": "EASY"
        }}
        """,
    ),
    (
        BoolExprLenIssue(
            origin_class='SomeBoolExprLenIssueClass',
            type=IssueType.BOOL_EXPR_LEN,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=983,
            column_no=428,
            inspector_type=InspectorType.DETEKT,
            bool_expr_len=975,
            difficulty=IssueDifficulty.EASY,
        ),
        f"""
        {{
            "origin_class": "SomeBoolExprLenIssueClass",
            "type": "BOOL_EXPR_LEN",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 983,
            "column_no": 428,
            "inspector_type": "DETEKT",
            "difficulty": "EASY",
            "measure": 975
        }}
        """,
    ),
    (
        FuncLenIssue(
            origin_class='SomeFuncLenIssueClass',
            type=IssueType.FUNC_LEN,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=790,
            column_no=487,
            inspector_type=InspectorType.ESLINT,
            func_len=909,
            difficulty=IssueDifficulty.EASY,
        ),
        f"""
        {{
            "origin_class": "SomeFuncLenIssueClass",
            "type": "FUNC_LEN",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 790,
            "column_no": 487,
            "inspector_type": "ESLINT",
            "difficulty": "EASY",
            "measure": 909
        }}
        """,
    ),
    (
        LineLenIssue(
            origin_class='SomeLineLenIssueClass',
            type=IssueType.LINE_LEN,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=154,
            column_no=383,
            inspector_type=InspectorType.PMD,
            line_len=383,
            difficulty=IssueDifficulty.EASY,
        ),
        f"""
        {{
            "origin_class": "SomeLineLenIssueClass",
            "type": "LINE_LEN",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 154,
            "column_no": 383,
            "inspector_type": "PMD",
            "difficulty": "EASY",
            "measure": 383
        }}
        """,
    ),
    (
        CyclomaticComplexityIssue(
            origin_class='SomeCyclomaticComplexityIssueClass',
            type=IssueType.CYCLOMATIC_COMPLEXITY,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=670,
            column_no=78,
            inspector_type=InspectorType.INTELLIJ,
            cc_value=229,
            difficulty=IssueDifficulty.HARD,
        ),
        f"""
        {{
            "origin_class": "SomeCyclomaticComplexityIssueClass",
            "type": "CYCLOMATIC_COMPLEXITY",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 670,
            "column_no": 78,
            "inspector_type": "INTELLIJ",
            "difficulty": "HARD",
            "measure": 229
        }}
        """,
    ),
    (
        CohesionIssue(
            origin_class='SomeCohesionIssueClass',
            type=IssueType.COHESION,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=997,
            column_no=386,
            inspector_type=InspectorType.PYLINT,
            cohesion_lack=564,
            difficulty=IssueDifficulty.HARD,
        ),
        f"""
        {{
            "origin_class": "SomeCohesionIssueClass",
            "type": "COHESION",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 997,
            "column_no": 386,
            "inspector_type": "PYLINT",
            "difficulty": "HARD",
            "measure": 564
        }}
        """,
    ),
    (
        MaintainabilityLackIssue(
            origin_class='SomeMaintainabilityLackIssueClass',
            type=IssueType.MAINTAINABILITY,
            description=DESCRIPTION,
            file_path=Path(FILE_PATH),
            line_no=830,
            column_no=542,
            inspector_type=InspectorType.RADON,
            maintainability_lack=431,
            difficulty=IssueDifficulty.HARD,
        ),
        f"""
        {{
            "origin_class": "SomeMaintainabilityLackIssueClass",
            "type": "MAINTAINABILITY",
            "description": "{DESCRIPTION}",
            "file_path": "{FILE_PATH}",
            "line_no": 830,
            "column_no": 542,
            "inspector_type": "RADON",
            "difficulty": "HARD",
            "measure": 431
        }}
        """,
    ),
]


@pytest.mark.parametrize(('issue', 'expected_json'), ISSUE_AND_JSON_ISSUE)
def test_encode_issue(issue: BaseIssue, expected_json: str):
    assert json.dumps(issue, cls=RawIssueEncoder, indent=4) == textwrap.dedent(expected_json).strip()


@pytest.mark.parametrize(('expected_issue', 'json_issue'), ISSUE_AND_JSON_ISSUE)
def test_decode_issue(json_issue: str, expected_issue: BaseIssue):
    assert json.loads(json_issue, cls=RawIssueDecoder) == expected_issue


@pytest.mark.parametrize(('issue', 'json_issue'), ISSUE_AND_JSON_ISSUE)
def test_encode_decode(issue: BaseIssue, json_issue: str):
    assert json.loads(json.dumps(issue, cls=RawIssueEncoder), cls=RawIssueDecoder) == issue


@pytest.mark.parametrize(('issue', 'json_issue'), ISSUE_AND_JSON_ISSUE)
def test_decode_encode(issue: BaseIssue, json_issue: str):
    assert (
        json.dumps(json.loads(json_issue, cls=RawIssueDecoder), cls=RawIssueEncoder, indent=4)
        == textwrap.dedent(json_issue).strip()
    )
