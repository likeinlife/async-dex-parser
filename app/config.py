__all__ = ['config']
import logging


class Config:
    SEMAPHORE = 6  # number of connections at the same time
    TRIES_NUMBER = 3
    SLEEP_BEFORE_RECONNECTION = 5  # seconds
    NAME_MAX_LENGTH = 40  # max length of title name
    LOGGING_LEVEL = logging.INFO
    LOGS_MAX_SIZE = 256  # in bytes
    ENABLE_STREAM_HANDLER = False  # print logs to console


config = Config()
