from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from dex_parser.chapter_parser import ParseChapter


class BaseImageDownloader:
	def __init__(self, chapter: 'ParseChapter', directory: Path = Path(), folder_name: str = '') -> None:
		...

	def run(self) -> None:
		"""Run image downloading."""
