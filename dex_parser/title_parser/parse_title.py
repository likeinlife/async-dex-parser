import textwrap
import httpx
from pathlib import Path
from typing import NamedTuple, Tuple

import jmespath  # type: ignore

from dex_parser.chapter_parser import get_chapter
from dex_parser.headers import title_headers
from dex_parser.config import config
from dex_parser.logger_setup import get_logger
from dex_parser.common import clean_name
from .select_chapters import SelectChapters

logger = get_logger(__name__)


class Chapter(NamedTuple):
    id: str
    chapter: str
    language: str
    pages: int


class ParseTitle:

    def __init__(self, title_id: str, language: str = 'en') -> None:
        self.id = title_id
        self.language = language
        self.name: str = self.__getTitleName()
        self.__chapters: tuple[Chapter, ...] = self.__parseJson(self.__getJsonWithChapters())
        self.__filter_chapters()

    def __filter_chapters(self):
        if self.language == 'any':
            return
        self.__chapters = tuple(filter(lambda chapter: chapter.language == self.language, self.__chapters))

    def selectiveDownload(self, chapter_range: str, directory: Path = Path(), disable_creating_title_dir: bool = False):
        """Download chapters range
        Args:
            chapter_range: `10-24, 12, ~13`
        """
        logger.info(f'Downloading chapters range {chapter_range} from {self.name}')

        selected_chapters = SelectChapters(chapter_range)
        directory_for_title = self.__makeDirectory(directory, disable_creating_title_dir)
        for chapter_info in self.__chapters:
            if chapter_info.chapter in selected_chapters:
                chapter = get_chapter(chapter_info.id)
                chapter.downloadChapter(directory=directory_for_title)

    def massDownload(self, directory: Path = Path(), disable_creating_title_dir: bool = False):
        """Download all chapters from title"""
        logger.info(f'Downloading all chapters from manga {self.name}')

        directory_for_title = self.__makeDirectory(directory, disable_creating_title_dir)
        if not directory_for_title.exists():
            directory_for_title.mkdir()
        for chapter_info in self.__chapters:
            chapter = get_chapter(chapter_info.id)
            chapter.downloadChapter(directory=directory_for_title)

    def __getTitleName(self) -> str:
        """Get manga name"""

        json_response = httpx.get(
            f'https://api.mangadex.org/manga/{self.id}',
            verify=False,
            headers=title_headers,
        ).json()

        name = jmespath.search('data.attributes.title.* | [0]', json_response)
        logger.debug(f'Got name from {self.id}, {name}')

        return name

    def __getJsonWithChapters(self, offset: int = 0):

        json_response = httpx.get(
            f'https://api.mangadex.org/manga/{self.id}'
            f'/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'
            f'order[chapter]=desc&offset={offset}&contentRating[]=safe&contentRating[]=suggestive&'
            f'contentRating[]=erotica&contentRating[]=pornographic',
            verify=False,
            headers=title_headers,
        ).json()

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.__getJsonWithChapters(offset + limit))

        logger.debug(f'Got chapters from {self.id=}')

        return content

    @staticmethod
    def __parseJson(json_response: dict) -> Tuple[Chapter, ...]:
        chapters_data = jmespath.search('[*].[id, attrs.chapter, attrs.translatedLanguage, attrs.pages]', json_response)

        def __make_chapter(chapter_info) -> Chapter:
            return Chapter(*chapter_info)

        chapters_list = tuple(map(__make_chapter, chapters_data))

        return chapters_list

    def __makeDirectory(self, directory: Path, disable_creating_title_dir: bool = False):
        if disable_creating_title_dir:
            directory_for_title = directory
        else:
            clean_title_name = clean_name(self.name)
            short_name = textwrap.shorten(clean_title_name, config.NAME_MAX_LENGTH, placeholder='')
            directory_for_title = directory / short_name
        logger.info(f'Creating directory {directory_for_title}')

        if not directory_for_title.exists():
            directory_for_title.mkdir()
        logger.info(f'Directory for save: {directory_for_title}')
        return directory_for_title

    @property
    def chapters(self):
        return self.__chapters

    def __repr__(self) -> str:
        return f'{self.id}'
