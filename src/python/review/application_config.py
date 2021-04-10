from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional, Set

from src.python.review.inspectors.inspector_type import InspectorType


@dataclass
class ApplicationConfig:
    disabled_inspectors: Set[InspectorType]
    allow_duplicates: bool
    n_cpu: int
    inspectors_config: dict
    start_line: int = 1
    end_line: Optional[int] = None
    new_format: bool = False


@unique
class LanguageVersion(Enum):
    JAVA_7 = 'java7'
    JAVA_8 = 'java8'
    JAVA_9 = 'java9'
    JAVA_11 = 'java11'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls.__members__.values()]
