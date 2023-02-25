import json
import ssl
import re
import urllib.request
from typing import NamedTuple

import jmespath  # type: ignore

from headers import parse_title_headers


class Chapter(NamedTuple):
    id: str
    chapter: str
    lang: str
    pages: int


def get_title(url_or_id: str):

    def __get_id_from_url(url: str) -> str | bool:
        clear_id = re.match(r'https://mangadex.org/title/([\w\W]*)/[\w\W]*', url)
        if clear_id is None:
            return False
        return clear_id.group(1)

    if title_id := __get_id_from_url(url_or_id):
        return ParseTitle(title_id)
    elif re.match(r'[a-zA-Z0-90]', url_or_id):
        return ParseTitle(url_or_id)
    else:
        raise Exception('Incorrect entry value')


class ParseTitleName:

    def __init__(self, name: str) -> None:
        self._chapter_ids = self.getJsonWithTitles(name)

    def getJsonWithTitles(self, name: str, offset: int = 0):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f'https://api.mangadex.org/manga?title={name}&limit=5&contentRating[]=safe&'
            f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc')
        for key, value in parse_title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id:id, title: attributes.title.en}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.getJsonWithTitles(name, offset + limit))

        return content


class ParseTitle:

    def __init__(self, title_id) -> None:
        self.__id = title_id
        self.__json = self.getJsonWithChapters(self.__id)
        self.__chapters: list[Chapter] = self.parseJson(self.__json)

    def getJsonWithChapters(self, title_id: str, offset: int = 0):

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(f'https://api.mangadex.org/manga/{title_id}'\
            f'/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'\
            f'order[chapter]=desc&offset={offset}&contentRating[]=safe&contentRating[]=suggestive&'\
            f'contentRating[]=erotica&contentRating[]=pornographic')
        for key, value in parse_title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self.getJsonWithChapters(self.__id, offset + limit))

        return content

    @staticmethod
    def parseJson(json_response: dict) -> list[Chapter]:
        chapters_data = jmespath.search(
            '[*].{id: id, chapter: attrs.chapter, lang: attrs.translatedLanguage, pages: attrs.pages}', json_response)

        def __make_chapter(chapter_info):
            return Chapter(**chapter_info)

        chapters_list = list(map(__make_chapter, chapters_data))

        return chapters_list

    @property
    def chapters(self):
        return self.__chapters

    def __repr__(self) -> str:
        return f'{self.__id}'
