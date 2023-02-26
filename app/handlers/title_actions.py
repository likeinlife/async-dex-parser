from app import title_parser
import textwrap
import pyperclip  # type: ignore
import argparse
import tabulate  # type: ignore

table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


def print_chapters(chapters: list[title_parser.Chapter]):
    if len(chapters) == 0:
        print('There are no chapters')
        return

    headers = ('chapter', 'language', 'id')
    content = ((chapter.chapter, chapter.lang, chapter.id) for chapter in chapters)

    print(
        tabulate.tabulate(content,
                          headers=headers,
                          tablefmt='rounded_outline',
                          stralign='center',
                          numalign='right',
                          showindex='always'))

    copy = input('copy? y/n >> ')
    if not table.get(copy):
        return
    while True:
        choosen_number = input('chapter number? >> ')
        if not choosen_number.isnumeric():
            exit('Stopping')
        return pyperclip.copy(chapters[int(choosen_number)].id)


def choose_title(title: title_parser.ParseTitle | title_parser.ParseTitleName) -> title_parser.ParseTitle:
    if isinstance(title, title_parser.ParseTitle):
        return title
    else:
        if (titles_count := len(title.titles)) == 1:
            return title_parser.ParseTitle(title.titles[0]['id'])
        print('There are more than 1 title found by this name')
        headers = ('name', 'id')
        content = ((textwrap.shorten(title['title'], 30), title['id']) for title in title.titles)
        print(tabulate.tabulate(content, headers=headers, tablefmt='rounded_outline', showindex='always'))
        while True:
            choosen_number = input('title number? >> ')
            if not choosen_number.isnumeric():
                exit('Stopping')
            if int(choosen_number) <= titles_count - 1:
                return title_parser.ParseTitle(title.titles[int(choosen_number)]['id'])
            print('There is no title with that number')


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
        print(f'{title.title_name: ^65}')
        print_chapters(chapters)


def title_mass_download(title: title_parser.ParseTitle, args: argparse.Namespace):
    chapter_number = len(list(filter(lambda chapter: chapter.lang == args.language, title.chapters)))
    approval = input(f'You want to download all chapters? Title - {title.title_name}, chapters - {chapter_number}\n'\
                     f'y/n >> ')
    if table[approval]:
        title.massDownload(lang=args.language, directory=args.directory)
    else:
        print('Stopping')
