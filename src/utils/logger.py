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


class GoogleCloudLoggingClient:
    _google_cloud_logging_client = None

    def __init__(self, credentials: service_account.Credentials = None):
        if credentials:
            self._google_cloud_logging_client = google_cloud_logging.Client(credentials=credentials)
        else:
            # Initialize with default credentials in case none are provided
            self._google_cloud_logging_client = google_cloud_logging.Client()
        self._resource_names = [f'projects/{self._google_cloud_logging_client.project}']

    @staticmethod
    def get_credentials():
        """
        Retrieves Google Cloud credentials from a JSON file.
        """
        credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not os.path.exists(credentials_file):
            raise FileNotFoundError(f"Google Cloud credentials file not found: {credentials_file}")

        credentials = service_account.Credentials.from_service_account_file(str(credentials_file))
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/logging.read'])
        return scoped_credentials

    def filter_logs(self, **kwargs) -> (List[str], None):
        """
        Filter Logs

        Filters logs based on specified parameters.

        Parameters:
        - container_name (str): The name of the container to filter logs for.
        - start_time (str): The start time of the log entries to retrieve. If not provided, the default start time is set to 1 minute before the current time.
        - end_time (str): The end time of the log entries to retrieve. If not provided, the default end time is set to the current time.
        - filter_string (str): The initial filter string to use for filtering log entries.

        Returns:
        - list: A list of log entries that match the specified parameters. Returns None if no log entries were found.

        Raises:
        - AssertionError: If no log entries were found.

        """
        logs_list = []
        container_name = kwargs.get("container_name")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        try:
            # Construct initial filter string
            filter_str = kwargs.get("filter_string")

            # Handle default or specified time range
            if not start_time or not end_time:
                now = datetime.now(timezone.utc)
                start_time = (now - timedelta(minutes=1)).isoformat()
                end_time = now.isoformat()
            else:
                # Ensure start_time and end_time are properly converted to UTC datetime objects
                start_time = datetime.fromisoformat(start_time.rstrip("Z")).replace(tzinfo=timezone.utc).isoformat()
                end_time = datetime.fromisoformat(end_time.rstrip("Z")).replace(tzinfo=timezone.utc).isoformat()

            filter_str += f'AND timestamp>="{start_time}" AND timestamp<="{end_time}" '

            if container_name:
                filter_str += f'AND resource.labels.container_name="{container_name}"'

            entries = self._google_cloud_logging_client.list_entries(filter_=filter_str,
                                                                     resource_names=self._resource_names)
            for entry in entries:
                logs_list.append(entry.payload)
            if logs_list:
                logger.info("Entries found. Proceeding with log validation")
                return logs_list
        except Exception as e:
            log.error(f"An error occurred while filtering logs: \n{e}")
            raise e
        finally:
            if not logs_list:
                raise AssertionError("")
