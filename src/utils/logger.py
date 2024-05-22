import datetime
import logging
import logging.config as LoggingConfig
import os
from datetime import datetime, timedelta, timezone
from typing import List

from google.cloud import logging as google_cloud_logging
from google.oauth2 import service_account

from src.utils.utils import go_up_n_dirs

# Load logging configuration
root_path = go_up_n_dirs(os.path.abspath(__file__), 3)
LoggingConfig.fileConfig(os.path.join(root_path, 'logging.conf'))


def get_logger(log_level):
    loggers = {
        "DEBUG": "integrationTestsLogger",
        "INFO": "root",
        "ERROR": "pipelineTestsLogger"
    }

    log_level_upper = log_level.upper()

    if log_level_upper in loggers:
        return logging.getLogger(loggers[log_level_upper])
    else:
        raise AttributeError(f"LOG_LEVEL {log_level_upper} is invalid. Valid values are: DEBUG, INFO, ERROR")


logger = get_logger(os.getenv("LOG_LEVEL"))


def log_request(func):
    def wrapper(*args, **kwargs):
        logger.debug(
            f"Calling {func.__name__} with url: {args[0].host}, headers: {args[0].headers} and payload:"
            f"{args[0].payload if hasattr(args[0], 'payload') else None}")
        response = func(*args, **kwargs)
        logger.debug(f"{func.__name__} status_code: {response.status_code} - body: {response.body}")
        return response

    return wrapper
