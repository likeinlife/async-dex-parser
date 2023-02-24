import asyncio
from asyncio.windows_events import ERROR_CONNECTION_ABORTED
from pathlib import Path
import re
from typing import NamedTuple
import aiofiles  # type: ignore

import aiohttp
import jmespath  # type: ignore

import headers
from config import config
import sys

__all__ = ['get_chapter', 'ImageDownloader']


def get_chapter(chapter_id: str | list[str]):
    if isinstance(chapter_id, str):
        return SingleParser(chapter_id)
    elif isinstance(chapter_id, list):
        return MassParser(chapter_id)
    else:
        raise Exception('chapter_id not a list[str] or str')


class Chapter(NamedTuple):
    id: str
    chapter_number: str
    title: str
    lan: str
    pages: int


class SingleParser:
    """Parses dex chapter via id or url"""

    def __init__(self, chapter_id: str):
        self._chapter_id: str = chapter_id
        self.chapter_info, self.pages_urls = asyncio.run(self._collectInfo())

    async def _collectInfo(self) -> tuple[Chapter, list]:
        tasks = await asyncio.gather(self._getChapter(), self._getPages())
        return tasks

    @staticmethod
    def cleanURL(url: str) -> str:
        clear_id = re.search(r'chapter/([\w\W]*)/[^/]', url)
        if clear_id is None:
            raise TypeError("Не получается найти айди из URL")
        return clear_id.group(1)

    async def _getPages(self) -> list:
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(f'https://api.mangadex.org/at-home/server/{self._chapter_id}',
                                             params=headers.parse_chapter_params,
                                             headers=headers.parse_chapter_headers)
                json_response = await response.json()
                image_names = jmespath.search("chapter.data[*]", json_response)
                base_url = json_response['baseUrl']
                ch_hash = json_response['chapter']['hash']
                image_urls = list(map(lambda x: self.makeURLFromImageName(base_url, ch_hash, x), image_names))
                return image_urls
            except KeyError:
                raise KeyError('There is no baseUrl key in json response. Maybe you accidently typed title_id?')
            except Exception as e:
                raise Exception(f'{e}. Somethig went wrong')

    def makeURLFromImageName(self, base_url, ch_hash, image_name: str) -> str:
        return f'{base_url}/data/{ch_hash}/{image_name}'

    async def _getChapter(self) -> Chapter:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://api.mangadex.org/chapter/{self._chapter_id}'\
                f'?includes/[]=scanlation_group&includes[]=manga&includes[]=user',
                params=headers.parse_chapter_params,
                headers=headers.parse_chapter_headers)
        json_response = await response.json()

        parsed_json = jmespath.search("data.attributes.[chapter, title, translatedLanguage, pages]", json_response)
        return Chapter(self._chapter_id, *parsed_json)

    def __repr__(self) -> str:
        return f'Айди - {self.chapter_info.id} | Страниц - {self.chapter_info.pages}'


class MassParser(SingleParser):

    def __init__(self, chapter_id: list[str]):
        raise NotImplementedError()


class ImageDownloader:

    def __init__(self, chapter: SingleParser, directory: Path = Path(), folder_name: str = "") -> None:
        if folder_name:
            self.path_to_dir = directory / folder_name
        else:
            if title := chapter.chapter_info.title:
                folder_name = f'{chapter.chapter_info.chapter_number} - {title}'
            else:
                folder_name = f'{chapter.chapter_info.chapter_number}'
            self.path_to_dir = directory / folder_name

        self.chapter = chapter
        self.makeDir()
        self.override = False

        asyncio.run(self.downloadAllImages())

    def makeDir(self):
        if not self.path_to_dir.exists():
            self.path_to_dir.mkdir()

    def checkOverride(self, file: Path):
        """Checks if already exists"""
        if self.override:
            return
        table = {'y': True, 'n': False}
        if file.exists():
            override = input('Файл уже существует. Перезаписать? y/n ')
            if table.get(override):
                return
            exit('Отменено.')

    @staticmethod
    async def getImage(session: aiohttp.ClientSession, image_url: str):
        async with session.get(image_url) as response:
            content = await response.read()
            return content

    async def saveImage(self, content: bytes, path_to_file: Path):
        async with aiofiles.open(path_to_file, 'wb') as file_obj:
            await file_obj.write(content)

    async def downloadImage(self, semaphore: asyncio.Semaphore, session: aiohttp.ClientSession, image_url: str,
                            page_number: int):
        await semaphore.acquire()
        file_name = str(page_number).rjust(3, "0") + '.png'
        path_to_file = self.path_to_dir / file_name
        self.checkOverride(path_to_file)
        content = await self.getImage(session, image_url)
        semaphore.release()
        await self.saveImage(content, path_to_file)
        print(f'Downloaded p{page_number}')

    async def downloadAllImages(self) -> None:
        semaphore = asyncio.Semaphore(config.SEMAPHORE)
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(self.downloadImage(semaphore, session, image_url, number))
                for number, image_url in enumerate(self.chapter.pages_urls)
            ]
            await asyncio.wait(tasks)
