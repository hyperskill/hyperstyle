from typing import Dict

from review.common.language import Language
from review.inspectors.issue import IssueType
from review.quality.model import Quality
from review.quality.rules.best_practices_scoring import (
    BestPracticesRule, LANGUAGE_TO_BEST_PRACTICES_RULE_CONFIG
)
from review.quality.rules.boolean_length_scoring import (
    BooleanExpressionRule, LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG
)
from review.quality.rules.class_response_scoring import (
    LANGUAGE_TO_RESPONSE_RULE_CONFIG, ResponseRule
)
from review.quality.rules.code_style_scoring import (
    CodeStyleRule, LANGUAGE_TO_CODE_STYLE_RULE_CONFIG
)
from review.quality.rules.coupling_scoring import (
    CouplingRule, LANGUAGE_TO_COUPLING_RULE_CONFIG
)
from review.quality.rules.cyclomatic_complexity_scoring import (
    CyclomaticComplexityRule, LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG
)
from review.quality.rules.error_prone_scoring import (
    ErrorProneRule, LANGUAGE_TO_ERROR_PRONE_RULE_CONFIG
)
from review.quality.rules.function_length_scoring import (
    FunctionLengthRule, LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG
)
from review.quality.rules.inheritance_depth_scoring import (
    InheritanceDepthRule, LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG
)
from review.quality.rules.line_len_scoring import (
    LANGUAGE_TO_LINE_LENGTH_RULE_CONFIG, LineLengthRule
)
from review.quality.rules.method_number_scoring import (
    LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG, MethodNumberRule
)
from review.quality.rules.weighted_methods_scoring import (
    LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG, WeightedMethodsRule
)
from review.reviewers.utils.code_statistics import CodeStatistics


def get_statistics(statistics: CodeStatistics) -> Dict[IssueType, int]:
    rule_type_counter = {
        IssueType.CODE_STYLE:
            statistics.code_style_lines,

        IssueType.BEST_PRACTICES:
            statistics.n_best_practices_issue,

        IssueType.ERROR_PRONE:
            statistics.n_error_prone_issues,

        IssueType.CYCLOMATIC_COMPLEXITY:
            statistics.max_cyclomatic_complexity,

        IssueType.FUNC_LEN:
            statistics.max_func_len,

        IssueType.LINE_LEN:
            statistics.n_line_len,

        IssueType.BOOL_EXPR_LEN:
            statistics.max_bool_expr_len,

        IssueType.INHERITANCE_DEPTH:
            statistics.inheritance_depth,

        IssueType.METHOD_NUMBER:
            statistics.method_number,

        IssueType.COUPLING:
            statistics.coupling,

        IssueType.CLASS_RESPONSE:
            statistics.class_response,

        IssueType.WEIGHTED_METHOD:
            statistics.weighted_method_complexities
    }
    return rule_type_counter


def evaluate_quality(statistics: CodeStatistics, language: Language) -> Quality:
    rule_statistics = get_statistics(statistics)

    rules = [
        ErrorProneRule(LANGUAGE_TO_ERROR_PRONE_RULE_CONFIG[language]),
        BestPracticesRule(LANGUAGE_TO_BEST_PRACTICES_RULE_CONFIG[language]),
        CyclomaticComplexityRule(LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG[language]),
        BooleanExpressionRule(LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG[language]),
        FunctionLengthRule(LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG[language]),
        InheritanceDepthRule(LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG[language]),
        MethodNumberRule(LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG[language]),
        CouplingRule(LANGUAGE_TO_COUPLING_RULE_CONFIG[language]),
        ResponseRule(LANGUAGE_TO_RESPONSE_RULE_CONFIG[language]),
        WeightedMethodsRule(LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG[language])
    ]

    for rule in rules:
        rule.apply(rule_statistics[rule.rule_type])

    code_style_rule = CodeStyleRule(LANGUAGE_TO_CODE_STYLE_RULE_CONFIG[language])
    code_style_rule.apply(rule_statistics[IssueType.CODE_STYLE],
                          statistics.n_code_style_issues, statistics.total_lines)
    rules.append(code_style_rule)

    line_len_rule = LineLengthRule(LANGUAGE_TO_LINE_LENGTH_RULE_CONFIG[language])
    line_len_rule.apply(rule_statistics[IssueType.LINE_LEN], statistics.total_lines)
    rules.append(line_len_rule)

    return Quality(rules)
