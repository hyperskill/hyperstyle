from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from hyperstyle.src.python.review.common.file_system import get_total_code_lines_from_file
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueType


@dataclass
class CodeStatistics:
    n_best_practices_issue: int
    n_error_prone_issues: int
    n_complexity_issues: int
    n_line_len: int

    method_number: int

    max_cyclomatic_complexity: int
    max_cohesion_lack: int
    max_maintainability_lack: int
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
            IssueType.COMPLEXITY: self.n_complexity_issues,
            IssueType.LINE_LEN: self.n_line_len,

            IssueType.METHOD_NUMBER: self.method_number,

            IssueType.CYCLOMATIC_COMPLEXITY: self.max_cyclomatic_complexity,
            IssueType.COHESION: self.max_cohesion_lack,
            IssueType.MAINTAINABILITY: self.max_maintainability_lack,
            IssueType.FUNC_LEN: self.max_func_len,
            IssueType.BOOL_EXPR_LEN: self.max_bool_expr_len,

            IssueType.CODE_STYLE: self.code_style_lines,
            IssueType.INHERITANCE_DEPTH: self.inheritance_depth,
            IssueType.COUPLING: self.coupling,
            IssueType.CLASS_RESPONSE: self.class_response,
            IssueType.WEIGHTED_METHOD: self.weighted_method_complexities,
        }


def get_code_style_lines(issues: List[BaseIssue]) -> int:
    code_style_issues = filter(lambda issue: issue.type == IssueType.CODE_STYLE, issues)
    line_counter = Counter([issue.line_no for issue in code_style_issues])
    return len(line_counter)


def __get_max_measure_by_issue_type(issue_type: IssueType, issues: List[BaseIssue]) -> int:
    return max(map(
        lambda issue: issue.measure(),
        filter(lambda issue: issue.type == issue_type, issues),
    ), default=0)


# TODO: Need testing
def gather_code_statistics(issues: List[BaseIssue], path: Path) -> CodeStatistics:
    issue_type_counter = Counter([issue.type for issue in issues])

    bool_expr_lens = __get_max_measure_by_issue_type(IssueType.BOOL_EXPR_LEN, issues)
    func_lens = __get_max_measure_by_issue_type(IssueType.FUNC_LEN, issues)
    cyclomatic_complexities = __get_max_measure_by_issue_type(IssueType.CYCLOMATIC_COMPLEXITY, issues)
    cohesion_lacks = __get_max_measure_by_issue_type(IssueType.COHESION, issues)
    maintainabilities = __get_max_measure_by_issue_type(IssueType.MAINTAINABILITY, issues)

    # Actually, we expect only one issue with each of the following metrics.
    inheritance_depths = __get_max_measure_by_issue_type(IssueType.INHERITANCE_DEPTH, issues)
    class_responses = __get_max_measure_by_issue_type(IssueType.CLASS_RESPONSE, issues)
    couplings = __get_max_measure_by_issue_type(IssueType.COUPLING, issues)
    weighted_method_complexities = __get_max_measure_by_issue_type(IssueType.WEIGHTED_METHOD, issues)
    method_numbers = __get_max_measure_by_issue_type(IssueType.METHOD_NUMBER, issues)

    return CodeStatistics(
        n_code_style_issues=issue_type_counter[IssueType.CODE_STYLE],
        n_best_practices_issue=issue_type_counter[IssueType.BEST_PRACTICES],
        n_error_prone_issues=issue_type_counter[IssueType.ERROR_PRONE],
        n_complexity_issues=issue_type_counter[IssueType.COMPLEXITY],
        max_bool_expr_len=bool_expr_lens,
        max_func_len=func_lens,
        n_line_len=issue_type_counter[IssueType.LINE_LEN],
        max_cohesion_lack=cohesion_lacks,
        max_maintainability_lack=maintainabilities,
        max_cyclomatic_complexity=cyclomatic_complexities,
        inheritance_depth=inheritance_depths,
        class_response=class_responses,
        coupling=couplings,
        weighted_method_complexities=weighted_method_complexities,
        method_number=method_numbers,
        total_lines=get_total_code_lines_from_file(path),
        code_style_lines=get_code_style_lines(issues),
    )
