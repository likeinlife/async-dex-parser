import re
from .parse_title import ParseTitle, ParseTitleName, Chapter


def get_title(title_identificator: str):

    def __get_id_from_url(url: str) -> str | bool:
        clear_id = re.match(r'https://mangadex.org/title/([\w\W]*)/[\w\W]*', url)
        if clear_id is None:
            return False
        return clear_id.group(1)

    if title_id := __get_id_from_url(title_identificator):
        return ParseTitle(title_id)
    elif re.match(r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', title_identificator):
        return ParseTitle(title_identificator)
    else:
        return ParseTitleName(title_identificator)
