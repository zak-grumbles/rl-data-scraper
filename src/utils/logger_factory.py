import logging
import sys

def make_logger(name, level=None):
    log_format = '%(asctime)s %(name)s:%(levelname)s - %(message)s'

    logger = logging.getLogger(name)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(log_format))

    if level is not None:
        logger.setLevel(level)
        console.setLevel(level)

    logger.addHandler(console)

    return logger