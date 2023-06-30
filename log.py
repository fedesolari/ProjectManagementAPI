import logging
import sys

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)

handlers = [stdout_handler]

logging.basicConfig(level=logging.DEBUG, handlers=handlers)


def get_logger():
    return logging.getLogger()


LOG = get_logger()
