from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.python.review.common.file_system import new_temp_dir
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.reviewers.utils.metadata_exploration import explore_file, FileMetadata


@pytest.fixture
def branch_info_response() -> Dict[str, Any]:
    response = {
        'result': {
            'commitsCount': 1,
            'filesCount': 1,
            'branchingRevision': 'foo',
            'headRevision': {
                'projectId': 'foo',
                'revisionId': 'foo',
                'revisionDate': 1,
                'effectiveRevisionDate': 1,
                'revisionCommitMessage': 'foo',
                'state': 1,
                'vcsRevisionId': 1,
                'shortRevisionId': 'foo',
                'authorId': 'foo',
                'reachability': 1,
            },
            'canCreateReview': {
                'isAllowed': True
            },
            'stats': {
                'parentBranch': 'bar',
                'commitsAhead': 0,
                'commitsBehind': 0
            },
            'mergeInfo': {},
            'isPullRequest': False
        }
    }

    return response


@pytest.fixture
def ownership_summary_response() -> Dict[str, Any]:
    response = {
        'result': {
            'files': [
                {
                    'filePath': '/foo.py',
                    'state': 0,
                    'userId': None
                },
                {
                    'filePath': '/bar/baz.py',
                    'state': 0,
                    'userId': None
                }
            ]
        }
    }

    return response


@dataclass(frozen=True)
class IssuesTestInfo:
    n_code_style: int = 0
    n_best_practices: int = 0
    n_error_prone: int = 0
    n_func_len: int = 0
    n_cc: int = 0
    n_bool_expr_len: int = 0
    n_other_complexity: int = 0


def gather_issues_test_info(issues: List[BaseIssue]) -> IssuesTestInfo:
    counter = Counter([issue.type for issue in issues])

    return IssuesTestInfo(
        n_code_style=counter[IssueType.CODE_STYLE],
        n_best_practices=counter[IssueType.BEST_PRACTICES],
        n_error_prone=counter[IssueType.ERROR_PRONE],
        n_func_len=counter[IssueType.FUNC_LEN],
        n_cc=counter[IssueType.CYCLOMATIC_COMPLEXITY],
        n_bool_expr_len=counter[IssueType.BOOL_EXPR_LEN],
        n_other_complexity=counter[IssueType.COMPLEXITY]
    )


@contextmanager
def use_file_metadata(file_path: Path) -> FileMetadata:
    with new_temp_dir() as temp_dir:
        new_file_path = temp_dir / file_path.name

        text = file_path.read_text()
        new_file_path.write_text(text)

        file_target = explore_file(new_file_path)

        yield file_target
