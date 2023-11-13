import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dex_parser.config import config

BASEPATH = config.BASEPATH / Path('logs')
if not BASEPATH.exists():
	BASEPATH.mkdir()


class StreamFormatter(logging.Formatter):
	grey = '\x1b[38;20m'
	yellow = '\x1b[33;20m'
	blue = '\x1b[96m'
	red = '\x1b[31;20m'
	bold_red = '\x1b[31;1m'
	reset = '\x1b[0m'
	this_format = r'%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'

	FORMATS = {
		logging.DEBUG: grey + this_format + reset,
		logging.INFO: blue + this_format + reset,
		logging.WARNING: yellow + this_format + reset,
		logging.ERROR: red + this_format + reset,
		logging.CRITICAL: bold_red + this_format + reset,
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


class FileFormatter(logging.Formatter):
	this_format = r'%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'

	def format(self, record):
		log_fmt = self.this_format
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


def get_logger(name: str) -> logging.Logger:
	level = config.LOGGING_LEVEL

	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	if config.ENABLE_STREAM_HANDLER:
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(level)
		stream_handler.setFormatter(StreamFormatter())
		logger.addHandler(stream_handler)

	file_handler = RotatingFileHandler(BASEPATH / 'dex.log', maxBytes=config.LOGS_MAX_SIZE)
	file_handler.setLevel(level)
	file_handler.setFormatter(FileFormatter())
	logger.addHandler(file_handler)
	logger.propagate = False

	return logger
