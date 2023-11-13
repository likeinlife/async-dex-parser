import argparse

from .commands import chapter, favourite_list, title

fav_commands = favourite_list.Commands


class MyParser(argparse.ArgumentParser):
	def parse_args(self, *args, **kwargs):
		output = super().parse_args(*args, **kwargs)
		if output == argparse.Namespace():
			self.print_help()
			exit(2)
		return output

	def error(self, message):
		print(f'error: {message}')
		self.print_help()
		exit(2)


def parse_args():
	prog = 'parser'
	description = 'MangaDex parser for titles and chapters.'
	parser = MyParser(prog=prog, description=description)

	subparsers = parser.add_subparsers(help='Available commands')

	chapter_sub = subparsers.add_parser('chapter', help='Download chapter')
	chapter_sub.add_argument('id', type=str, help='Chapter id or url')
	chapter_sub.add_argument('--directory', '-d', help='Directory to save', default='')
	chapter_sub.add_argument('--folder_name', '-n', help='Folder to save', default='')
	chapter_sub.set_defaults(func=chapter.entrypoint)

	title_sub = subparsers.add_parser('title', help='See info about manga')
	title_sub.add_argument('id', type=str, help='Title id or url or name', nargs=argparse.ONE_OR_MORE)
	title_sub.add_argument('--language', '-l', help='Language. en/ru/...', default='en')
	title_sub.add_argument('--add-fav', '-f', help='Add to favourite', action='store_true')
	title_sub.add_argument('--directory', '-d', help='Directory for save', default='')
	title_sub.add_argument(
		'--disable-creating-title-dir',
		'-dd',
		help='Disable creating directory for title',
		action='store_true',
	)
	title_sub.add_argument('--show-id', '-show', help='Show chapters ids', action='store_true')
	title_sub.add_argument('--cut-results', '-cut', help='Show only n results', type=int, default=0)
	title_sub.add_argument('--no-verbose', '-nv', help='Disable chapters list output', action='store_true')
	title_sub.set_defaults(func=title.entrypoint)

	fav = subparsers.add_parser('fav', help='Favourite list')

	fav_sub = fav.add_subparsers(help='Favourite list actions')
	fav_sub_get = fav_sub.add_parser('list', help='See your favourite list')
	fav_sub_get.set_defaults(func=fav_commands.print_favourite_list)

	fav_sub_download = fav_sub.add_parser('download', help='Download chapter from favourite list')
	fav_sub_download.add_argument('number', help='Title number', type=int)
	fav_sub_download.add_argument('--language', '-l', help='Language. en/ru/...', default='en')
	fav_sub_download.add_argument('--directory', '-d', help='Directory for save', default='')
	fav_sub_download.add_argument('--show-id', '-show', help='Show chapters ids', action='store_true')
	fav_sub_download.add_argument('--cut-results', '-cut', help='Show only n results', type=int, default=0)
	fav_sub_download.add_argument('--no-verbose', '-nv', help='Disable chapters list output', action='store_true')
	fav_sub_download.add_argument(
		'--disable-creating-title-dir',
		'-dd',
		help='Disable creating directory for title',
		action='store_true',
	)
	fav_sub_download.set_defaults(func=fav_commands.download)

	fav_sub_add = fav_sub.add_parser('add', help='Add item to your favourite list')
	fav_sub_add.add_argument('name', help='Manga name')
	fav_sub_add.add_argument('id', help='Manga id')
	fav_sub_add.set_defaults(func=fav_commands.add_item)

	fav_sub_del = fav_sub.add_parser('del', help='Delete item from your favourite list')
	fav_sub_del.add_argument('num', type=int, help='Number in favourite list')
	fav_sub_del.set_defaults(func=fav_commands.delete_item)

	fav_sub_update = fav_sub.add_parser('update', help='Update item name from your favourite list')
	fav_sub_update.add_argument('num', type=int, help='Number in favourite list')
	fav_sub_update.add_argument('name', type=str, help='New name', default=None)
	fav_sub_update.set_defaults(func=fav_commands.update_item)

	args = parser.parse_args()
	return args
