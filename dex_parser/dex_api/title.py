from typing import Any

from dex_parser import errors

from .base import ApiInterface


class TitleGetInfoAPI(ApiInterface):
	"""Get title info"""

	def sendRequest(self, **kwargs) -> Any:
		"""Parameters:
		id(UUID)
		"""
		return super().sendRequest(**kwargs)

	@staticmethod
	def _formRequest(parameters: dict[str, Any]) -> str:
		return f'https://api.mangadex.org/manga/{parameters["id"]}'

	@staticmethod
	def _validateResponse(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleInfoError('Most likely an incorrect id')


class TitleGetChaptersAPI(ApiInterface):
	"""Get chapters from title"""

	def sendRequest(self, **kwargs) -> Any:
		"""Parameters:
		id(UUID)
		offset(int)
		limit(int)

		Restrictions:
		    limit must be <= 500
		"""
		return super().sendRequest(**kwargs)

	@staticmethod
	def _formRequest(parameters: dict[str, Any]) -> str:
		return (
			f'https://api.mangadex.org/manga/{parameters["id"]}'
			f'/feed?limit={parameters["limit"]}&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'
			f'order[chapter]=desc&offset={parameters["offset"]}&contentRating[]=safe&contentRating[]=suggestive&'
			f'contentRating[]=erotica&contentRating[]=pornographic'
		)

	@staticmethod
	def _validateResponse(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleGetChaptersError('Most likely an incorrect id')


class TitleGetByNameAPI(ApiInterface):
	"""Get title by name"""

	def sendRequest(self, **kwargs) -> Any:
		"""Parameters:
		name(str)
		"""
		return super().sendRequest(**kwargs)

	@staticmethod
	def _formRequest(parameters: dict[str, Any]) -> Any:
		return (
			f'https://api.mangadex.org/manga?title={parameters["name"]}&limit=10&contentRating[]=safe&'
			f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc'
		)

	@staticmethod
	def _validateResponse(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleGetByNameError('Most likely an incorrect id')
