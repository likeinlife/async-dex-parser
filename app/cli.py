import argparse
from pathlib import Path

from app.actions import chapter_actions, fav_actions, title_actions


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

    subparsers = parser.add_subparsers(help="Available commands")

    chapter = subparsers.add_parser('chapter', help='Download chapter')
    chapter.add_argument('id', type=str, help='Chapter id or url')
    chapter.add_argument('--directory', '-d', help='Directory to save', default="")
    chapter.add_argument('--folder_name', '-n', help='Folder to save', default="")
    chapter.set_defaults(func=chapter_actions.get_chapter)

    title = subparsers.add_parser('title', help='See info about manga')
    title.add_argument('id', type=str, help='Title id or url or name', nargs=argparse.ONE_OR_MORE)
    title.add_argument('--language', '-l', help='Language. en/ru/...', default='en')
    title.add_argument('--add-fav', '-f', help='Add to favourite', action='store_true')
    title.add_argument('--mass',
                       '-m',
                       help='Download all chapters. By default download all en chapters',
                       action='store_true')
    title.add_argument('--directory', '-d', help='Directory for save', default="")
    title.add_argument('--folder-name', '-n', help='Folder to save', default="")
    title.add_argument('--show-id', '-show', help='Show chapters ids', action='store_true')
    title.add_argument('--cut-results', '-cut', help='Show only n results', type=int, default=0)
    title.set_defaults(func=title_actions.title_actions)

    fav = subparsers.add_parser('fav', help='Favourite list')
    fav_acts = fav.add_subparsers(help='Favourite list actions')
    fav_acts_list = fav_acts.add_parser('list', help='See your favourite list')
    fav_acts_list.add_argument('--language', '-l', help='Language. en/ru/...', default='en')
    fav_acts_list.set_defaults(func=fav_actions.see_favourite_list)

    fav_acts_add = fav_acts.add_parser('add', help='Add item to your favourite list')
    fav_acts_add.add_argument('name', help='Manga name')
    fav_acts_add.add_argument('id', help='Manga id')
    fav_acts_add.set_defaults(func=fav_actions.add_favourite_list_item)

    fav_acts_del = fav_acts.add_parser('del', help='Delete item from your favourite list')
    fav_acts_del.add_argument('num', type=int, help='Number in favourite list')
    fav_acts_del.set_defaults(func=fav_actions.delete_favourite_list_item)

    args = parser.parse_args()
    return args
