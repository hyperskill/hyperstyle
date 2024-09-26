from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging.config import _DictConfigArgs

logging_config: _DictConfigArgs = {
    "version": 1,
    "formatters": {
        "common": {
            "class": "logging.Formatter",
            "format": "%(asctime)s | %(levelname)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "common",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
    "disable_existing_loggers": False,
}
