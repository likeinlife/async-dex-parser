__all__ = ['config']
class Config:
    SEMAPHORE = 50  # number of connections at the same time
    TRIES_NUMBER = 3
    SLEEP_BEFORE_RECONNECTION = 5  # seconds

config = Config()
