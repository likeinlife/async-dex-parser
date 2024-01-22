import textwrap
from pathlib import Path
from typing import Any

import jmespath  # type: ignore

from dex_parser import dex_api, headers
from dex_parser.chapter_parser import get_chapter_parser
from dex_parser.common import get_clean_path
from dex_parser.config import config
from dex_parser.logger_setup import get_logger

from .chapter_selector import get_chapter_selector
from .models import TitleChapter

logger = get_logger(__name__)


class TitleParser:
    def __init__(self, title_id: str, language: str = 'en') -> None:
        self.id = title_id
        self.language = language
        self.name: str = self._get_title_name()
        self.chapters = self._parse_json(self._get_json())
        self._filter_chapters()

    def download(
        self,
        chapter_select_string: str,
        directory: Path | None = None,
        disable_creating_title_dir: bool = False,
    ):
        """
        Download chapters range.

        Args:
            chapter_range: `10-24, 12, ~13`
        """
        logger.info(f'Downloading chapters range {chapter_select_string} from {self.name}')

        selected_chapters = get_chapter_selector(chapter_select_string)
        directory_for_title = self._create_dir(directory, disable_creating_title_dir)
        for chapter_info in self.chapters:
            if chapter_info.chapter in selected_chapters:
                chapter = get_chapter_parser(chapter_info.id)
                chapter.download_chapter(directory=directory_for_title)

    def _filter_chapters(self):
        if self.language == 'any':
            return
        self.chapters = list(filter(lambda chapter: chapter.language == self.language, self.chapters))

    def _get_title_name(self) -> str:
        """Get manga name."""
        json_response = dex_api.title.TitleGetInfoAPI(
            headers=headers.title_headers,
            timeout=config.TIMEOUT,
        ).send_request(id=self.id)

        name = jmespath.search('data.attributes.title.* | [0]', json_response)
        logger.debug(f'Got name from {self.id}, {name}')

        return name

    def _get_json(self, offset: int = 0):
        json_response = dex_api.title.TitleGetChaptersAPI(
            headers=headers.title_headers,
            timeout=config.TIMEOUT,
        ).send_request(
            id=self.id,
            offset=offset,
            limit=500,
        )

        content = jmespath.search('data[].{id: id, attrs: attributes}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')

        if total > limit and offset + limit < total:
            content.extend(self._get_json(offset + limit))

        logger.debug(f'Got chapters from {self.id=}')

        return content

    @staticmethod
    def _parse_json(json_response: dict[str, Any]) -> list[TitleChapter]:
        chapters_data = jmespath.search(
            '[*].[id, attrs.chapter, attrs.translatedLanguage, attrs.pages]',
            json_response,
        )

        def __make_chapter(chapter_info) -> TitleChapter:
            return TitleChapter(*chapter_info)

        chapters_list = list(map(__make_chapter, chapters_data))

        return chapters_list

    def _create_dir(self, directory: Path | None, disable_creating_title_dir: bool = False) -> Path:
        directory_for_title = directory or Path()
        if not disable_creating_title_dir:
            clean_title_name = get_clean_path(self.name)
            short_name = textwrap.shorten(clean_title_name, config.NAME_MAX_LENGTH, placeholder='')
            directory_for_title = directory_for_title / short_name
        directory_for_title.mkdir(exist_ok=True, parents=True)
        logger.info(f'Directory for save: {directory_for_title}')
        return directory_for_title

    def __repr__(self) -> str:
        return f'{self.id}'
