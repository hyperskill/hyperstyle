from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hyperstyle.src.python.review.common.language import Language
    from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType


@dataclass
class ApplicationConfig:
    disabled_inspectors: set[InspectorType]
    allow_duplicates: bool
    n_cpu: int
    inspectors_config: dict[str, object]
    with_all_categories: bool
    start_line: int = 1
    language: Language | None = None
    end_line: int | None = None
    new_format: bool = False
    history: str | None = None
    group_by_difficulty: bool = False
    ij_config: str | None = None

    @staticmethod
    def get_default_config() -> ApplicationConfig:
        return ApplicationConfig(
            disabled_inspectors=set(),
            allow_duplicates=False,
            n_cpu=1,
            inspectors_config={"n_cpu": 1},
            with_all_categories=True,
            start_line=1,
            language=None,
            new_format=False,
            group_by_difficulty=False,
        )
