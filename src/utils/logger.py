import logging


def setup_logger(name="default", log_name=None, level=logging.INFO):
    """
    Sets up and returns a logger instance with file and console handlers.
    If log_name is provided, log will be written to logs/{log_name}.log
    """
    if log_name is None:
        log_file = "logs/app.log"
    else:
        log_file = f"logs/{log_name}.log"

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
