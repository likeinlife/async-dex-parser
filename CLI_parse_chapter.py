import argparse
import json
import parse_chapter
import parse_title
from pathlib import Path
import sys
import pyperclip


class MyParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
        output = super().parse_args(*args, **kwargs)
        if output == argparse.Namespace():
            self.print_help()
            sys.exit(2)
        return output

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def get_chapter_info(args: argparse.Namespace):
    chapter = parse_chapter.get_chapter(args.id)
    print(chapter)
    table = {'y': True}
    download = input('download? y/n ')
    if table.get(download):
        parse_chapter.ImageDownloader(chapter, args.directory, args.folder_name)


def get_title_info(args: argparse.Namespace):
    title = parse_title.get_title(args.id)
    chapters = list(filter(lambda x: x.lang == args.language, title.chapters))
    for number, chapter in enumerate(chapters):
        print(f'{number: >3} | {chapter.chapter: ^5} | {chapter.lang} | {chapter.id}')
    copy = input('copy? y/n ')
    if copy == 'n':
        return
    chapter_number = int(input('chapter number? >> '))
    for number, chapter in enumerate(chapters):
        if number == chapter_number:
            pyperclip.copy(chapter.id)


def parse_args():
    parser = MyParser()

    subparsers = parser.add_subparsers()

    chapter = subparsers.add_parser('chapter', help='Download chapter by its id')
    chapter.add_argument('id', type=str, help='Chapter id or url')
    chapter.add_argument('--directory', '-d', help='Directory to save', default=Path())
    chapter.add_argument('--folder_name', '-n', help='Folder to save', default="")
    chapter.set_defaults(func=get_chapter_info)

    title = subparsers.add_parser('title', help='Title info')
    title.add_argument('id', type=str, help='Title id or url')
    title.add_argument('--language', '-l', help='Language', default='en', choices=('ru', 'en', 'any'))
    title.set_defaults(func=get_title_info)

    favs = subparsers.add_parser('fav', help='Actions with favourite list')
    favs.add_argument('action', choices=('list', 'add', 'del'))
    favs.add_argument('--id', '-id', help='Title id')
    favs.add_argument('--title', '-t', help='Title name')
    favs.set_defaults(func=FavouriteList())

    args = parser.parse_args()
    return args


class FavouriteList:
    BASEPATH = Path(__file__).parent / 'favs.json'

    def __call__(self, args):
        action = args.action
        table = {
            'list': self.list,
            'add': self.add,
            'del': self.delete,
        }
        return table[action](args)

    def checkFavListIsEmpty(self):
        global abs_path_to_fav
        if self.BASEPATH.exists():
            if self.BASEPATH.__sizeof__():
                return False
        else:
            with open(self.BASEPATH, 'w', encoding='UTF-8') as file_obj:
                json.dump({}, file_obj, ensure_ascii=False, indent=4)
            print('Favourite list does not exists. Just made one')

        return True

    def list(self, _):
        if self.checkFavListIsEmpty():
            return
        with open(self.BASEPATH, 'r') as file_obj:
            favs = json.load(file_obj)

        for number, (title_id, title_name) in enumerate(favs.items()):
            print(f'{number: >3} | {title_id} | {title_name}')

        copy = input('Copy? y/n ')
        if copy == 'n':
            return
        chapter_number = int(input('chapter number? >> '))
        for number, (title_id, title_name) in enumerate(favs.items()):
            if number == chapter_number:
                pyperclip.copy(title_id)

    def add(self, args):
        title = {args.title: args.id}
        if self.checkFavListIsEmpty():
            with open(self.BASEPATH, 'w') as file_obj:
                json.dump(title, file_obj, indent=4, ensure_ascii=False)
                return

        with open(self.BASEPATH, 'r') as file_obj:
            favourites: dict = json.load(file_obj)
            favourites.update(title)

        with open(self.BASEPATH, 'w') as file_obj:
            json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

        print(f'Add {args.title}')

    def delete(self, args):
        with open(self.BASEPATH, 'r') as file_obj:
            favourites: dict = json.load(file_obj)

        if args.id in favourites:
            favourites.pop(args.id)
            print(f"deleted {args.id}")
        else:
            print("Element not found")
            return

        with open(self.BASEPATH, 'w') as file_obj:
            json.dump(favourites, file_obj)
            return


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
