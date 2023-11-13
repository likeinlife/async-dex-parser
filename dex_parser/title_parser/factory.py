import re

from dex_parser import common

from .title_name_parser import TitleNameParser
from .title_parser import TitleParser


def get_title_parser(identificator: str, language: str):
	if title_id := common.get_id_from_url(identificator, 'title'):
		return TitleParser(title_id, language)  # type: ignore
	elif re.match(common.id_pattern, identificator):
		return TitleParser(identificator, language)
	else:
		return TitleNameParser(identificator)
