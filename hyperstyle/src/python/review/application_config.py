from dataclasses import dataclass
from typing import Optional, Set

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType


@dataclass
class ApplicationConfig:
    disabled_inspectors: Set[InspectorType]
    allow_duplicates: bool
    n_cpu: int
    inspectors_config: dict
    with_all_categories: bool
    start_line: int = 1
    language: Optional[Language] = None
    end_line: Optional[int] = None
    new_format: bool = False
    history: Optional[str] = None
    group_by_difficulty: bool = False
    ij_config: Optional[str] = None

    @staticmethod
    def get_default_config() -> 'ApplicationConfig':
        return ApplicationConfig(
            disabled_inspectors=set(),
            allow_duplicates=False,
            n_cpu=1,
            inspectors_config={'n_cpu': 1},
            with_all_categories=True,
            start_line=1,
            language=None,
            new_format=False,
            group_by_difficulty=False,
        )
