import ast
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common import language
from hyperstyle.src.python.review.common.file_system import get_all_file_system_items
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue, BoolExprLenIssue, FuncLenIssue, IssueDifficulty, IssueType,
)
from hyperstyle.src.python.review.inspectors.tips import get_bool_expr_len_tip, get_func_len_tip

BOOL_EXPR_LEN_ORIGIN_CLASS = 'C001'
FUNC_LEN_ORIGIN_CLASS = 'C002'


class BoolExpressionLensGatherer(ast.NodeVisitor):

    def __init__(self, file_path: Path, inspector_type: InspectorType):
        self._inspector_type = inspector_type
        self._file_path = file_path
        self.bool_expression_lens: List[BoolExprLenIssue] = []

    def visit(self, node: ast.AST):
        if not isinstance(node, ast.BoolOp):
            super().visit(node)
            return

        length = 0
        for inner_node in ast.walk(node):
            if isinstance(inner_node, ast.BoolOp):
                length += len(inner_node.values) - 1

        issue_type = PythonAstInspector.choose_issue_type(BOOL_EXPR_LEN_ORIGIN_CLASS)

        self.bool_expression_lens.append(BoolExprLenIssue(
            file_path=self._file_path,
            line_no=node.lineno,
            column_no=node.col_offset,
            description=get_bool_expr_len_tip(),
            origin_class=BOOL_EXPR_LEN_ORIGIN_CLASS,
            inspector_type=self._inspector_type,
            bool_expr_len=length,
            type=issue_type,
            difficulty=IssueDifficulty.get_by_issue_type(issue_type),
        ))


class FunctionLensGatherer(ast.NodeVisitor):

    def __init__(self, content: str, file_path: Path, inspector_type: InspectorType):
        self._inspector_type = inspector_type
        self._file_path = file_path
        self._content = content
        self._line_no_to_sym_no_map = create_line_no_to_sym_no_map(content)
        self._n_lines = Counter(content)['\n'] + 1
        self._previous_node = None
        self._function_lens: List[FuncLenIssue] = []

    def visit(self, node):
        if isinstance(self._previous_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_length = self._find_func_len(
                self._previous_node.lineno, node.lineno,
            )

            issue_type = PythonAstInspector.choose_issue_type(FUNC_LEN_ORIGIN_CLASS)

            self._function_lens.append(FuncLenIssue(
                file_path=self._file_path,
                line_no=self._previous_node.lineno,
                column_no=self._previous_node.col_offset,
                description=get_func_len_tip(),
                origin_class=FUNC_LEN_ORIGIN_CLASS,
                inspector_type=self._inspector_type,
                func_len=func_length,
                type=issue_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            ))

        self._previous_node = node
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            super().visit(node)

    @property
    def function_lens(self) -> List[FuncLenIssue]:
        if isinstance(self._previous_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_length = self._find_func_len(
                self._previous_node.lineno, self._n_lines + 1,
            )

            issue_type = PythonAstInspector.choose_issue_type(FUNC_LEN_ORIGIN_CLASS)

            self._function_lens.append(FuncLenIssue(
                file_path=self._file_path,
                line_no=self._previous_node.lineno,
                column_no=self._previous_node.col_offset,
                description=get_func_len_tip(),
                origin_class=FUNC_LEN_ORIGIN_CLASS,
                inspector_type=self._inspector_type,
                func_len=func_length,
                type=issue_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            ))

        self._previous_node = None
        return self._function_lens

    def _find_func_len(self, start_line_no: int, end_line_no: int):
        func_body = self._content[self._line_no_to_sym_no_map[start_line_no]:
                                  self._line_no_to_sym_no_map[end_line_no]]
        func_body = func_body.strip()

        return Counter(func_body)['\n']


class PythonAstInspector(BaseInspector):
    inspector_type = InspectorType.PYTHON_AST

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        if path.is_file():
            path_to_files = [path]
        else:
            path_to_files = get_all_file_system_items(path)

        path_to_files = language.filter_paths_by_language(path_to_files, Language.PYTHON)

        metrics = []
        for path_to_file in path_to_files:
            file_content = path_to_file.read_text()
            tree = ast.parse(file_content, path_to_file.name)

            bool_gatherer = BoolExpressionLensGatherer(path_to_file, cls.inspector_type)
            bool_gatherer.visit(tree)
            metrics.extend(
                bool_gatherer.bool_expression_lens,
            )

            func_gatherer = FunctionLensGatherer(file_content, path_to_file, cls.inspector_type)
            func_gatherer.visit(tree)
            metrics.extend(
                func_gatherer.function_lens,
            )

        return metrics

    @staticmethod
    def choose_issue_type(code: str) -> IssueType:
        if code == BOOL_EXPR_LEN_ORIGIN_CLASS:
            return IssueType.BOOL_EXPR_LEN

        if code == FUNC_LEN_ORIGIN_CLASS:
            return IssueType.FUNC_LEN

        return IssueType.BEST_PRACTICES


def create_line_no_to_sym_no_map(content) -> Dict[int, int]:
    mapping = defaultdict(lambda: len(content), {1: 0})
    line_no = 2
    for sym_no, sym in enumerate(content):
        if sym == '\n':
            mapping[line_no] = sym_no + 1
            line_no += 1

    return mapping
