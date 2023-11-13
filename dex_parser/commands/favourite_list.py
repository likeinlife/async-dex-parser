import argparse
import json
import textwrap
from typing import Any, TypeAlias

from tabulate import tabulate  # type: ignore

from dex_parser import common
from dex_parser.config import config

from .title import entrypoint

FavouriteElement: TypeAlias = dict[str, Any]

FAVOURITE_LIST_PATH = config.BASEPATH / 'favs.json'


class Commands:
	@staticmethod
	def download(args: argparse.Namespace):
		"""Download one of favourite list."""
		favourite_list = read_favourite_list()

		if 0 <= int(args.number) <= len(favourite_list) - 1:
			id = favourite_list[args.number]['id']
			args.id = id
			return entrypoint(args)
		print(f'There is no item with number {args.number}')

	@staticmethod
	def print_favourite_list(args: argparse.Namespace) -> None:
		favourite_list = read_favourite_list()
		print_favourite_list(favourite_list)

	@staticmethod
	def delete_item(args: argparse.Namespace):
		favourite_list = read_favourite_list()

		if args.num > len(favourite_list) - 1:
			exit('Not a valid number')

		deleted: dict[str, str] = favourite_list.pop(args.num)

		write_favourite_list_file(favourite_list)

		print(f'Deleted {deleted["name"]} with id {deleted["id"]} to favourite list')

	@staticmethod
	def add_item(args: argparse.Namespace):
		short_name = textwrap.shorten(args.name, config.NAME_MAX_LENGTH, placeholder='...')
		if not (id := common.validate_id(args.id)):
			exit('Invalid id')
		title = {'name': short_name, 'id': id}
		favourite_list = read_favourite_list()

		if id in favourite_list:
			favourite_list.append(title)
			write_favourite_list_file(favourite_list)
			print(f'Add {title["name"]} with id {title["id"]} to favourite list')
		else:
			print(f'{id} already in favourites')

	@staticmethod
	def update_item(args: argparse.Namespace):
		favs = read_favourite_list()

		if args.num > len(favs) - 1:
			exit('Not a valid number')

		with open(FAVOURITE_LIST_PATH, 'r') as file_obj:
			favourite_list: list[FavouriteElement] = json.load(file_obj)

			updated = favourite_list[args.num]
			previous_name = updated['name']
			updated['name'] = args.name

		with open(FAVOURITE_LIST_PATH, 'w') as file_obj:
			json.dump(favourite_list, file_obj, ensure_ascii=False, indent=4)

		print(f'Updated {previous_name} with id {updated["id"]} to {args.name}')


def write_favourite_list_file(favourite_list: list[FavouriteElement]) -> None:
	with open(FAVOURITE_LIST_PATH, 'w', encoding='UTF-8') as file_obj:
		json.dump(favourite_list, file_obj, ensure_ascii=False, indent=4)


def read_favourite_list() -> list[FavouriteElement]:
	if not FAVOURITE_LIST_PATH.exists():
		return []

	with open(FAVOURITE_LIST_PATH, 'r') as file_obj:
		favs = json.load(file_obj)

	return favs


def print_favourite_list(favourite_list: list[FavouriteElement]) -> None:
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
