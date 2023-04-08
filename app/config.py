__all__ = ['config']
import logging
import os


class Config:
    SEMAPHORE = 5  # number of connections at the same time
    TRIES_NUMBER = 3
    SLEEP_BEFORE_RECONNECTION = 5  # seconds
    NAME_MAX_LENGTH = 40  # max length of title name
    LOGS_MAX_SIZE = 256  # in bytes
    ENABLE_STREAM_HANDLER = False  # print logs to console

    @property
    def LOGGING_LEVEL(self):
        if (var := os.getenv('LOGGING_LEVEL')):
            return var
        else:
            return logging.INFO


config = Config()
