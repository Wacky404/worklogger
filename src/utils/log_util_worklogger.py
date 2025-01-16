#!/opt/homebrew/bin/python3
"""
LOGGER SETUP FILE FOR WORKLOGGER
author: Wacky404 <wacky404@dev.com>
"""

import logging.config
import atexit


logger = logging.getLogger("WorkLogger")


def setup_logging(log_lvl_stdout='WARNING') -> None:
    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)s: %(message)s",
            },
            "detailed": {
                "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": log_lvl_stdout,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "logs/WorkLogger.log",
                "maxBytes": 5000000,  # 5 mb
                "backupCount": 5,
            },
            "queue_handler": {
                "class": "logging.handlers.QueueHandler",
                "handlers": [
                    "stdout",
                    "file"
                ],
                "respect_handler_level": True
            }
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": [
                    "queue_handler"
                ],
            },
        },
    }
    logging.config.dictConfig(logging_config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
