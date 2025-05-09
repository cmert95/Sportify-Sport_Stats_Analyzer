import logging
import os

from utils.paths import LOG_DIR


def setup_logger(name=__name__, log_name="app", level=logging.INFO):
    """
    Sets up and returns a logger instance with file and console handlers.
    If log_name is provided, log will be written to logs/{log_name}.log
    """
    log_file = os.path.join(LOG_DIR, f"{log_name}.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(name)s — %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
