import re
from functools import partial
from pathlib import Path

from tabulate import tabulate  # type: ignore

id_pattern = '([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})'
true_table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}

basic_table = partial(tabulate, tablefmt='rounded_outline', stralign='center', numalign='left')


def get_path(path: str) -> Path:
	if path.replace(' ', '.') == '.':
		return Path('.')
	return Path(path)


def clean_name(name: str) -> str:
	"""Delete invalid symbols for Windows file name"""
	return re.sub(r'[;<>|/\:"?]', '', name)


def get_id_from_url(url: str, search_for: str) -> str | bool:
	url_pattern = re.compile(f'https://mangadex.org/{search_for}/{id_pattern}')
	clear_id = url_pattern.search(url)
	if clear_id is None:
		return False
	return clear_id.group(1)


def validate_id(identificator: str) -> str | bool:
	if re.match(id_pattern, identificator):
		return identificator
	else:
		return False


class Words:
	STOP = 'Stopping'
	INVALID_NUMBER = 'Invalid number'
	NO_CHAPTERS = 'There are no chapters'
	CHAPTER_SELECT_HELP = """Example: 1, 2, 4-10, ~2-7, ~8. \nIt selects 1, 9, 10 chapters.
1 | 1-10 - Include
~1 | ~1-10 - Exclude
* - Selects all chapters"""
