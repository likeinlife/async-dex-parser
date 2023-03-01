__all__ = ['config']
import logging


class Config:
    SEMAPHORE = 6  # number of connections at the same time
    TRIES_NUMBER = 3
    SLEEP_BEFORE_RECONNECTION = 5  # seconds
    NAME_MAX_LENGTH = 40
    LOGGING_LEVEL = logging.DEBUG


config = Config()
