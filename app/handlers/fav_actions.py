from pathlib import Path
import argparse
import json
import re
from tabulate import tabulate  # type: ignore

from .title_actions import get_title_info

BASEPATH = Path(__file__).parent.parent / 'favs.json'

true_table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


def validate_id(title_identificator: str) -> str:
    if re.match(r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', title_identificator):
        return title_identificator
    else:
        exit('Not a valid id')


def check_if_favourite_list_empty():
    if BASEPATH.exists():
        return False
    else:
        with open(BASEPATH, 'w', encoding='UTF-8') as file_obj:
            json.dump({}, file_obj, ensure_ascii=False, indent=4)
        print('Favourite list does not exists. Just made one')

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

    copy = input('Details? y/n ')
    if not true_table.get(copy):
        return
    while True:
        choosen_number = input('title number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        if int(choosen_number) <= len(favs) - 1:
            return get_title_info(args, favs[int(choosen_number)]['id'])
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

    with open(BASEPATH, 'w') as file_obj:
        json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

    print(f'Deleted {deleted["name"]} with id {deleted["id"]} to favourite list')


def add_favourite_list_item(args: argparse.Namespace):
    title = {'name': args.name, 'id': validate_id(args.id)}
    if check_if_favourite_list_empty():
        with open(BASEPATH, 'w') as file_obj:
            json.dump([title], file_obj, indent=4, ensure_ascii=False)
            print(f'Added {title["name"]} with id {title["id"]} to favourite list')
            return

    with open(BASEPATH, 'r') as file_obj:
        favourites: list = json.load(file_obj)
        favourites.append(title)

    with open(BASEPATH, 'w') as file_obj:
        json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

    print(f'Added {title["name"]} with id {title["id"]} to favourite list')

