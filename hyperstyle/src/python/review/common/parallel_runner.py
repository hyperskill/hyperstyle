from __future__ import annotations

import functools
import itertools
import logging
import multiprocessing
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from hyperstyle.src.python.review.application_config import ApplicationConfig
    from hyperstyle.src.python.review.inspectors.common.issue.issue import BaseIssue

from hyperstyle.src.python.review.inspectors.common.inspector.base_inspector import BaseInspector, BaseIJInspector

logger = logging.getLogger(__name__)


def run_inspector(path: Path, config: ApplicationConfig, inspector: BaseInspector) -> list[BaseIssue]:
    return _run_inspector(inspector.inspect, path, config, inspector)


def run_inspector_in_memory(
    code: str, config: ApplicationConfig, inspector: BaseInspector
) -> list[BaseIssue]:
    return _run_inspector(inspector.inspect_in_memory, code, config, inspector)


def _run_inspector(
    inspect_function: Callable[[Any, dict[str, Any]], list[BaseIssue]],
    data: Any,
    config: ApplicationConfig,
    inspector: BaseInspector,
) -> list[BaseIssue]:
    try:
        return inspect_function(data, config.inspectors_config)
    except Exception:
        if isinstance(inspector, BaseIJInspector):
            logger.exception(f"Inspector {inspector.inspector_type} failed. Returning empty result.")
            return []
        logger.exception(f"Inspector {inspector.inspector_type} failed.")
        raise


def inspect_in_parallel(
    inspector_runner: Callable[[Any, ApplicationConfig, BaseInspector], list[BaseIssue]],
    data: Any,
    config: ApplicationConfig,
    inspectors: list[BaseInspector],
) -> list[BaseIssue]:
    inspectors_to_run = filter(lambda i: i.inspector_type not in config.disabled_inspectors, inspectors)

    if config.n_cpu == 1:
        issues = []
        for inspector in inspectors_to_run:
            inspector_issues = inspector_runner(data, config, inspector)
            issues.extend(inspector_issues)
        return issues

    with multiprocessing.Pool(config.n_cpu) as pool:
        issues = pool.map(
            functools.partial(inspector_runner, data, config),
            inspectors_to_run,
        )

    return list(itertools.chain(*issues))
