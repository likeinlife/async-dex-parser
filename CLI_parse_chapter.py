import argparse
import json
import sys
from pathlib import Path
import textwrap

import pyperclip

import parse_chapter
import parse_title

table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


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
    download = input('download? y/n ')
    if table.get(download):
        parse_chapter.ImageDownloader(chapter, args.directory, args.folder_name)


def print_chapters(chapters: list[parse_title.Chapter]):
    if len(chapters) == 0:
        print('There are no chapters')
        return
    for number, chapter in enumerate(chapters):
        print(f'| {number: >3} | {chapter.chapter: ^6} | {chapter.lang: ^6} | {chapter.id} |')
    print(f'  {"-" * 58: ^60} ')
    copy = input('copy? y/n ')
    if copy == 'n':
        return
    while True:
        choosen_number = input('chapter number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        for number, chapter in enumerate(chapters):
            if number == int(choosen_number):
                return pyperclip.copy(chapter.id)


def choose_title(title: parse_title.ParseTitle | parse_title.ParseTitleName) -> parse_title.ParseTitle:
    if isinstance(title, parse_title.ParseTitle):
        return title
    else:
        print('There are more than 1 title found by this name')
        print(f'| {"num": ^3} | {"name": ^30} | {"id": ^36} |')
        print(f'| {"---": ^3} | {"-" * 30: ^30} | {"-" * 36: ^36} |')
        for number, this_title in enumerate(title.titles):
            title_name = textwrap.shorten(this_title['title'], 30)
            print(f'| {number: ^3} | {title_name: ^30} | {this_title["id"]: ^36} |')
        print(f'  {"-" * 72: ^75}  ')
        while True:
            choosen_number = input('title number? >> ')
            if not choosen_number.isnumeric():
                exit('Stopping')
            for number, this_title in enumerate(title.titles):
                if number == int(choosen_number):
                    return parse_title.ParseTitle(this_title['id'])
            print('There is no number. Try again')


def get_title_info(args: argparse.Namespace):
    title = parse_title.get_title(args.id)
    title = choose_title(title)

    if args.language == 'any':
        chapters = title.chapters
    else:
        chapters = list(filter(lambda x: x.lang == args.language, title.chapters))
    if args.mass:
        title_mass_download(title, args)
    else:
        if len(chapters) == 0:
            print(f'There are no chapters with {args.language}. Try `-l any`')
            return
        print_beauty_table_begin(title)
        print_chapters(chapters)


def print_beauty_table_begin(title):
    if (title_length := len(title.title_name)) > 55:
        parts_number = title_length // 55 + 1
        for part in range(parts_number):
            print(f'| {title.title_name[part*54: part*54 + 54]: ^60} |')
    print(f'| {"-" * 58: ^60} |')
    print(f'| {"num": >3} | {"ch": ^6} | {"lang": ^6} | {"id": ^36} |')
    print(f'| {"---": >3} | {"--": ^6} | {"----": ^6} | {"-"*34: ^36} |')


def title_mass_download(title: parse_title.ParseTitle, args: argparse.Namespace):
    chapter_number = len(list(filter(lambda chapter: chapter.lang == args.language, title.chapters)))
    approval = input(f'You want to download all chapters? Title - {title.title_name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if table[approval]:
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        print('Stopping')


def parse_args():
    parser = MyParser()

    subparsers = parser.add_subparsers()

    chapter = subparsers.add_parser('chapter', help='Download chapter by its id')
    chapter.add_argument('id', type=str, help='Chapter id or url')
    chapter.add_argument('--directory', '-d', help='Directory to save', default=Path())
    chapter.add_argument('--folder_name', '-n', help='Folder to save', default="")
    chapter.set_defaults(func=get_chapter_info)

    title = subparsers.add_parser('title', help='Title info')
    title.add_argument('id', type=str, help='Title id or url or name')
    title.add_argument('--language', '-l', help='Language', default='en', choices=('ru', 'en', 'any'))
    title.add_argument('--mass',
                       '-m',
                       help='Download all chapters. By default download all en chapters',
                       action='store_true')
    title.add_argument('--directory', '-d', help='Directory for save', default=Path())
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
