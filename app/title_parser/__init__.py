import re

from app import common

from .parse_title import Chapter, ParseTitle
from .parse_title_name import ParseTitleName


def get_title(identificator: str):

    if title_id := common.get_id_from_url(identificator, 'title'):
        return ParseTitle(title_id)  # type: ignore
    elif re.match(common.id_pattern, identificator):
        return ParseTitle(identificator)
    else:
        return ParseTitleName(identificator)
