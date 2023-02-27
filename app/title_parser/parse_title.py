import json
import ssl
import textwrap
import urllib.request
from pathlib import Path
from typing import NamedTuple

import jmespath  # type: ignore

from ..chapter_parser import get_chapter
from ..headers import title_headers


class Chapter(NamedTuple):
    id: str
    chapter: str
    language: str
    pages: int


class ParseTitle:

    def __init__(self, title_id: str) -> None:
        self.id = title_id
        self.title_name: str = self.__getTitleName()
        self.__chapters: list[Chapter] = self.__parseJson(self.__getJsonWithChapters())

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

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

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

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.__getJsonWithChapters(offset + limit))

        return content

    @staticmethod
    def __parseJson(json_response: dict) -> list[Chapter]:
        chapters_data = jmespath.search('[*].[id, attrs.chapter, attrs.translatedLanguage, attrs.pages]', json_response)

        def __make_chapter(chapter_info):
            return Chapter(*chapter_info)

        chapters_list = list(map(__make_chapter, chapters_data))

        return chapters_list

    def __makeDirectoryName(self, directory):
        directory_for_title = directory / textwrap.shorten(self.title_name, 20)
        return directory_for_title

    @property
    def chapters(self):
        return self.__chapters

    def __repr__(self) -> str:
        return f'{self.id}'
