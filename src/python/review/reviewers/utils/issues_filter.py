from typing import Dict, List

from src.python.review.common.language import Language
from src.python.review.inspectors.issue import BaseIssue, IssueType, Measurable
from src.python.review.quality.rules.boolean_length_scoring import LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG
from src.python.review.quality.rules.class_response_scoring import LANGUAGE_TO_RESPONSE_RULE_CONFIG
from src.python.review.quality.rules.coupling_scoring import LANGUAGE_TO_COUPLING_RULE_CONFIG
from src.python.review.quality.rules.cyclomatic_complexity_scoring import LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG
from src.python.review.quality.rules.function_length_scoring import LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG
from src.python.review.quality.rules.inheritance_depth_scoring import LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG
from src.python.review.quality.rules.method_number_scoring import LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG
from src.python.review.quality.rules.weighted_methods_scoring import LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG


def __get_issue_type_to_low_measure_dict(language: Language) -> Dict[IssueType, int]:
    return {
        IssueType.CYCLOMATIC_COMPLEXITY: LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG[language].cc_value_moderate,
        IssueType.FUNC_LEN: LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG[language].func_len_bad,
        IssueType.BOOL_EXPR_LEN: LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG[language].bool_expr_len_good,
        IssueType.INHERITANCE_DEPTH: LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG[language].depth_bad,
        IssueType.METHOD_NUMBER: LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG[language].method_number_good,
        IssueType.COUPLING: LANGUAGE_TO_COUPLING_RULE_CONFIG[language].coupling_moderate,
        IssueType.CLASS_RESPONSE: LANGUAGE_TO_RESPONSE_RULE_CONFIG[language].response_good,
        IssueType.WEIGHTED_METHOD: LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG[language].weighted_methods_good
    }


def __more_than_low_measure(issue: BaseIssue, issue_type_to_low_measure_dict: Dict[IssueType, int]) -> bool:
    issue_type = issue.type
    if isinstance(issue, Measurable) and issue.measure() <= issue_type_to_low_measure_dict.get(issue_type, -1):
        return False
    return True


def filter_low_measure_issues(issues: List[BaseIssue],
                              language: Language) -> List[BaseIssue]:
    issue_type_to_low_measure_dict = __get_issue_type_to_low_measure_dict(language)

    # Disable this types of issue, requires further investigation.
    ignored_issues = [IssueType.COHESION, IssueType.CHILDREN_NUMBER]

    return list(filter(
        lambda issue: issue.type not in ignored_issues and __more_than_low_measure(issue,
                                                                                   issue_type_to_low_measure_dict),
        issues))


def filter_duplicate_issues(issues: List[BaseIssue]) -> List[BaseIssue]:
    """
    Skipping duplicate issues using heuristic rules
    """
    grouped_issues = group_issues_by_file_line_inspector_and_type(issues)

    selected_issues = []
    for _, issues_in_file in grouped_issues.items():
        for _, issues_in_line in issues_in_file.items():
            # no conflicts -> take all issues found by a single inspector
            if len(issues_in_line) == 1:
                all_issues = [issue for types_by_inspector in issues_in_line.values()
                              for issues_by_type in types_by_inspector.values()
                              for issue in issues_by_type]
                selected_issues.extend(all_issues)
            # conflicts -> take issues found by a more informative inspector
            elif len(issues_in_line) > 1:
                inspectors_by_types = {}
                for inspector, issues_by_types in issues_in_line.items():
                    for issue_type in IssueType:
                        count = len(issues_by_types.get(issue_type, []))
                        if count == 0:
                            continue
                        if issue_type not in inspectors_by_types:
                            inspectors_by_types[issue_type] = ('UNKNOWN', -1)
                        if count > inspectors_by_types[issue_type][1]:
                            inspectors_by_types[issue_type] = (inspector, count)

                for issue_type, inspector in inspectors_by_types.items():
                    selected_issues.extend(issues_in_line[inspector[0]][issue_type])

    return selected_issues


def group_issues_by_file_line_inspector_and_type(issues: List[BaseIssue]) -> dict:
    grouped_issues: Dict[str, Dict[int, Dict[str, Dict[IssueType, List[BaseIssue]]]]] = {}

    for issue in issues:
        file_path = str(issue.file_path)
        if file_path not in grouped_issues:
            grouped_issues[file_path] = {}

        line_no = issue.line_no
        if line_no not in grouped_issues[file_path]:
            grouped_issues[file_path][line_no] = {}

        inspector_name = str(issue.inspector_type)
        if inspector_name not in grouped_issues[file_path][line_no]:
            grouped_issues[file_path][line_no][inspector_name] = {}

        issue_type = issue.type
        if issue_type not in grouped_issues[file_path][line_no][inspector_name]:
            grouped_issues[file_path][line_no][inspector_name][issue_type] = []

        grouped_issues[file_path][line_no][inspector_name][issue_type].append(issue)

    return grouped_issues
