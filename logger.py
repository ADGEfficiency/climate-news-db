import logging

from pathlib import Path


def make_logger(log_file, level='debug'):
    """info to STDOUT, debug to file"""
    log_file = Path.home() / 'climate-nlp' / log_file

    if level == 'debug':
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Create a custom logger
    logger = logging.getLogger('logger')
    logger.setLevel(level)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_file)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
