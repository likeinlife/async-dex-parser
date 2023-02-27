import re

id_pattern = '([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})'


def get_id_from_url(url: str, search_for: str) -> str | bool:
    url_pattern = re.compile(f'https://mangadex.org/{search_for}/{id_pattern}')
    clear_id = url_pattern.search(url)
    if clear_id is None:
        return False
    return clear_id.group(1)
