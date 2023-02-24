from typing import NamedTuple
import requests  # type: ignore
import re

from headers import parse_title_headers
import jmespath  # type: ignore


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


class ParseTitle:
    """
    Парсит айди или url тайтла на дексе. С доступа к спарсенных главам используется chapters
    """

    def __init__(self, title_id):
        self.__id = title_id
        self.__json = self.getJsonWithChapters(self.__id)
        self.__chapters: list[Chapter] = self.parseJson(self.__json)

    def getJsonWithChapters(self, title_id: str, offset: int = 0):
        json_response = requests.get(
            f'https://api.mangadex.org/manga/{title_id}'\
            f'/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'\
            f'order[chapter]=desc&offset={offset}&contentRating[]=safe&contentRating[]=suggestive&'\
            f'contentRating[]=erotica&contentRating[]=pornographic',
            headers=parse_title_headers).json()

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


if __name__ == '__main__':
    a = get_title(
        'https://mangadex.org/title/edb82d3c-20f6-4cf9-a879-7457478642fe/my-lovey-dovey-wife-is-a-stone-cold-killer')

    b = get_title('edb82d3c-20f6-4cf9-a879-7457478642fe')
    print(a.chapters)
    print(b.chapters)
