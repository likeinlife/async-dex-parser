import re
from functools import partial
from typing import Sequence, TypeVar

import typer
from tabulate import tabulate

id_pattern = '([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})'
true_table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}

basic_table = partial(tabulate, tablefmt='rounded_outline', stralign='center', numalign='left')

T = TypeVar('T')


def choose(collection: Sequence[T]) -> T:
    number: int
    number = typer.prompt('Enter number', type=int)
    if not 0 <= number < len(collection):
        print('Incorrect number')
        return choose(collection)
    return collection[number]


def get_clean_path(name: str) -> str:
    """Delete invalid symbols for Windows file name"""
    return re.sub(r'[;<>|/\:"?]', '', name)


def get_id_from_url(url: str, search_for: str) -> str | None:
    url_pattern = re.compile(f'https://mangadex.org/{search_for}/{id_pattern}')
    clear_id = url_pattern.search(url)
    if clear_id is None:
        return None
    return clear_id.group(1)
