import functools
import itertools
import logging
import multiprocessing
from pathlib import Path
from typing import Any, Callable, Dict, List

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.issue import BaseIssue

logger = logging.getLogger(__name__)


def run_inspector(path: Path,
                  config: ApplicationConfig,
                  inspector: BaseInspector) -> List[BaseIssue]:
    return _run_inspector(inspector.inspect, path, config, inspector)


def run_inspector_in_memory(code: str,
                            config: ApplicationConfig,
                            inspector: BaseInspector) -> List[BaseIssue]:
    return _run_inspector(inspector.inspect_in_memory, code, config, inspector)


def _run_inspector(inspect_function: Callable[[Any, Dict[str, Any]], List[BaseIssue]],
                   data: Any,
                   config: ApplicationConfig,
                   inspector: BaseInspector) -> List[BaseIssue]:
    try:
        return inspect_function(data, config.inspectors_config)
    except Exception as e:
        logger.error(f'Inspector {inspector.inspector_type} failed.', e)
        return []


def inspect_in_parallel(inspector_runner: Callable[[Any, ApplicationConfig, BaseInspector], List[BaseIssue]],
                        data: Any,
                        config: ApplicationConfig,
                        inspectors: List[BaseInspector]) -> List[BaseIssue]:
    inspectors = filter(lambda i: i.inspector_type not in config.disabled_inspectors, inspectors)

    if config.n_cpu == 1:
        issues = []
        for inspector in inspectors:
            inspector_issues = inspector_runner(data, config, inspector)
            issues.extend(inspector_issues)
        return issues

    with multiprocessing.Pool(config.n_cpu) as pool:
        issues = pool.map(
            functools.partial(inspector_runner, data, config),
            inspectors,
        )

    return list(itertools.chain(*issues))
