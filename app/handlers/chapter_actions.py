import argparse
from typing import Optional
from app import chapter_parser

table = {'y': True, 'yes': True, 'Y': True, 'n': False, 'not': False}


def get_chapter_id(args: argparse.Namespace, chapter_id: Optional[str]):
    if chapter_id:
        return chapter_id
    return args.id


def get_chapter(args: argparse.Namespace, chapter_id: Optional[str] = None):
    chapter = chapter_parser.get_chapter(get_chapter_id(args, chapter_id))
    print(chapter)
    download = input('download? y/n ')
    if table.get(download):
        chapter_parser.ImageDownloader(chapter, args.directory, args.folder_name)
