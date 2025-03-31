import logging

"""
LOGGER UTILS
"""

ERR_LOG_FILE = "error.log"

def setup_logger(name="app_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Error Log Handler
    file_handler = logging.FileHandler(ERR_LOG_FILE)
    file_handler.setLevel(logging.ERROR)

    # Format Log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add Handler into Logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

