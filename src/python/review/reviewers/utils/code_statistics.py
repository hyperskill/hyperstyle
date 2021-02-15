from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from src.python.review.common.file_system import get_content_from_file
from src.python.review.inspectors.issue import BaseIssue, IssueType


@dataclass
class CodeStatistics:
    n_best_practices_issue: int
    n_error_prone_issues: int
    n_line_len: int

    method_number: int

    max_cyclomatic_complexity: int
    max_func_len: int
    max_bool_expr_len: int

    code_style_lines: int
    inheritance_depth: int
    coupling: int
    class_response: int
    weighted_method_complexities: int

    n_code_style_issues: int
    total_lines: int

    @property
    def issue_type_to_statistics_dict(self) -> Dict[IssueType, int]:
        return {
            IssueType.BEST_PRACTICES: self.n_best_practices_issue,
            IssueType.ERROR_PRONE: self.n_error_prone_issues,
            IssueType.LINE_LEN: self.n_line_len,

            IssueType.METHOD_NUMBER: self.method_number,

            IssueType.CYCLOMATIC_COMPLEXITY: self.max_cyclomatic_complexity,
            IssueType.FUNC_LEN: self.max_func_len,
            IssueType.BOOL_EXPR_LEN: self.max_bool_expr_len,

            IssueType.CODE_STYLE: self.code_style_lines,
            IssueType.INHERITANCE_DEPTH: self.inheritance_depth,
            IssueType.COUPLING: self.coupling,
            IssueType.CLASS_RESPONSE: self.class_response,
            IssueType.WEIGHTED_METHOD: self.weighted_method_complexities
        }


def __get_total_lines(path: Path) -> int:
    lines = get_content_from_file(path, to_strip_nl=False).splitlines()
    return len(list(filter(lambda line: not __is_empty(line) and not __is_comment(line), lines)))


def __is_empty(line: str) -> bool:
    return len(line.strip()) == 0


def __is_comment(line: str) -> bool:
    return line.strip().startswith(('#', '//'))


def get_code_style_lines(issues: List[BaseIssue]) -> int:
    code_style_issues = filter(lambda issue: issue.type == IssueType.CODE_STYLE, issues)
    line_counter = Counter([issue.line_no for issue in code_style_issues])
    return len(line_counter)


# TODO: Need testing
def gather_code_statistics(issues: List[BaseIssue], path: Path) -> CodeStatistics:
    issue_type_counter = Counter([issue.type for issue in issues])

    bool_expr_lens = map(
        lambda issue: issue.bool_expr_len,
        filter(lambda issue: issue.type == IssueType.BOOL_EXPR_LEN, issues)
    )
    func_lens = map(
        lambda issue: issue.func_len,
        filter(lambda issue: issue.type == IssueType.FUNC_LEN, issues)
    )

    cyclomatic_complexities = map(
        lambda issue: issue.cc_value,
        filter(lambda issue: issue.type == IssueType.CYCLOMATIC_COMPLEXITY, issues)
    )

    # Actually, we expect only one issue with each of the following metrics.

    inheritance_depths = map(
        lambda issue: issue.inheritance_tree_depth,
        filter(lambda issue: issue.type == IssueType.INHERITANCE_DEPTH, issues)
    )

    class_responses = map(
        lambda issue: issue.class_response,
        filter(lambda issue: issue.type == IssueType.CLASS_RESPONSE, issues)
    )

    couplings = map(
        lambda issue: issue.class_objects_coupling,
        filter(lambda issue: issue.type == IssueType.COUPLING, issues)
    )

    weighted_method_complexities = map(
        lambda issue: issue.weighted_method,
        filter(lambda issue: issue.type == IssueType.WEIGHTED_METHOD, issues)
    )

    method_numbers = map(
        lambda issue: issue.method_number,
        filter(lambda issue: issue.type == IssueType.METHOD_NUMBER, issues)
    )

    return CodeStatistics(
        n_code_style_issues=issue_type_counter[IssueType.CODE_STYLE],
        n_best_practices_issue=issue_type_counter[IssueType.BEST_PRACTICES],
        n_error_prone_issues=issue_type_counter[IssueType.ERROR_PRONE],
        max_bool_expr_len=max(bool_expr_lens, default=0),
        max_func_len=max(func_lens, default=0),
        n_line_len=issue_type_counter[IssueType.LINE_LEN],
        max_cyclomatic_complexity=max(cyclomatic_complexities, default=0),
        inheritance_depth=max(inheritance_depths, default=0),
        class_response=max(class_responses, default=0),
        coupling=max(couplings, default=0),
        weighted_method_complexities=max(weighted_method_complexities, default=0),
        method_number=max(method_numbers, default=0),
        total_lines=__get_total_lines(path),
        code_style_lines=get_code_style_lines(issues)
    )
