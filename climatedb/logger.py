import logging

from pathlib import Path


def make_logger(log_file=None):
    """info to STDOUT, debug to file"""

    level = logging.INFO

    # Create a custom logger
    logger = logging.getLogger("climatedb")
    logger.setLevel(level)

    # Create handlers
    c_handler = logging.StreamHandler()
    if log_file:
        log_file = Path.home() / "climate-nlp" / log_file
        f_handler = logging.FileHandler(log_file)
        f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        f_handler.setFormatter(f_format)
        f_handler.setLevel(logging.INFO)
        logger.addHandler(f_handler)

    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    return logger
