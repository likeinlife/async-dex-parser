from pathlib import Path
from typing import Annotated, Optional

import typer

from dex_parser import chapter_parser, downloader

router = typer.Typer(help='Chapters actions')


@router.command()
def download(
	chapter_identification: str,
	directory: Annotated[Optional[Path], typer.Option('--directory', '-d', help='Directory to save')] = None,
	folder_name: Annotated[Optional[str], typer.Option('--folder-name', '-f', help='Folder name')] = None,
):
	chapter = chapter_parser.get_chapter_parser(chapter_identification)
	typer.confirm('Download chapter?', abort=True)
	downloader.ImageDownloader(chapter, directory=directory, folder_name=folder_name).run()
