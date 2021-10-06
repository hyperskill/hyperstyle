import ast
from test.python.inspectors import PYTHON_AST_DATA_FOLDER, PYTHON_DATA_FOLDER
from test.python.inspectors.conftest import use_file_metadata

import pytest
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.pyast.python_ast import (
    BoolExpressionLensGatherer,
    FunctionLensGatherer,
    PythonAstInspector,
)

FILE_NAMES_AND_N_ISSUES = [
    ('case0_spaces.py', 0),
    ('case1_simple_valid_program.py', 0),
    ('case2_boolean_expressions.py', 3),
    ('case3_redefining_builtin.py', 0),
    ('case4_naming.py', 5),
    ('case5_returns.py', 1),
    ('case6_unused_variables.py', 1),
    ('case8_good_class.py', 1),
    ('case20_imports_order.py', 0),
    ('case10_unused_variable_in_loop.py', 1),
    ('case11_redundant_parentheses.py', 0),
    ('case12_unreachable_code.py', 1),
    ('case14_returns_errors.py', 4),
    ('case15_redefining.py', 1),
    ('case16_comments.py', 0),
    ('case17_dangerous_default_value.py', 1),
    ('case18_comprehensions.py', 0),
    ('case19_bad_indentation.py', 1),
    ('case21_imports.py', 0),
    ('case23_merging_comparisons.py', 4),
    ('case24_long_function.py', 1),
    ('case25_django.py', 1),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = PythonAstInspector()
    path_to_file = PYTHON_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    assert len(issues) == n_issues


def test_bool_expr_len_gatherer_one_expr():
    file_path = PYTHON_AST_DATA_FOLDER / 'one_bool_expression.py'
    code = file_path.read_text()

    tree = ast.parse(code, file_path)
    gatherer = BoolExpressionLensGatherer(file_path, InspectorType.PYTHON_AST)
    gatherer.visit(tree)

    assert len(gatherer.bool_expression_lens) == 1
    assert gatherer.bool_expression_lens[0].bool_expr_len == 5
    assert gatherer.bool_expression_lens[0].line_no == 2


def test_bool_expr_len_gatherer_many_exprs():
    file_path = PYTHON_AST_DATA_FOLDER / 'many_bool_expressions.py'
    code = file_path.read_text()

    tree = ast.parse(code, file_path)
    gatherer = BoolExpressionLensGatherer(file_path, InspectorType.PYTHON_AST)
    gatherer.visit(tree)

    assert len(gatherer.bool_expression_lens) == 3
    assert all(issue.bool_expr_len == 1 for issue in gatherer.bool_expression_lens)


def test_function_lens_gatherer():
    file_path = PYTHON_AST_DATA_FOLDER / 'function.py'
    code = file_path.read_text()

    tree = ast.parse(code, file_path)
    gatherer = FunctionLensGatherer(code, file_path, InspectorType.PYTHON_AST)
    gatherer.visit(tree)

    assert len(gatherer.function_lens) == 1
    assert gatherer.function_lens[0].func_len == 15
