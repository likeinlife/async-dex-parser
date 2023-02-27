import argparse

from app import chapter_parser

table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}



def get_chapter(args: argparse.Namespace):
    chapter = chapter_parser.get_chapter(args.id)
    print(chapter)
    download = input('download? y/n ')
    if table.get(download):
        chapter.downloadChapter(args.directory, args.folder_name)
