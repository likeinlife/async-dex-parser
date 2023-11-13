import os
from functools import cached_property
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
	NAME_MAX_LENGTH: int = Field(40)  # the maximum length of the title
	LOGS_MAX_SIZE: int = Field(256)  # in bytes
	ENABLE_STREAM_HANDLER: int = Field(False)  # print logs to console

	THREADS: int = Field(5)
	TIMEOUT: int = Field(5)
	LOGGING_LEVEL: str = Field('WARNING')

	@cached_property
	def BASEPATH(self) -> Path:
		BASEPATH = Path(os.path.expanduser(r'~\Documents\dex'))
		BASEPATH.mkdir(exist_ok=True, parents=True)
		return BASEPATH


config = Config()
