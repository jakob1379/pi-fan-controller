"""
Template for Beautiful Logging in Python
Based on tips from the YouTube video: https://www.youtube.com/watch?v=9L77QExPmI0

This script configures a logging setup to produce clear, informative log messages.
It includes console and file handlers, and is set up to capture different log levels in an elegant manner.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
import os

LOG_FILE = os.environ.get("LOG_FILE", "application.log")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.DEBUG)


def setup_logging():
    """
    Configures logging for console and file outputs with different handlers and formats.
    """
    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    
    # Rich Handler for console with timestamp
    console_handler = RichHandler(rich_tracebacks=True, show_path=False)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(fmt="[%(asctime)s] %(message)s", datefmt="%m/%d/%y %H:%M:%S"))
    logger.addHandler(console_handler)
    
    # File handler configuration (with rotation)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
    )
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


if __name__ == "__main__":
    setup_logging()
    
    # Example usage of logging in different scenarios
    logging.debug("This is a debug message for detailed debugging information.")
    logging.info("Application is running smoothly.")
    logging.warning("This is a warning for potential issues.")
    logging.error("An error occurred during execution.")
    logging.critical("Critical issue that needs immediate attention.")
