import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles  # type: ignore
import httpx
import tqdm.asyncio  # type: ignore

from dex_parser import common, headers
from dex_parser.config import config
from dex_parser.logger_setup import get_logger
from dex_parser.common import clean_name

if TYPE_CHECKING:
    from .parse_chapter import ParseChapter

logger = get_logger(__name__)


class ImageDownloader:

    def __init__(self, chapter: "ParseChapter", directory: Path = Path(), folder_name: str = "") -> None:

        self.chapter = chapter
        self.__path_to_dir = self.__makePath(directory, folder_name)
        self.__makeDir()
        self.__override_dir: tuple[bool, Path | None] = (False, None)

        asyncio.run(self.__downloadAllImages())

    def __makePath(self, directory: Path, folder_name: str):
        logger.debug(f'Making path of `{directory=}` and `{folder_name=}`')
        if not folder_name:
            if title := self.chapter.chapter_info.chapter_name:
                folder_name = f'{self.chapter.chapter_info.chapter_number} - {clean_name(title)}'
            else:
                folder_name = f'{self.chapter.chapter_info.chapter_number}'
        return directory / folder_name

    def __makeDir(self):
        if not self.__path_to_dir.exists():
            self.__path_to_dir.mkdir()

    def __checkOverride(self, path_to_object: Path):
        """Checks if files inside directory already exists"""
        folder = path_to_object.parent
        if (True, folder) == self.__override_dir:
            return True
        if (False, folder) == self.__override_dir:
            return False
        if path_to_object.exists():
            override = input(f'`{folder}` already exists. Override? y/n ')
            if common.true_table.get(override):
                self.__override_dir = (True, folder)
                return True
            else:
                self.__override_dir = (False, folder)
                return False
        self.__override_dir = (True, folder)
        return True

    @staticmethod
    async def __getImage(session: httpx.AsyncClient, image_url: str):
        """Download image from internet"""
        response = await session.get(image_url)
        logger.debug(f'Get image from internet `{image_url}`')
        content = response.read()
        return content

    @staticmethod
    async def __saveImage(content: bytes, path_to_file: Path):
        """Save image in local storage"""
        async with aiofiles.open(path_to_file, 'wb') as file_obj:
            logger.debug(f'Saving image to `{path_to_file}`')
            await file_obj.write(content)

    async def __downloadImage(self, semaphore: asyncio.Semaphore, image_url: str, page_number: int):
        """Download image from internet, then save it in local storage"""
        async with semaphore:
            logger.debug(f'Downloading image {page_number} from `{image_url}`')
            file_name = str(page_number).rjust(3, "0") + '.png'
            path_to_file = self.__path_to_dir / file_name
            if self.__checkOverride(path_to_file):
                async with httpx.AsyncClient(
                        headers=headers.get_image_headers,
                        verify=False,
                        timeout=config.TIMEOUT,
                ) as session:
                    content = await self.__getImage(session, image_url)
                await self.__saveImage(content, path_to_file)

    async def __downloadAllImages(self) -> None:
        logger.info(f'Downloading all image from title {self.chapter.chapter_info.manga_name}')
        semaphore = asyncio.Semaphore(config.THREADS)
        tasks = [
            asyncio.create_task(self.__downloadImage(semaphore, image_url, number))
            for number, image_url in enumerate(self.chapter.pages_urls)
        ]
        [await f for f in tqdm.asyncio.tqdm.as_completed(tasks)]
