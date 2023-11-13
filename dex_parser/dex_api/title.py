from typing import Any

from dex_parser import errors

from .base import ApiInterface


class TitleGetInfoAPI(ApiInterface):
	"""Get title info"""

	def send_request(self, **kwargs) -> Any:
		"""Parameters:
		id(UUID)
		"""
		return super().send_request(**kwargs)

	@staticmethod
	def _form_request(parameters: dict[str, Any]) -> str:
		return f'https://api.mangadex.org/manga/{parameters["id"]}'

	@staticmethod
	def _validate_response(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleInfoError('Most likely an incorrect id')


class TitleGetChaptersAPI(ApiInterface):
	"""Get chapters from title"""

	def send_request(self, **kwargs) -> Any:
		"""Parameters:
		id(UUID)
		offset(int)
		limit(int)

		Restrictions:
		    limit must be <= 500
		"""
		return super().send_request(**kwargs)

	@staticmethod
	def _form_request(parameters: dict[str, Any]) -> str:
		return (
			f'https://api.mangadex.org/manga/{parameters["id"]}'
			f'/feed?limit={parameters["limit"]}&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'
			f'order[chapter]=desc&offset={parameters["offset"]}&contentRating[]=safe&contentRating[]=suggestive&'
			f'contentRating[]=erotica&contentRating[]=pornographic'
		)

	@staticmethod
	def _validate_response(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleGetChaptersError('Most likely an incorrect id')


class TitleGetByNameAPI(ApiInterface):
	"""Get title by name"""

	def send_request(self, **kwargs) -> Any:
		"""Parameters:
		name(str)
		"""
		return super().send_request(**kwargs)

	@staticmethod
	def _form_request(parameters: dict[str, Any]) -> Any:
		return (
			f'https://api.mangadex.org/manga?title={parameters["name"]}&limit=10&contentRating[]=safe&'
			f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc'
		)

	@staticmethod
	def _validate_response(json_response: dict[str, Any]) -> bool:
		if json_response['result'] == 'ok':
			return True
		raise errors.ParseTitleGetByNameError('Most likely an incorrect id')
