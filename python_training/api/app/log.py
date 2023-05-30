import logging
import logging.config
import os
from typing import Any

import structlog
from asgi_correlation_id import correlation_id
from structlog.types import EventDict


def _add_correlation(logger: structlog.BoundLogger, name: str, event_dict: EventDict) -> EventDict:
    event_dict["_request_id"] = correlation_id.get()
    return event_dict


def _add_pid(logger: structlog.BoundLogger, name: str, event_dict: EventDict) -> EventDict:
    event_dict["pid"] = os.getpid()
    return event_dict


def _add_module_and_lineno(logger: structlog.BoundLogger, name: str, event_dict: EventDict) -> EventDict:
    # https://github.com/jrobichaud/django-structlog/issues/29#issuecomment-600991068
    frame, module_str = structlog._frames._find_first_app_frame_and_name(additional_ignores=[__name__])
    event_dict["module"] = module_str
    event_dict["lineno"] = frame.f_lineno
    return event_dict


def get_logger(log_level: str) -> Any:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(colors=False),
                    ],
                    "foreign_pre_chain": [],
                },
            },
            "handlers": {
                "default": {
                    "level": log_level,
                    "class": "logging.StreamHandler",
                    "formatter": "plain",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": log_level,
                    "propagate": True,
                },
                "uvicorn": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.threadlocal.merge_threadlocal,
            structlog.stdlib.add_log_level,
            _add_module_and_lineno,
            _add_pid,
            _add_correlation,
            structlog.processors.TimeStamper(fmt="iso", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(ensure_ascii=False, sort_keys=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()
