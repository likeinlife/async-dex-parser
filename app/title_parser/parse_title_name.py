import ssl
import urllib.request
import jmespath  # type: ignore
import json

from app import headers


class ParseTitleName:

    def __init__(self, name: str) -> None:
        self._total = 0
        self.titles = self.__getTitles(name)
        self.__checkTotal()

    def __checkTotal(self):
        if self._total > 10:
            exit('Total number of titles is too much. Try more specific name')

    def __getTitles(self, name: str, offset: int = 0) -> list[dict[str, str]]:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        name = name.replace(' ', '%20')

        req = urllib.request.Request(
            f'https://api.mangadex.org/manga?title={name}&limit=5&contentRating[]=safe&'
            f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc')
        for key, value in headers.title_headers.items():
            req.add_header(key, value)

        json_response = json.load(urllib.request.urlopen(req, context=ctx))

        content = jmespath.search('data[].{id:id, title: attributes.title.* | [0]}', json_response)
        total, limit = json_response.get('total'), json_response.get('limit')
        self._total = total

        if total > limit and offset + limit < total:
            content.extend(self.__getTitles(name, offset + limit))

        return content


    def __len__(self):
        return len(self.titles)


