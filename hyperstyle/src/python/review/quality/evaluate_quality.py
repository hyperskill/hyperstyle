from typing import List

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import Quality, Rule
from hyperstyle.src.python.review.quality.rules.best_practices_scoring import (
    BestPracticesRule,
    LANGUAGE_TO_BEST_PRACTICES_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.boolean_length_scoring import (
    BooleanExpressionRule,
    LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.class_response_scoring import (
    LANGUAGE_TO_RESPONSE_RULE_CONFIG, ResponseRule,
)
from hyperstyle.src.python.review.quality.rules.code_style_scoring import (
    CodeStyleRule, LANGUAGE_TO_CODE_STYLE_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.cohesion_scoring import (
    CohesionRule,
    LANGUAGE_TO_COHESION_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.complexity_scoring import (
    ComplexityRule, LANGUAGE_TO_COMPLEXITY_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.coupling_scoring import CouplingRule, LANGUAGE_TO_COUPLING_RULE_CONFIG
from hyperstyle.src.python.review.quality.rules.cyclomatic_complexity_scoring import (
    CyclomaticComplexityRule,
    LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.error_prone_scoring import (
    ErrorProneRule, LANGUAGE_TO_ERROR_PRONE_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.function_length_scoring import (
    FunctionLengthRule,
    LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.inheritance_depth_scoring import (
    InheritanceDepthRule,
    LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG,
)
from hyperstyle.src.python.review.quality.rules.line_len_scoring import (
    LANGUAGE_TO_LINE_LENGTH_RULE_CONFIG, LineLengthRule,
)
from hyperstyle.src.python.review.quality.rules.maintainability_scoring import (
    LANGUAGE_TO_MAINTAINABILITY_RULE_CONFIG,
    MaintainabilityRule,
)
from hyperstyle.src.python.review.quality.rules.method_number_scoring import (
    LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG,
    MethodNumberRule,
)
from hyperstyle.src.python.review.quality.rules.weighted_methods_scoring import (
    LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG,
    WeightedMethodsRule,
)
from hyperstyle.src.python.review.reviewers.utils.code_statistics import CodeStatistics


def __get_available_rules(language: Language) -> List[Rule]:
    return [
        ErrorProneRule(LANGUAGE_TO_ERROR_PRONE_RULE_CONFIG[language]),
        BestPracticesRule(LANGUAGE_TO_BEST_PRACTICES_RULE_CONFIG[language]),
        ComplexityRule(LANGUAGE_TO_COMPLEXITY_RULE_CONFIG[language]),
        CyclomaticComplexityRule(LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG[language]),
        BooleanExpressionRule(LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG[language]),
        FunctionLengthRule(LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG[language]),
        InheritanceDepthRule(LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG[language]),
        MethodNumberRule(LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG[language]),
        CouplingRule(LANGUAGE_TO_COUPLING_RULE_CONFIG[language]),
        ResponseRule(LANGUAGE_TO_RESPONSE_RULE_CONFIG[language]),
        WeightedMethodsRule(LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG[language]),
        CohesionRule(LANGUAGE_TO_COHESION_RULE_CONFIG[language]),
        MaintainabilityRule(LANGUAGE_TO_MAINTAINABILITY_RULE_CONFIG[language]),
    ]


def evaluate_quality(statistics: CodeStatistics, language: Language) -> Quality:
    rule_statistics = statistics.issue_type_to_statistics_dict

    rules = __get_available_rules(language)
    for rule in rules:
        rule.apply(rule_statistics[rule.rule_type])

    # TODO: refactor
    code_style_rule = CodeStyleRule(LANGUAGE_TO_CODE_STYLE_RULE_CONFIG[language])
    code_style_rule.apply(rule_statistics[IssueType.CODE_STYLE],
                          statistics.n_code_style_issues, statistics.total_lines)
    rules.append(code_style_rule)

    line_len_rule = LineLengthRule(LANGUAGE_TO_LINE_LENGTH_RULE_CONFIG[language])
    line_len_rule.apply(rule_statistics[IssueType.LINE_LEN], statistics.total_lines)
    rules.append(line_len_rule)

    return Quality(rules)
