__all__ = ['config']
from functools import cached_property
import logging
import os
from pathlib import Path

from httpx import Timeout


class Config:
    SLEEP_BEFORE_RECONNECTION = 5  # seconds
    NAME_MAX_LENGTH = 40  # max length of title name
    LOGS_MAX_SIZE = 256  # in bytes
    ENABLE_STREAM_HANDLER = False  # print logs to console

    @property
    def THREADS(self) -> int:
        """Change threads count"""
        if (var := os.getenv('THREADS')):
            if self.LOGGING_LEVEL == 'DEBUG':
                print(f'THREADS count = {int(var)}')
            return int(var)
        return 5

    @property
    def TIMEOUT(self) -> Timeout:
        """Time to make connect with mangadex server. Set higher if your internet is slow"""
        if (var := os.getenv('TIMEOUT')):
            return Timeout(int(var))
        return Timeout(30)

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
