import httpx

import jmespath  # type: ignore

from dex_parser import headers
from dex_parser.config import config
from dex_parser.logger_setup import get_logger
import time

logger = get_logger(__name__)


class ParseTitleName:

    def __init__(self, name: str) -> None:
        self.name = name
        self._total = 0
        self.titles = self.__getTitles(name)

    def __getTitles(self, name: str) -> list[dict[str, str]]:
        name = name.replace(' ', '%20')

        current_reconnect = 0
        while True:
            try:
                json_response = httpx.get(
                    f'https://api.mangadex.org/manga?title={name}&limit=10&contentRating[]=safe&'
                    f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc',
                    verify=False,
                    headers=headers.title_headers,
                ).json()
                break
            except httpx.TimeoutException as e:
                print(f'Sever disconnected. Continue in {config.SLEEP_BEFORE_RECONNECTION} sec...')
                current_reconnect += 1
                time.sleep(config.SLEEP_BEFORE_RECONNECTION)
                if current_reconnect >= config.TRIES_NUMBER:
                    logger.error(e)
                    exit('Server disconnected')

        content = jmespath.search('data[].{id:id, title: attributes.title.* | [0]}', json_response)
        logger.debug(f'Got info by {self.name=}: {content}')

        return content

    def __len__(self):
        return len(self.titles)

    def __getitem__(self, key):
        logger.debug(f'Getting item by {key=}')
        return self.titles[key]
