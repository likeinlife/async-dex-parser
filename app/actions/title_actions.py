import argparse
import textwrap

from app import common, title_parser
from app.common import Words
from app.config import config
from app.logger_setup import get_logger

logger = get_logger(__name__)


def print_chapters(title: title_parser.ParseTitle, args: argparse.Namespace):
    if len(title.chapters) == 0:
        exit(Words.NO_CHAPTERS)

    headers = ('chapter', 'language', 'pages')
    content = ((chapter.chapter, chapter.language, chapter.pages) for chapter in title.chapters)

    table = common.basic_table(content, headers=headers)
    print(table)

    download = input('Download chapter(s)? y/n >> ')
    if not common.true_table.get(download):
        return
    while True:
        choosen_range = input('Enter chapter(s) `.h for help` >> ')
        if choosen_range == '.h':
            print(Words.CHAPTER_SELECT_HELP)
            continue
        confirm = input(f'You are going to download chapters {choosen_range} from {title.name}. y/n >> ')
        if not common.true_table.get(confirm):
            exit(Words.STOP)
        return title.selectiveDownload(choosen_range, common.get_path(args.directory))


def choose_title_by_name(title: title_parser.ParseTitleName, args: argparse.Namespace):
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
            return title_parser.ParseTitle(title.titles[int(choosen_number)]['id'], args.language)
        print(Words.INVALID_NUMBER)


def get_identificator(args: argparse.Namespace):
    """args.id might be manga name or id
    case name: (Test, manga, name) - tuple
    case id: 11a98sdj9a - str
    case name with one word: (Test,) - tuple
    """
    if isinstance(args.id, str):
        return args.id
    else:
        return " ".join(args.id)


def add_to_favourite(title: title_parser.ParseTitle, args: argparse.Namespace):
    if 'add_fav' in args and args.add_fav:
        from .fav_actions import add_favourite_list_item
        own_namespace = argparse.Namespace(name=title.name, id=title.id)
        add_favourite_list_item(own_namespace)


def title_mass_download(title: title_parser.ParseTitle, args: argparse.Namespace):
    chapter_number = title
    approval = input(f'You want to download all chapters? Title - {title.name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if common.true_table.get(approval):
        title.massDownload(directory=common.get_path(args.directory))
    else:
        exit('Stopping')


def find_title(identificator: str, args: argparse.Namespace) -> title_parser.ParseTitle:
    """Find title(s) by identificator: url, id, name"""
    founded = title_parser.get_title(identificator, args.language)
    if isinstance(founded, title_parser.ParseTitle):
        return founded
    else:
        if len(founded) == 1:
            return title_parser.ParseTitle(founded[0]['id'], args.language)  # type: ignore
        else:
            return choose_title_by_name(founded, args)


def title_actions(args: argparse.Namespace):
    """Entry point"""
    identificator = get_identificator(args)
    title = find_title(identificator, args)

    add_to_favourite(title, args)
    if 'mass' in args and args.mass:
        title_mass_download(title, args)
    else:
        if len(title.chapters) == 0:
            print(f'There are no chapters with {args.language}. Try `-l any`')
            return
        print(f'{title.name: ^65}')
        print_chapters(title, args)
