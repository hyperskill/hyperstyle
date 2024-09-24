from __future__ import annotations

import sys

logging_config: dict[str, object] = {
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
