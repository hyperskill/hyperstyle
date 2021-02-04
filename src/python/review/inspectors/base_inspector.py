import abc
from pathlib import Path
from typing import List

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue


class BaseInspector(abc.ABC):

    @property
    @abc.abstractmethod
    def inspector_type(self) -> InspectorType:
        raise NotImplementedError

    @abc.abstractmethod
    def inspect(self, path: Path, config: dict) -> List[BaseIssue]:
        raise NotImplementedError
