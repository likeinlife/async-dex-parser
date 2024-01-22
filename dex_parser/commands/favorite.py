import json
import textwrap
import uuid
from pathlib import Path
from typing import Annotated, Any, Optional, TypeAlias

import typer
from tabulate import tabulate

from dex_parser.config import config

FavoriteElement: TypeAlias = dict[str, Any]

FAVORITE_LIST_PATH = config.BASEPATH / 'favs.json'

router = typer.Typer(help='Favorite list actions')


@router.command()
def add(
    name: str,
    id: uuid.UUID,
):
    add_to_favorite_list(name, id)


@router.command()
def update(number: int, new_name: str):
    update_favorite_list(number, new_name)


@router.command(name='print')
def print_():
    print_favorite_list(read_favorite_list())


@router.command()
def download(
    number: int,
    language: Annotated[str, typer.Option('--language', '-l', help='Language')] = 'en',
    directory: Annotated[Optional[Path], typer.Option('--directory', '-d', help='Directory to save')] = None,
    show_id: Annotated[bool, typer.Option('--show-id', '-si', help="Show chapters' id")] = False,
    number_result: Annotated[Optional[int], typer.Option('--number-result', '-n', help='Show only n results')] = False,
    no_chapters_print: Annotated[
        bool, typer.Option('--no-chapters-print', '-no-print', help='Dont print chapters numbers')
    ] = False,
    disable_creating_title_dir: Annotated[
        bool,
        typer.Option(
            '--disable-title-dir',
            '-dd',
            help='Add to favorite list',
        ),
    ] = False,
):
    from .title import download_chapters, find_title

    favorite_list = read_favorite_list()

    if 0 <= int(number) < len(favorite_list):
        id = favorite_list[number]['id']
        title = find_title(identification=id, language=language)
    print(f'No item with number {number}')

    download_chapters(
        title=title,
        directory=directory,
        disable_creating_title_dir=disable_creating_title_dir,
        no_chapters_print=no_chapters_print,
        number_result=number_result,
        show_id=show_id,
    )


def write_favorite_list(favorite_list: list[FavoriteElement]) -> None:
    with open(FAVORITE_LIST_PATH, 'w', encoding='UTF-8') as file_obj:
        json.dump(favorite_list, file_obj, ensure_ascii=False, indent=4)


def read_favorite_list() -> list[FavoriteElement]:
    if not FAVORITE_LIST_PATH.exists():
        return []

    with open(FAVORITE_LIST_PATH, 'r') as file_obj:
        return json.load(file_obj)


def print_favorite_list(favourite_list: list[FavoriteElement]) -> None:
    headers = ('name', 'id')
    content = ((item['name'], item['id']) for item in favourite_list)
    table = tabulate(
        content,
        headers=headers,
        showindex='always',
        stralign='center',
        tablefmt='rounded_outline',
    )
    print(table)


def add_to_favorite_list(name: str, id: uuid.UUID):
    short_name = textwrap.shorten(name, config.NAME_MAX_LENGTH, placeholder='...')
    title = {'name': short_name, 'id': str(id)}
    favorite_list = read_favorite_list()

    if id in favorite_list:
        favorite_list.append(title)
        write_favorite_list(favorite_list)
        print(f'Add {title["name"]} with id {title["id"]} to favorite list')
    else:
        print(f'{id} already in favorites')


def update_favorite_list(number: int, new_name: str):
    favorite_list = read_favorite_list()

    if number > len(favorite_list) - 1:
        exit('Not a valid number')

    updated = favorite_list[number]
    previous_name = updated['name']
    updated['name'] = new_name

    write_favorite_list(favorite_list)

    print(f'Update {previous_name} with id {updated["id"]} to {new_name}')
