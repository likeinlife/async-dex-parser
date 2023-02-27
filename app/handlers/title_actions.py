from typing import Optional
from app import title_parser
import textwrap
import argparse
import tabulate  # type: ignore

from .chapter_actions import get_chapter

true_table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


def print_chapters(chapters: list[title_parser.Chapter], args: argparse.Namespace):
    if len(chapters) == 0:
        print('There are no chapters')
        return

    headers = ('chapter', 'language', 'id')
    content = ((chapter.chapter, chapter.lang, chapter.id) for chapter in chapters)

    table = (tabulate.tabulate(content,
                               headers=headers,
                               tablefmt='rounded_outline',
                               stralign='center',
                               numalign='right',
                               showindex='always'))

    print(table)

    copy = input('copy? y/n >> ')
    if not true_table.get(copy):
        return
    while True:
        choosen_number = input('chapter number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        own_namespace = argparse.Namespace(id=chapters[int(choosen_number)].id,
                                           folder_name=args.folder_name,
                                           directory=args.directory)
        return get_chapter(own_namespace)


def choose_title(title: title_parser.ParseTitle | title_parser.ParseTitleName) -> title_parser.ParseTitle:
    if isinstance(title, title_parser.ParseTitle):
        return title
    else:
        if (titles_count := len(title.titles)) == 1:
            return title_parser.ParseTitle(title.titles[0]['id'])
        print('There are more than 1 title found by this name')
        headers = ('name', 'id')
        content = ((textwrap.shorten(title['title'], 30), title['id']) for title in title.titles)
        table = (tabulate.tabulate(content,
                                   headers=headers,
                                   stralign='center',
                                   tablefmt='rounded_outline',
                                   showindex='always'))
        print(table)
        while True:
            choosen_number = input('title number? >> ')
            if not choosen_number.isnumeric():
                exit('Stopping')
            if int(choosen_number) <= titles_count - 1:
                return title_parser.ParseTitle(title.titles[int(choosen_number)]['id'])
            print('There is no title with that number')


def get_title(args: argparse.Namespace):
    identificator = " ".join(args.id)
    title = title_parser.get_title(identificator)
    title = choose_title(title)

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
    if true_table[approval]:
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        exit('Stopping')
