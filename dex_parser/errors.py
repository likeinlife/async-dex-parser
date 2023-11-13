from dex_parser import logger_setup

logger = logger_setup.get_logger(__name__)


class DexParserError(Exception):
	"""Base error"""

	def __init__(self, msg, *args: object) -> None:
		logger.error('%s - %s' % (self.__class__.__name__, msg))
		super().__init__(msg, *args)


class ParseChapterInfoError(DexParserError):
	"""Invalid chapter info response"""


class ParseChapterPagesError(DexParserError):
	"""Invalid chapter pages response"""


class ParseTitleInfoError(DexParserError):
	"""Invalid title info response"""


class ParseTitleGetChaptersError(DexParserError):
	"""Invalid title chapters response"""


class ParseTitleGetByNameError(DexParserError):
	"""Invalid title found by name response"""
