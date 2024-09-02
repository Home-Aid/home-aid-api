import logging
from logging import INFO

class CustomFormatter(logging.Formatter):
    """The `CustomFormatter` class is a subclass of `logging.Formatter`
    that provides custom formatting for log messages with different log levels."""

    CYAN = "\x1b[0;36m"
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    format = "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s"

    FORMATS = {
        logging.DEBUG: CYAN + format + RESET,
        logging.INFO: GREY + format + RESET,
        logging.WARNING: YELLOW + format + RESET,
        logging.ERROR: RED + format + RESET,
        logging.CRITICAL: BOLD_RED + format + RESET,
    }

    def __init__(self):
        """Initialize the CustomFormatter with the desired date format."""
        super().__init__(datefmt="%Y-%m-%d %H:%M:%S IST")

    def format(self, record):
        """The function formats a log record using a specified log format.

        Parameters
        ----------
        record
            The `record` parameter is an instance of the `LogRecord` class. It contains information about
            the log message being formatted, such as the log level, log message, timestamp, and other
            attributes.

        Returns
        -------
            The code is returning the formatted log message for the given record.

        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S IST")
        return formatter.format(record)

class Logger(object):
    """The Logger class is a Python class that sets up logging configuration with a
    console logger and a custom formatter."""

    def __init__(self):
        """The above function initializes a logger with a custom formatter
        and adds a console logger to it."""
        # Logger configuration.
        console_logger = logging.StreamHandler()
        console_logger.setFormatter(CustomFormatter())

        # Complete logging config.
        self.logger = logging.getLogger()
        self.logger.setLevel(INFO)
        self.logger.addHandler(console_logger)

logger = Logger().logger
