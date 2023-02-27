import re

from .parse_title import Chapter, ParseTitle, ParseTitleName
from app import common


def get_title(identificator: str):

    if title_id := common.get_id_from_url(identificator, 'title'):
        return ParseTitle(title_id)
    elif re.match(common.id_pattern, identificator):
        return ParseTitle(identificator)
    else:
        return ParseTitleName(identificator)
