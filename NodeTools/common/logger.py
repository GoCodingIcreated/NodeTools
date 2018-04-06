import logging


LOG_LEVEL = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def configure_logger(verbose_arg, log_path):
    log_level = LOG_LEVEL.get(verbose_arg, logging.NOTSET)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    rootLogger.addHandler(consoleHandler)

    if log_path:
        fileHandler = logging.FileHandler(log_path)
        fileHandler.setFormatter(formatter)
        rootLogger.addHandler(fileHandler)
