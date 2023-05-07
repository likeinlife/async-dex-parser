__all__ = ['config']
from functools import cached_property
import logging
import os
from pathlib import Path


class Config:
    SEMAPHORE = 5  # number of connections at the same time
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

    @cached_property
    def BASEPATH(self):
        BASEPATH = Path(os.path.expanduser(r'~\Documents\dex'))
        if not BASEPATH.exists():
            BASEPATH.mkdir()

        return BASEPATH


config = Config()
