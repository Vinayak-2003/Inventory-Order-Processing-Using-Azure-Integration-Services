import logging

def create_logger():
    logger = logging.getLogger("order_logger")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs/logs.log')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('{%(asctime)s - %(module)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s}')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    return logger