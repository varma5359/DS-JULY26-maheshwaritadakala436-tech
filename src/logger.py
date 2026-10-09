
"""
Configure logging for the Motor Insurance Analytics project.

Logs pipeline activities, warnings, and errors to a log file
and displays important messages in the console.
"""

import logging
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"


def setup_logger():
    """
    Configure and return the project logger.

    Creates the logs directory if it does not exist.
    Logs are written to a file and displayed in the console.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("motor_insurance")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Avoid duplicate handlers if setup_logger() is called repeatedly.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_pipeline_step(message):
    """
    Record a successful or informational pipeline step.

    Args:
        message: Description of the pipeline activity.
    """
    logger = setup_logger()
    logger.info(message)


def log_error(message):
    """
    Record an error encountered during pipeline execution.

    Args:
        message: Description of the error.
    """
    logger = setup_logger()
    logger.error(message)


def log_warning(message):
    """
    Record a warning that needs attention but may not stop the pipeline.

    Args:
        message: Description of the warning.
    """
    logger = setup_logger()
    logger.warning(message)


def log_exception(message):
    """
    Record an error message and the active exception traceback.

    Call this function inside an except block.
    """
    logger = setup_logger()
    logger.exception(message)

