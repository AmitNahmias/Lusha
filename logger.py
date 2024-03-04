import logging
import colorlog

LOG_PATH = 'log.log'
LOG_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] -> %(message)s'


def setup_logger(logger_id: str) -> logging.Logger:
    """
    Setup logger.

    :param logger_id: Logger id/name.
    :return: Logger instance.
    """
    logger = logging.getLogger(name=logger_id)
    logger.setLevel(logging.DEBUG)

    # Create a ColoredFormatter
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s] -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors=
        {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    if not getattr(logger, 'handler_set', None):
        stream_handler = _create_stream_handler(formatter=formatter)
        # file_handler = _create_file_handler(formatter=formatter)
        # logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.handler_set = True
    return logger


def _create_stream_handler(formatter: logging.Formatter) -> logging.StreamHandler:
    """
    Create stream handler for logger.

    :param formatter: Data format.
    :return: Stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler


def _create_file_handler(formatter: logging.Formatter) -> logging.FileHandler:
    """
    Create file handler for logger.

    :param formatter: Data format.
    :return: File handler.
    """
    file_handler = logging.FileHandler(filename=LOG_PATH)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler
