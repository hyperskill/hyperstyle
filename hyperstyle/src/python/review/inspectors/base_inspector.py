import abc
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue


class BaseInspector(abc.ABC):
    """
    Each external inspector contains a dictionary in which the IssueType corresponds to the original linter classes.
    The dictionary helps to categorize errors during parsing the linters' output.

    To add a new inspector, you need:
     - to create a class that inherits from the BaseInspector class,
     - define the type of inspector (the type filed) by adding a new option in the InspectorType,
     - implement the <inspect >function.

    Typically, the <inspect> function launches a linter and parses its output (XML or JSON) to get a list of BaseIssue.

    Some inspectors (internal) do not require creating a dictionary with IssueType.
    This is connected to the fact that they do not launch an additional analysis tool and work with the code directly,
    for example, the python AST inspector.
    """

    # Type of inspection for analyzing, e.g. pylint, detekt and etc
    @property
    @abc.abstractmethod
    def inspector_type(self) -> InspectorType:
        raise NotImplementedError('inspector_type property not implemented yet')

    @abc.abstractmethod
    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        raise NotImplementedError('inspect method not implemented yet')
