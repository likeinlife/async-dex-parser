from app import title_parser
import textwrap
import pyperclip
import argparse

table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


def print_chapters(chapters: list[title_parser.Chapter]):
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


def choose_title(title: title_parser.ParseTitle | title_parser.ParseTitleName) -> title_parser.ParseTitle:
    if isinstance(title, title_parser.ParseTitle):
        return title
    else:
        if len(title.titles) == 1:
            return title_parser.ParseTitle(title.titles[0]['id'])
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
                    return title_parser.ParseTitle(this_title['id'])
            print('There is no number. Try again')


def get_title_info(args: argparse.Namespace):
    identificator = " ".join(args.id)
    title = title_parser.get_title(identificator)
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
    else:
        print(f'| {title.title_name: ^60} |')
    print(f'| {"-" * 58: ^60} |')
    print(f'| {"num": >3} | {"ch": ^6} | {"lang": ^6} | {"id": ^36} |')
    print(f'| {"---": >3} | {"--": ^6} | {"----": ^6} | {"-"*34: ^36} |')


def title_mass_download(title: title_parser.ParseTitle, args: argparse.Namespace):
    chapter_number = len(list(filter(lambda chapter: chapter.lang == args.language, title.chapters)))
    approval = input(f'You want to download all chapters? Title - {title.title_name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if table[approval]:
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        print('Stopping')
