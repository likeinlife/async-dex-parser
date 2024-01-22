import textwrap
from pathlib import Path

import jmespath  # type: ignore

from dex_parser import common, dex_api, headers
from dex_parser.config import config
from dex_parser.downloader import ImageDownloader
from dex_parser.logger_setup import get_logger

from .models import Chapter

logger = get_logger(__name__)


class ParseChapter:
    """Parse mangadex chapter via id."""

    def __init__(self, chapter_id: str):
        logger.debug(f'Parsing {chapter_id=}')
        self._chapter_id: str = chapter_id
        self.chapter_info, self.pages_urls = self._get_chapter_info(), self._get_pages_urls()

    def download_chapter(self, directory: Path = Path(), folder_name: str = ''):
        logger.info(f'Download chapter {self.chapter_info}')
        downloader = ImageDownloader(self, directory, folder_name)
        downloader.run()

    def _get_pages_urls(self) -> list[str]:
        json_response = dex_api.chapter.ChapterGetPagesAPI(
            headers=headers.parse_chapter_headers,
            timeout=config.TIMEOUT,
        ).send_request(id=self._chapter_id)
        image_names = jmespath.search('chapter.data[*]', json_response)
        base_url = json_response['baseUrl']
        ch_hash = json_response['chapter']['hash']
        image_urls = [
            self.__get_url_from_image_name(
                base_url,
                ch_hash,
                image_name,
            )
            for image_name in image_names
        ]

        logger.debug(f'Got chapter({self._chapter_id}) pages')
        return image_urls

    def __get_url_from_image_name(self, base_url: str, ch_hash: str, image_name: str) -> str:
        return f'{base_url}/data/{ch_hash}/{image_name}'

    def _get_chapter_info(self) -> Chapter:
        json_response = dex_api.chapter.ChapterGetInfoAPI(
            headers=headers.parse_chapter_headers,
            params=headers.parse_chapter_params,
            timeout=config.TIMEOUT,
        ).send_request(id=self._chapter_id)

        parsed_json = jmespath.search(
            'data.attributes.[chapter, title, translatedLanguage, pages]',
            json_response,
        )
        title_name = jmespath.search(
            "data.relationships[?type=='manga'].attributes.title.* | [0] | [0]",
            json_response,
        )

        logger.debug('Got chapter info')
        return Chapter(self._chapter_id, title_name, *parsed_json)

    def __str__(self) -> str:
        headers = ('manga name', 'chapter name', 'id', 'pages')
        manga_name = textwrap.shorten(self.chapter_info.manga_name, 30)
        if self.chapter_info.chapter_name:
            chapter_name = textwrap.shorten(self.chapter_info.chapter_name, 30)
        else:
            chapter_name = ''

        content = (
            (
                manga_name,
                chapter_name,
                self.chapter_info.id,
                self.chapter_info.pages_number,
            ),
        )
        table = common.basic_table(content, headers)
        return table
