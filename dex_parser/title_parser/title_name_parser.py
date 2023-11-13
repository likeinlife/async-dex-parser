import jmespath  # type: ignore

from dex_parser import dex_api, headers
from dex_parser.config import config
from dex_parser.logger_setup import get_logger

logger = get_logger(__name__)


class TitleNameParser:
	def __init__(self, name: str) -> None:
		self.name = name
		self._total = 0
		self.titles = self.__getTitles(name)

	def __getTitles(self, name: str) -> list[dict[str, str]]:
		name = name.replace(' ', '%20')

		json_response = dex_api.title.TitleGetByNameAPI(
			headers=headers.title_headers,
			timeout=config.TIMEOUT,
		).sendRequest(name=name)

		content = jmespath.search('data[].{id:id, title: attributes.title.* | [0]}', json_response)
		logger.debug(f'Got info by {self.name=}: {content}')

		return content

	def __len__(self):
		return len(self.titles)

	def __getitem__(self, key):
		logger.debug(f'Getting item by {key=}')
		return self.titles[key]
