import argparse
import json
from pathlib import Path
import textwrap

from tabulate import tabulate  # type: ignore

from app import common
from app.logger_setup import get_logger
from app.config import config

from .title_actions import title_actions

BASEPATH = Path(__file__).parent.parent / 'favs.json'
logger = get_logger(__name__)


def check_if_favourite_list_empty():
    if BASEPATH.exists():
        logger.info(f'{BASEPATH} already exists')
        return False
    else:
        with open(BASEPATH, 'w', encoding='UTF-8') as file_obj:
            json.dump([], file_obj, ensure_ascii=False, indent=4)
        print('Favourite list does not exists. Just made one')
        logger.info(f'{BASEPATH} created')

    return True


def see_favourite_list(args: argparse.Namespace):
    if check_if_favourite_list_empty():
        return
    with open(BASEPATH, 'r') as file_obj:
        favs = json.load(file_obj)

    if not len(favs):
        exit('Favourite list is empty')

    headers = ('name', 'id')
    content = ((item['name'], item['id']) for item in favs)
    table = tabulate(content, headers=headers, showindex='always', stralign='center', tablefmt='rounded_outline')
    print(table)

    details = input('Details? y/n ')
    if not common.true_table.get(details):
        return
    while True:
        choosen_number = input('Enter number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        if 0 <= int(choosen_number) <= len(favs) - 1:
            id = favs[int(choosen_number)]['id']
            own_namepsace = argparse.Namespace(id=id, language=args.language, folder_name="", directory="")
            logger.info(f'Passing from fav_actions to title_actions {own_namepsace}')
            return title_actions(own_namepsace)
        print('There is no item with that number')


def delete_favourite_list_item(args: argparse.Namespace):
    if check_if_favourite_list_empty():
        return
    with open(BASEPATH, 'r') as file_obj:
        favs = json.load(file_obj)

    if not len(favs):
        exit('Favourite list is empty')

    if args.num > len(favs) - 1:
        exit('Not a valid number')

    with open(BASEPATH, 'r') as file_obj:
        favourites: list = json.load(file_obj)
        deleted: dict[str, str] = favourites.pop(args.num)
        logger.info(f'Deleting {deleted.get("name")} with {deleted.get("id")}')

    with open(BASEPATH, 'w') as file_obj:
        json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

    print(f'Deleted {deleted["name"]} with id {deleted["id"]} to favourite list')


def add_favourite_list_item(args: argparse.Namespace):
    short_name = textwrap.shorten(args.name, config.NAME_MAX_LENGTH, placeholder='...')
    logger.info(f'Adding to fav list {short_name} with {args.id}')
    if not (id := common.validate_id(args.id)):
        exit('Invalid id')
    title = {'name': short_name, 'id': id}

    if check_if_favourite_list_empty():
        with open(BASEPATH, 'w') as file_obj:
            json.dump([title], file_obj, indent=4, ensure_ascii=False)
            print(f'Added {title["name"]} with id {title["id"]} to favourite list')
            return

    with open(BASEPATH, 'r') as file_obj:
        favourites: list = json.load(file_obj)
        if title in favourites:
            print('Title already in favourites')
            return
        else:
            favourites.append(title)

    with open(BASEPATH, 'w') as file_obj:
        json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

    print(f'Added {title["name"]} with id {title["id"]} to favourite list')
