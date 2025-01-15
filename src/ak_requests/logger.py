"""Module for custom logging functionality with file and stream handlers.

This module provides a custom logging class that creates both console and file-based
logs with consistent formatting and user-specific log files.
"""

import getpass
import logging
import time
from pathlib import Path


class Log(object):
    """A custom logging class that provides both file and console logging capabilities.

    This class wraps Python's built-in logging functionality to provide a simplified
    interface for logging messages. It automatically creates log files in a 'logs'
    directory using the current user's username and month as part of the filename.

    Attributes:
        logger (logging.Logger): The underlying logger instance configured with
            both stream and file handlers.

    Example:
        >>> log = Log()
        >>> log.info("Starting application")
        >>> log.error("An error occurred")
    """

    def __init__(self):
        """Initialize the logger with both stream and file handlers.

        Sets up a logger instance with the current user's username, configures
        formatting for log messages, and creates handlers for both console output
        and file logging. The log files are stored in a 'logs' directory with
        filenames incorporating the username and current month.
        """
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        format = "%(asctime)s-%(levelname)s: %(message)s"
        formatter = logging.Formatter(format, datefmt="%Y%m%d-%H%M%S")

        # Set up console handler
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)

        # Set up file handler
        Path("logs").mkdir(exist_ok=True)
        logfile = Path("logs") / f'{user}{time.strftime("-%Y-%b")}.log'
        filehandler = logging.FileHandler(logfile, encoding="utf-8")
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)

    def debug(self, msg: str) -> None:
        """Log a debug message.

        Args:
            msg: The message to log at DEBUG level.
        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log an info message.

        Args:
            msg: The message to log at INFO level.
        """
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log a warning message.

        Args:
            msg: The message to log at WARNING level.
        """
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log an error message.

        Args:
            msg: The message to log at ERROR level.
        """
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """Log a critical message.

        Args:
            msg: The message to log at CRITICAL level.
        """
        self.logger.critical(msg)

    def log(self, level, msg: str) -> None:
        """Log a message at a specified level.

        Args:
            level: The logging level to use (e.g., logging.INFO, logging.ERROR)
            msg: The message to log at the specified level.
        """
        self.logger.log(level, msg)

    def setLevel(self, level) -> None:
        """Set the minimum logging level for the logger.

        Args:
            level: The minimum logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self.logger.setLevel(level)

    def disable(self) -> None:
        """Disable all logging.

        Disables all logging by setting the logging level to 50 (CRITICAL + 10),
        effectively preventing any messages from being logged.
        """
        logging.disable(50)
