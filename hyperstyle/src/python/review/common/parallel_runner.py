import functools
import itertools
import logging
import multiprocessing
from pathlib import Path
from typing import List

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.issue import BaseIssue

logger = logging.getLogger(__name__)


def run_inspector(path: Path,
                  config: ApplicationConfig,
                  inspector: BaseInspector) -> List[BaseIssue]:
    try:
        return inspector.inspect(path, config.inspectors_config)
    except Exception as e:
        logger.error(f'Inspector {inspector.inspector_type} failed.', e)
        return []


def inspect_in_parallel(path: Path,
                        config: ApplicationConfig,
                        inspectors: List[BaseInspector]) -> List[BaseIssue]:
    inspectors = filter(lambda i: i.inspector_type not in config.disabled_inspectors, inspectors)

    if config.n_cpu == 1:
        issues = []
        for inspector in inspectors:
            inspector_issues = run_inspector(path, config, inspector)
            issues.extend(inspector_issues)
        return issues

    with multiprocessing.Pool(config.n_cpu) as pool:
        issues = pool.map(
            functools.partial(run_inspector, path, config),
            inspectors,
        )

    return list(itertools.chain(*issues))
