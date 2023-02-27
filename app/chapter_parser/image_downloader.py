import asyncio
import re
from pathlib import Path
from typing import TYPE_CHECKING
import aiohttp
import aiofiles  # type: ignore
import tqdm.asyncio  # type: ignore
import time

from app.config import config

if TYPE_CHECKING:
    from .parse_chapter import ParseChapter


class ImageDownloader:

    def __init__(self, chapter: "ParseChapter", directory: Path = Path(), folder_name: str = "") -> None:
        if folder_name:
            self.__path_to_dir = directory / folder_name
        else:
            if title := chapter.chapter_info.name:
                folder_name = f'{chapter.chapter_info.chapter_number} - {self.__cleanName(title)}'
            else:
                folder_name = f'{chapter.chapter_info.chapter_number}'
            self.__path_to_dir = directory / folder_name

        self.chapter = chapter
        self.__makeDir()
        self.__override = False

        asyncio.run(self.__downloadAllImages())

    @staticmethod
    def __cleanName(name: str):
        return re.sub(r'[;<>|/\:"?]', '', name)

    def __makeDir(self):
        if not self.__path_to_dir.exists():
            self.__path_to_dir.mkdir()

    def __checkOverride(self, file: Path):
        """Checks if already exists"""
        if self.__override:
            return
        table = {'y': True, 'n': False}
        if file.exists():
            override = input('Файл уже существует. Перезаписать? y/n ')
            if table.get(override):
                self.__override = True
                return
            exit('Отменено.')

    @staticmethod
    async def __getImage(session: aiohttp.ClientSession, image_url: str):
        async with session.get(image_url) as response:
            content = await response.read()
            return content

    async def __saveImage(self, content: bytes, path_to_file: Path):
        async with aiofiles.open(path_to_file, 'wb') as file_obj:
            await file_obj.write(content)

    async def __downloadImage(self, semaphore: asyncio.Semaphore, image_url: str, page_number: int):
        async with semaphore:
            this_try = 0
            file_name = str(page_number).rjust(3, "0") + '.png'
            path_to_file = self.__path_to_dir / file_name
            self.__checkOverride(path_to_file)
            while True:
                try:
                    async with aiohttp.ClientSession() as session:
                        content = await self.__getImage(session, image_url)
                        break
                except aiohttp.ServerDisconnectedError:
                    print('Sever disconnected. Continue in 5 sec...')
                    this_try += 1
                    time.sleep(config.SLEEP_BEFORE_RECONNECTION)
                    if this_try >= config.TRIES_NUMBER:
                        raise aiohttp.ServerConnectionError(
                            'Server is dead. Try discrease semaphore in config and get a chance in a few minutes')
        await self.__saveImage(content, path_to_file)

    async def __downloadAllImages(self) -> None:
        semaphore = asyncio.Semaphore(config.SEMAPHORE)
        tasks = [
            asyncio.create_task(self.__downloadImage(semaphore, image_url, number))
            for number, image_url in enumerate(self.chapter.pages_urls)
        ]
        [await f for f in tqdm.asyncio.tqdm.as_completed(tasks)]
