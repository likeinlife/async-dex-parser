import asyncio
import textwrap
from pathlib import Path
from typing import NamedTuple

import aiohttp
import jmespath  # type: ignore

from dex_parser import common, headers
from dex_parser.logger_setup import get_logger

from .image_downloader import ImageDownloader

logger = get_logger(__name__)


class Chapter(NamedTuple):
    id: str
    manga_name: str
    chapter_number: str
    chapter_name: str
    language: str
    pages_number: int


class ParseChapter:
    """Parses dex chapter via id"""

    def __init__(self, chapter_id: str):
        logger.debug(f'Parsing {chapter_id=}')
        self._chapter_id: str = chapter_id
        self.chapter_info, self.pages_urls = asyncio.run(self.__collectInfo())

    def downloadChapter(self, directory: Path = Path(), folder_name: str = ""):
        logger.info(f'Download chapter {self.chapter_info}')
        ImageDownloader(self, directory, folder_name)

    async def __collectInfo(self) -> tuple[Chapter, list]:
        logger.debug('Collecting info about chapter')
        tasks = await asyncio.gather(self.__getChapter(), self.__getPages())
        return tasks

    async def __getPages(self) -> list:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False),
                                         headers=headers.parse_chapter_headers) as session:
            try:
                response = await session.get(f'https://api.mangadex.org/at-home/server/{self._chapter_id}')
                json_response = await response.json()
                image_names = jmespath.search("chapter.data[*]", json_response)
                base_url = json_response['baseUrl']
                ch_hash = json_response['chapter']['hash']
                image_urls = list(map(lambda x: self.__makeURLFromImageName(base_url, ch_hash, x), image_names))

                logger.debug('Got chapter pages')
                return image_urls
            except KeyError:
                raise KeyError('There is no baseUrl key in json response. Maybe you accidently typed title_id?')
            except Exception as e:
                raise Exception(f'{e}. Something went wrong')

    def __makeURLFromImageName(self, base_url: str, ch_hash: str, image_name: str) -> str:
        return f'{base_url}/data/{ch_hash}/{image_name}'

    async def __getChapter(self) -> Chapter:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            response = await session.get(
                f'https://api.mangadex.org/chapter/{self._chapter_id}'\
                f'?includes/[]=scanlation_group&includes[]=manga&includes[]=user',
                params=headers.parse_chapter_params,
                headers=headers.parse_chapter_headers)
        json_response = await response.json()

        parsed_json = jmespath.search("data.attributes.[chapter, title, translatedLanguage, pages]", json_response)
        title_name = jmespath.search("data.relationships[?type=='manga'].attributes.title.* | [0] | [0]", json_response)

        logger.debug('Got chapter info')
        return Chapter(self._chapter_id, title_name, *parsed_json)

    def __repr__(self) -> str:
        headers = ('manga name', 'chapter name', 'id', 'pages')
        manga_name = textwrap.shorten(self.chapter_info.manga_name, 30)
        if self.chapter_info.chapter_name:
            chapter_name = textwrap.shorten(self.chapter_info.chapter_name, 30)
        else:
            chapter_name = ""

        content = ((manga_name, chapter_name, self.chapter_info.id, self.chapter_info.pages_number),)
        table = common.basic_table(content, headers)
        return table
