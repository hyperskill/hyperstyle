from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List

from review.inspectors.issue import BaseIssue, IssueType


@dataclass
class CodeStatistics:
    n_code_style_issues: int
    n_best_practices_issue: int
    n_error_prone_issues: int
    max_bool_expr_len: int
    max_func_len: int
    n_line_len: int
    max_cyclomatic_complexity: int
    inheritance_depth: int
    class_response: int
    coupling: int
    weighted_method_complexities: int
    method_number: int
    total_lines: int
    code_style_lines: int


def get_total_lines(path):
    lines = open(str(path), 'r').readlines()
    total_lines = 0
    for line in lines:
        if len(line.strip()) > 0 and not line.strip().startswith(('#', '//')):
            total_lines += 1
    return total_lines


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
        issue_type_counter[IssueType.CODE_STYLE],
        issue_type_counter[IssueType.BEST_PRACTICES],
        issue_type_counter[IssueType.ERROR_PRONE],
        max(bool_expr_lens, default=0),
        max(func_lens, default=0),
        issue_type_counter[IssueType.LINE_LEN],
        max(cyclomatic_complexities, default=0),
        max(inheritance_depths, default=0),
        max(class_responses, default=0),
        max(couplings, default=0),
        max(weighted_method_complexities, default=0),
        max(method_numbers, default=0),
        get_total_lines(path),
        get_code_style_lines(issues)
    )
