from collections import defaultdict
from typing import Dict, List, Tuple

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType, Measurable
from hyperstyle.src.python.review.quality.rules.boolean_length_scoring import LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.class_response_scoring import LANGUAGE_TO_RESPONSE_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.cohesion_scoring import LANGUAGE_TO_COHESION_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.coupling_scoring import LANGUAGE_TO_COUPLING_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.cyclomatic_complexity_scoring import (
    LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.function_length_scoring import LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.inheritance_depth_scoring import (
    LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.maintainability_scoring import LANGUAGE_TO_MAINTAINABILITY_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.method_number_scoring import LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.weighted_methods_scoring import LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG


def __get_issue_type_to_low_measure_dict(language: Language) -> Dict[IssueType, int]:
    return {
        IssueType.CYCLOMATIC_COMPLEXITY: LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG[language].cc_value_moderate,
        IssueType.FUNC_LEN: LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG[language].func_len_bad,
        IssueType.BOOL_EXPR_LEN: LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG[language].bool_expr_len_good,
        IssueType.INHERITANCE_DEPTH: LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG[language].depth_bad,
        IssueType.METHOD_NUMBER: LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG[language].method_number_good,
        IssueType.COUPLING: LANGUAGE_TO_COUPLING_RULE_CONFIG[language].coupling_moderate,
        IssueType.CLASS_RESPONSE: LANGUAGE_TO_RESPONSE_RULE_CONFIG[language].response_good,
        IssueType.WEIGHTED_METHOD: LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG[language].weighted_methods_good,
        IssueType.COHESION: LANGUAGE_TO_COHESION_RULE_CONFIG[language].cohesion_lack_good,
        IssueType.MAINTAINABILITY: LANGUAGE_TO_MAINTAINABILITY_RULE_CONFIG[
            language
        ].maintainability_lack_good,
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
    ignored_issues = [IssueType.CHILDREN_NUMBER]

    return list(filter(
        lambda issue: issue.type not in ignored_issues and __more_than_low_measure(issue,
                                                                                   issue_type_to_low_measure_dict),
        issues))


FilePath = str
LinesNumber = int
Inspector = str
GroupedIssues = Dict[FilePath, Dict[LinesNumber, Dict[Inspector, Dict[IssueType, List[BaseIssue]]]]]


def __init_grouped_issues() -> GroupedIssues:
    return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: []))))


def filter_duplicate_issues(issues: List[BaseIssue]) -> List[BaseIssue]:
    """
    Skipping duplicate issues using heuristic rules:

    For each line's number try to count issues with unique type for each unique inspector and select the best one.
    The inspector with the biggest number of issues for each type will be chosen.
    """
    grouped_issues = group_issues(issues)

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
                default_inspector = 'UNKNOWN'
                # By default for each <IssueType> we add the tuple (inspector: 'UNKNOWN', issue_type_freq: -1)
                inspectors_by_types: Dict[IssueType, Tuple[Inspector, int]] = defaultdict(
                    lambda: (default_inspector, -1))
                for inspector, issues_by_types in issues_in_line.items():
                    # Handle all possible issue types
                    for issue_type in IssueType:
                        issue_type_freq = len(issues_by_types.get(issue_type, []))
                        # This <issue_type> was not find by the <inspector>
                        if issue_type_freq == 0:
                            continue
                        max_issue_type_freq = inspectors_by_types[issue_type][1]
                        # Current inspector has more issues with type <issue_type> than previous ones
                        if issue_type_freq > max_issue_type_freq:
                            inspectors_by_types[issue_type] = (inspector, issue_type_freq)

                for issue_type, inspector_to_freq in inspectors_by_types.items():
                    inspector = inspector_to_freq[0]
                    if inspector != default_inspector:
                        selected_issues.extend(issues_in_line[inspector][issue_type])

    return selected_issues


def group_issues(issues: List[BaseIssue]) -> GroupedIssues:
    """
    Group issues according to the following structure:
    - FILE_PATH:
        - LINES_NUMBER:
            - INSPECTOR:
                - ISSUE_TYPE:
                    [ISSUES]

    We will consider each file to find potential duplicates:
    if one line number in the file contains several same issues which were found by different inspectors,
    we will try to find the best one. See <filter_duplicate_issues> function.
    """
    grouped_issues: GroupedIssues = __init_grouped_issues()

    for issue in issues:
        file_path = str(issue.file_path)
        line_no = issue.line_no
        inspector_name = str(issue.inspector_type)
        issue_type = issue.type

        grouped_issues[file_path][line_no][inspector_name][issue_type].append(issue)

    return grouped_issues


def group_issues_by_difficulty(issues: List[BaseIssue]) -> Dict[IssueDifficulty, List[BaseIssue]]:
    return {
        IssueDifficulty.EASY: [issue for issue in issues if issue.difficulty == IssueDifficulty.EASY],
        IssueDifficulty.MEDIUM: [issue for issue in issues if issue.difficulty != IssueDifficulty.HARD],
        IssueDifficulty.HARD: issues,
    }
