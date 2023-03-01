__all__ = ['config']
class Config:
    SEMAPHORE = 10  # number of connections at the same time
    TRIES_NUMBER = 3
    SLEEP_BEFORE_RECONNECTION = 5  # seconds
    NAME_MAX_LENGTH = 40

config = Config()
