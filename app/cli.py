import argparse
from pathlib import Path

from app.handlers import title_actions, chapter_actions, fav_actions


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

    subparsers = parser.add_subparsers()

    chapter = subparsers.add_parser('chapter', help='Download chapter by its id')
    chapter.add_argument('id', type=str, help='Chapter id or url')
    chapter.add_argument('--directory', '-d', help='Directory to save', default=Path())
    chapter.add_argument('--folder_name', '-n', help='Folder to save', default="")
    chapter.set_defaults(func=chapter_actions.get_chapter)

    title = subparsers.add_parser('title', help='Title info')
    title.add_argument('id', type=str, help='Title id or url or name', nargs=argparse.ONE_OR_MORE)
    title.add_argument('--language', '-l', help='Language', default='en', choices=('ru', 'en', 'any'))
    title.add_argument('--mass',
                       '-m',
                       help='Download all chapters. By default download all en chapters',
                       action='store_true')
    title.add_argument('--directory', '-d', help='Directory for save', default=Path())
    title.set_defaults(func=title_actions.get_title_info)

    favs = subparsers.add_parser('fav', help='Actions with favourite list')
    favs.add_argument('action', choices=('list', 'add', 'del'))
    favs.add_argument('--id', '-id', help='Title id')
    favs.add_argument('--title', '-t', help='Title name')
    favs.set_defaults(func=fav_actions.FavouriteList())

    args = parser.parse_args()
    return args
