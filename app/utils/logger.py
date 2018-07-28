import logging
import settings

def init_logging():
    log = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(threadName)s(%(thread)d):%(module)s:%(filename)s:%(funcName)s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    level = logging.INFO
    if settings.core.LOGGING_LEVEL == 'DEBUG':
        level = logging.DEBUG
    elif settings.core.LOGGING_LEVEL == 'INFO':
        level = logging.INFO
    elif settings.core.LOGGING_LEVEL == 'WARNING':
        level = logging.WARNING
    elif settings.core.LOGGING_LEVEL == 'ERROR':
        level = logging.ERROR
    log.setLevel(level)
