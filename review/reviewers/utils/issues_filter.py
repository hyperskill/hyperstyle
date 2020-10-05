from typing import Dict, List

from review.common.language import Language
from review.inspectors.issue import BaseIssue, IssueType
from review.quality.evaluate_quality import (
    LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG,
    LANGUAGE_TO_COUPLING_RULE_CONFIG,
    LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG,
    LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG,
    LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG,
    LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG,
    LANGUAGE_TO_RESPONSE_RULE_CONFIG,
    LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG
)


def filter_low_metric_issues(issues: List[BaseIssue],
                             language: Language) -> List[BaseIssue]:
    filtered_issues = []

    func_len_rule_config = LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG[language]
    boolean_expression_rule_config = LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG[language]
    cyclomatic_complexity_rule_config = LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG[language]
    inheritance_depth_rule_config = LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG[language]
    method_number_rule_config = LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG[language]
    coupling_rule_config = LANGUAGE_TO_COUPLING_RULE_CONFIG[language]
    response_rule_config = LANGUAGE_TO_RESPONSE_RULE_CONFIG[language]
    weighted_methods_rule_config = LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG[language]

    # TODO make an abstraction for extraction the value
    for issue in issues:
        if (issue.type == IssueType.CYCLOMATIC_COMPLEXITY and
                issue.cc_value <= cyclomatic_complexity_rule_config.cc_value_moderate):
            continue

        if (issue.type == IssueType.FUNC_LEN and
                issue.func_len <= func_len_rule_config.func_len_bad):
            continue

        if (issue.type == IssueType.BOOL_EXPR_LEN and
                issue.bool_expr_len <= boolean_expression_rule_config.bool_expr_len_good):
            continue

        if (issue.type == IssueType.INHERITANCE_DEPTH and
                issue.inheritance_tree_depth <= inheritance_depth_rule_config.depth_bad):
            continue

        if (issue.type == IssueType.METHOD_NUMBER and
                issue.method_number <= method_number_rule_config.method_number_good):
            continue

        if (issue.type == IssueType.CLASS_RESPONSE and
                issue.class_response <= response_rule_config.response_good):
            continue

        if (issue.type == IssueType.WEIGHTED_METHOD and
                issue.weighted_method <= weighted_methods_rule_config.weighted_methods_good):
            continue

        if (issue.type == IssueType.COUPLING and
                issue.class_objects_coupling <= coupling_rule_config.coupling_moderate):
            continue

        # Disable this types of issue, requires further investigation.
        if (issue.type == IssueType.COHESION or
                issue.type == IssueType.CHILDREN_NUMBER):
            continue

        filtered_issues.append(issue)

    return filtered_issues


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
