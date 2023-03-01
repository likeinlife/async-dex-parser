import argparse
import textwrap

from app import common, title_parser
from app.common import Words
from app.config import config

from .chapter_actions import get_chapter


def print_chapters(chapters: list[title_parser.Chapter], args: argparse.Namespace):
    if len(chapters) == 0:
        exit(Words.NO_CHAPTERS)

    headers = ('chapter', 'language', 'pages')
    content = ((chapter.chapter, chapter.language, chapter.pages) for chapter in chapters)

    table = common.basic_table(content, headers=headers)
    print(table)

    download = input('Download chapter? y/n >> ')
    if not common.true_table.get(download):
        return
    while True:
        choosen_number = input('Chapter number? >> ')
        if not choosen_number.isnumeric():
            exit(Words.STOP)
        if 0 <= int(choosen_number) <= len(chapters) - 1:
            own_namespace = argparse.Namespace(id=chapters[int(choosen_number)].id,
                                               folder_name=args.folder_name,
                                               directory=args.directory)
            return get_chapter(own_namespace)
        print(Words.INVALID_NUMBER)


def find_title(identificator: str) -> title_parser.ParseTitle:
    founded = title_parser.get_title(identificator)
    if isinstance(founded, title_parser.ParseTitle):
        return founded
    else:
        if len(founded) == 1:
            return title_parser.ParseTitle(founded[0]['id'])
        else:
            return choose_title_by_name(founded)


def choose_title_by_name(title: title_parser.ParseTitleName):
    """If found several titles by this name"""
    print('There are more than 1 title found by this name')
    headers = ('name', 'id')
    content = ((textwrap.shorten(title['title'], config.NAME_MAX_LENGTH, placeholder='...'), title['id'])
               for title in title.titles)
    table = common.basic_table(content, headers, showindex='always')

    print(table)
    while True:
        choosen_number = input('Title number? >> ')
        if not choosen_number.isnumeric():
            exit(Words.STOP)
        if 0 <= int(choosen_number) <= len(title.titles) - 1:
            return title_parser.ParseTitle(title.titles[int(choosen_number)]['id'])
        print(Words.INVALID_NUMBER)


def get_identificator(args: argparse.Namespace):
    if isinstance(args.id, str):
        return args.id
    else:
        return " ".join(args.id)


def filter_chapters_by_language(title: title_parser.ParseTitle, language: str) -> list[title_parser.Chapter]:
    if language == 'any':
        return title.chapters
    return list(filter(lambda chapter: chapter.language == language, title.chapters))


def add_to_favourite(title: title_parser.ParseTitle, args: argparse.Namespace):
    if 'add_fav' in args and args.add_fav:
        from .fav_actions import add_favourite_list_item
        own_namespace = argparse.Namespace(name=title.title_name, id=title.id)
        add_favourite_list_item(own_namespace)


def get_title(args: argparse.Namespace):
    identificator = get_identificator(args)
    title = find_title(identificator)

    chapters = filter_chapters_by_language(title, args.language)

    add_to_favourite(title, args)
    if 'mass' in args and args.mass:
        title_mass_download(title, args)
    else:
        if len(chapters) == 0:
            print(f'There are no chapters with {args.language}. Try `-l any`')
            return
        print(f'{title.title_name: ^65}')
        print_chapters(chapters, args)


def title_mass_download(title: title_parser.ParseTitle, args: argparse.Namespace):
    chapter_number = len(filter_chapters_by_language(title, args.language))
    approval = input(f'You want to download all chapters? Title - {title.title_name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if common.true_table.get(approval):
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        exit('Stopping')
