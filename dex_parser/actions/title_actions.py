import argparse
import textwrap
import itertools

from dex_parser import common, title_parser
from dex_parser.common import Words
from dex_parser.config import config
from dex_parser.logger_setup import get_logger

logger = get_logger(__name__)


class MakeChaptersTable:

    def __init__(self, title: title_parser.ParseTitle, args: argparse.Namespace) -> None:
        self.title = title
        self.args = args
        self.content, self.headers = self.__check_option_show_id()
        self.__check_option_cut_results()

    def __check_no_verbose(self) -> bool:
        if 'no_verbose' in self.args and self.args.no_verbose:
            return True
        return False

    def __check_option_cut_results(self):
        if 'cut_results' in self.args and self.args.cut_results:
            self.content = itertools.islice(self.content, self.args.cut_results)

    def __check_option_show_id(self):
        if 'show_id' in self.args and self.args.show_id:
            headers = ('chapter', 'language', 'pages', 'id')
            content = [(ch.chapter, ch.language, ch.pages, ch.id) for ch in self.title.chapters]
        else:
            headers = ('chapter', 'language', 'pages')  # type: ignore
            content = [(ch.chapter, ch.language, ch.pages) for ch in self.title.chapters]

        return content, headers

    def __str__(self):
        if self.__check_no_verbose():
            return 'No verbose'
        return common.basic_table(self.content, self.headers)


def print_chapters(title: title_parser.ParseTitle, args: argparse.Namespace):
    if len(title.chapters) == 0:
        exit(Words.NO_CHAPTERS)

    print(f'{title.name: ^65}')
    print(MakeChaptersTable(title, args))

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
        return title.selectiveDownload(
            choosen_range,
            common.get_path(args.directory),
            args.disable_creating_title_dir,
        )


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
        title.massDownload(common.get_path(args.directory), args.disable_creating_title_dir)
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
    if len(title.chapters) == 0:
        exit(f'There are no chapters with {args.language}. Try `-l any`')

    add_to_favourite(title, args)
    if 'mass' in args and args.mass:
        title_mass_download(title, args)
    else:
        print_chapters(title, args)
