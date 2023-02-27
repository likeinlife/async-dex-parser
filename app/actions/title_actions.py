import argparse
import textwrap

from app import title_parser

from .chapter_actions import get_chapter

from app import common


def print_chapters(chapters: list[title_parser.Chapter], args: argparse.Namespace):
    if len(chapters) == 0:
        print('There are no chapters')
        return

    headers = ('chapter', 'language', 'id')
    content = ((chapter.chapter, chapter.lang, chapter.id) for chapter in chapters)

    table = common.basic_table(content, headers=headers, showindex='always')
    print(table)

    copy = input('copy? y/n >> ')
    if not common.true_table.get(copy):
        return
    while True:
        choosen_number = input('chapter number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        if int(choosen_number) <= len(chapters) - 1:
            own_namespace = argparse.Namespace(id=chapters[int(choosen_number)].id,
                                               folder_name=args.folder_name,
                                               directory=args.directory)
            return get_chapter(own_namespace)
        print('Invalid number')


def find_title(identificator: str) -> title_parser.ParseTitle:
    founded = title_parser.get_title(identificator)
    if isinstance(founded, title_parser.ParseTitle):
        return founded
    else:
        if len(founded) == 1:
            return title_parser.ParseTitle(identificator)
        else:
            return choose_title_by_name(founded)


def choose_title_by_name(title: title_parser.ParseTitleName):
    """If found several titles by this name"""
    print('There are more than 1 title found by this name')
    headers = ('name', 'id')
    content = ((textwrap.shorten(title['title'], 30), title['id']) for title in title.titles)
    table = common.basic_table(content, headers, showindex='always')

    print(table)
    while True:
        choosen_number = input('title number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        if int(choosen_number) <= len(title.titles) - 1:
            return title_parser.ParseTitle(title.titles[int(choosen_number)]['id'])
        print('Invalid number')


def get_title(args: argparse.Namespace):
    if isinstance(args.id, str):
        identificator = args.id
    else:
        identificator = " ".join(args.id)

    title = find_title(identificator)

    if args.language == 'any':
        chapters = title.chapters
    else:
        chapters = list(filter(lambda x: x.lang == args.language, title.chapters))
    if 'add_fav' in args and args.add_fav:
        from .fav_actions import add_favourite_list_item
        own_namespace = argparse.Namespace(name=title.title_name, id=title.id)
        add_favourite_list_item(own_namespace)

    if 'mass' in args and args.mass:
        title_mass_download(title, args)
    else:
        if len(chapters) == 0:
            print(f'There are no chapters with {args.language}. Try `-l any`')
            return
        print(f'{title.title_name: ^65}')
        print_chapters(chapters, args)


def title_mass_download(title: title_parser.ParseTitle, args: argparse.Namespace):
    chapter_number = len(list(filter(lambda chapter: chapter.lang == args.language, title.chapters)))
    approval = input(f'You want to download all chapters? Title - {title.title_name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if common.true_table[approval]:
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        exit('Stopping')
