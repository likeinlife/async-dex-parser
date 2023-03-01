import json
import ssl
import textwrap
import urllib.request
from pathlib import Path
from typing import NamedTuple, Tuple
import http.client
import time

import jmespath  # type: ignore

from app.chapter_parser import get_chapter
from app.headers import title_headers
from app.config import config


class Chapter(NamedTuple):
    id: str
    chapter: str
    language: str
    pages: int


class SelectChapters:
    """Select chapter ranges like `1, 2, 2-10, 20-30, ~8`"""

    def __init__(self, chapters_select: str) -> None:
        self.input = chapters_select.replace(' ', '').split(',')
        self.include, self.exclude = self.__make_lists()

    def __contains__(self, number: str) -> bool:
        """Check if this chapter in range"""
        include_flag = any(map(lambda x: self.__check_number(x, number), self.include))
        exclude_flag = not any(map(lambda x: self.__check_number(x, number), self.exclude))
        if include_flag and exclude_flag:
            return True
        return False

    def __make_lists(self):
        include = []
        exclude = []
        for item in self.input:
            if '~' in item:
                exclude.append(self.__make_range(item))
            else:
                include.append(self.__make_range(item))
        return include, exclude

    def __make_range(self, number: str):
        number = number.replace('~', '')
        if number.isnumeric():
            return float(number)
        elif '-' in number:
            return self.__get_start_and_end(number)
        else:
            exit(f'Something went wrong with chapter range {number}')

    def __get_start_and_end(self, chapter_range: str) -> Tuple[float, float]:
        """Transform '1-20' to tuple(1, 20)"""
        start, end = list(map(self.__make_range, chapter_range.split('-')))

        if isinstance(start, float) and isinstance(end, float):
            return start, end
        else:
            exit(f'Something went wrong with chapter range {chapter_range}')

    @staticmethod
    def __check_number(chapter_range: float | Tuple[float, float], value_to_check: str) -> bool:
        """Check number if it is in :chapter_range:"""
        if isinstance(chapter_range, float):
            if float(value_to_check) == chapter_range:
                return True
        if isinstance(chapter_range, tuple):
            if chapter_range[0] <= float(value_to_check) <= chapter_range[1]:
                return True
        return False

    def __repr__(self) -> str:
        return f'{self.include}; excluding {self.exclude}'


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

    def selectiveDownload(self, chapter_range: str, lang: str = 'en', directory: Path = Path()):
        selected_chapters = SelectChapters(chapter_range)
        directory_for_title = self.__makeDirectoryName(directory)
        if not directory_for_title.exists():
            directory_for_title.mkdir()
        for chapter_info in self.__chapters:
            if chapter_info.language == lang and chapter_info.chapter in selected_chapters:
                chapter = get_chapter(chapter_info.id)
                chapter.downloadChapter(directory=directory_for_title)

    def massDownload(self, lang: str = 'en', directory: Path = Path()):
        directory_for_title = self.__makeDirectoryName(directory)
        if not directory_for_title.exists():
            directory_for_title.mkdir()
        for chapter_info in self.__chapters:
            if chapter_info.language == lang:
                chapter = get_chapter(chapter_info.id)
                chapter.downloadChapter(directory=directory_for_title)

    def __getTitleName(self) -> str:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(f'https://api.mangadex.org/manga/{self.id}')
        for key, value in title_headers.items():
            req.add_header(key, value)

        current_reconnect = 0
        while True:
            try:
                json_response = json.load(urllib.request.urlopen(req, context=ctx))
                break
            except http.client.IncompleteRead as e:
                print(f'Sever disconnected. Continue in {config.SLEEP_BEFORE_RECONNECTION} sec...')
                current_reconnect += 1
                time.sleep(config.SLEEP_BEFORE_RECONNECTION)
                if current_reconnect >= config.TRIES_NUMBER:
                    raise e

        name = jmespath.search('data.attributes.title.* | [0]', json_response)

        return name

    def __getJsonWithChapters(self, offset: int = 0):

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(f'https://api.mangadex.org/manga/{self.id}'\
            f'/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'\
            f'order[chapter]=desc&offset={offset}&contentRating[]=safe&contentRating[]=suggestive&'\
            f'contentRating[]=erotica&contentRating[]=pornographic')
        for key, value in title_headers.items():
            req.add_header(key, value)

        current_reconnect = 0
        while True:
            try:
                json_response = json.load(urllib.request.urlopen(req, context=ctx))
                break
            except http.client.IncompleteRead as e:
                print(f'Sever disconnected. Continue in {config.SLEEP_BEFORE_RECONNECTION} sec...')
                current_reconnect += 1
                time.sleep(config.SLEEP_BEFORE_RECONNECTION)
                if current_reconnect >= config.TRIES_NUMBER:
                    raise e

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.__getJsonWithChapters(offset + limit))

        return content

    @staticmethod
    def __parseJson(json_response: dict) -> Tuple[Chapter, ...]:
        chapters_data = jmespath.search('[*].[id, attrs.chapter, attrs.translatedLanguage, attrs.pages]', json_response)

        def __make_chapter(chapter_info) -> Chapter:
            return Chapter(*chapter_info)

        chapters_list = tuple(map(__make_chapter, chapters_data))

        return chapters_list

    def __makeDirectoryName(self, directory):
        short_name = textwrap.shorten(self.name, config.NAME_MAX_LENGTH, placeholder='...')
        directory_for_title = directory / short_name
        return directory_for_title

    @property
    def chapters(self):
        return self.__chapters

    def __repr__(self) -> str:
        return f'{self.id}'
