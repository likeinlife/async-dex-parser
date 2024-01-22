import re

from dex_parser import common

from .title_name_parser import TitleNameParser
from .title_parser import TitleParser


def get_title_parser(identification: str, language: str):
    if title_id := common.get_id_from_url(identification, 'title'):
        return TitleParser(title_id, language)
    elif re.match(common.id_pattern, identification):
        return TitleParser(identification, language)
    return TitleNameParser(identification)
