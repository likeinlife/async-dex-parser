import json
import ssl
import urllib.request

import jmespath  # type: ignore

from app import headers
from app.config import config
from app.logger_setup import get_logger
import http.client
import time

logger = get_logger(__name__)


class ParseTitleName:

    def __init__(self, name: str) -> None:
        self.name = name
        self._total = 0
        self.titles = self.__getTitles(name)

    def __getTitles(self, name: str) -> list[dict[str, str]]:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        name = name.replace(' ', '%20')

        req = urllib.request.Request(
            f'https://api.mangadex.org/manga?title={name}&limit=10&contentRating[]=safe&'
            f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc')
        for key, value in headers.title_headers.items():
            req.add_header(key, value)

        current_reconnect = 0
        while True:
            try:
                json_response = json.load(urllib.request.urlopen(req, context=ctx))
                break
            except http.client.IncompleteRead as e:
                print(f'Sever disconnected. Continue in {config.SLEEP_BEFORE_RECONNECTION} sec...')
                current_reconnect += 1
                time.sleep(config.SLEEP_BEFORE_RECONNECTION)
                if current_reconnect >= config.TRIES_NUMBER:
                    logger.error(e)
                    exit('Server disconnected')

        content = jmespath.search('data[].{id:id, title: attributes.title.* | [0]}', json_response)
        logger.debug(f'Got info by {self.name=}: {self.titles}')

        return content

    def __len__(self):
        return len(self.titles)

    def __getitem__(self, key):
        logger.debug(f'Getting item by {key=}')
        return self.titles[key]
