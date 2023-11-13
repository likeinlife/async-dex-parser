import argparse

from dex_parser import chapter_parser, common


def entrypoint(args: argparse.Namespace):
	chapter = chapter_parser.get_chapter_parser(args.id)
	print(chapter)
	download = input('download? y/n ')
	if common.true_table.get(download):
		chapter.download_chapter(common.get_path(args.directory), args.folder_name)
