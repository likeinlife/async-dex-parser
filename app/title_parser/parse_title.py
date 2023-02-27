import json
import ssl
import textwrap
import urllib.request
from pathlib import Path
from typing import NamedTuple

import jmespath  # type: ignore

from ..chapter_parser import ImageDownloader, get_chapter
from ..headers import parse_title_headers


class Chapter(NamedTuple):
    id: str
    chapter: str
    lang: str
    pages: int


class ParseTitleName:

    def __init__(self, name: str) -> None:
        self._total = 0
        self.titles = self.getTitles(name)
        self.checkTotal()

    def checkTotal(self):
        if self._total > 10:
            exit('Total number of titles is too much. Try more specific name')

    def getTitles(self, name: str, offset: int = 0) -> list[dict[str, str]]:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        name = name.replace(' ', '%20')

        req = urllib.request.Request(
            f'https://api.mangadex.org/manga?title={name}&limit=5&contentRating[]=safe&'
            f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc')
        for key, value in parse_title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id:id, title: attributes.title.* | [0]}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')
        self._total = total

        if total > limit and offset + limit < total:
            content.extend(self.getTitles(name, offset + limit))

        return content


class ParseTitle:

    def __init__(self, title_id) -> None:
        self.id = title_id
        self.title_name: str = self.__getTitleName()
        self.__chapters: list[Chapter] = self.__parseJson(self.getJsonWithChapters())

    def __getTitleName(self) -> str:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(f'https://api.mangadex.org/manga/{self.id}')
        for key, value in parse_title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        name = jmespath.search('data.attributes.title.* | [0]', json_response)

        return name

    def getJsonWithChapters(self, offset: int = 0):

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(f'https://api.mangadex.org/manga/{self.id}'\
            f'/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'\
            f'order[chapter]=desc&offset={offset}&contentRating[]=safe&contentRating[]=suggestive&'\
            f'contentRating[]=erotica&contentRating[]=pornographic')
        for key, value in parse_title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.getJsonWithChapters(offset + limit))

        return content

    @staticmethod
    def __parseJson(json_response: dict) -> list[Chapter]:
        chapters_data = jmespath.search(
            '[*].{id: id, chapter: attrs.chapter, lang: attrs.translatedLanguage, pages: attrs.pages}', json_response)

        def __make_chapter(chapter_info):
            return Chapter(**chapter_info)

        chapters_list = list(map(__make_chapter, chapters_data))

        return chapters_list

    def massDownload(self, lang: str = 'en', directory: Path = Path()):
        directory_for_title = self.makeDirectoryName(directory)
        if not directory_for_title.exists():
            directory_for_title.mkdir()
        for chapter_info in self.__chapters:
            if chapter_info.lang == lang:
                chapter = get_chapter(chapter_info.id)
                ImageDownloader(chapter, directory=directory_for_title)

    def makeDirectoryName(self, directory):
        directory_for_title = directory / textwrap.shorten(self.title_name, 20)
        return directory_for_title

    @property
    def chapters(self):
        return self.__chapters

    def __repr__(self) -> str:
        return f'{self.id}'
