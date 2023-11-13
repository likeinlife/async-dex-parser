from typing import Any

from dex_parser import errors

from .base import DexApiInterface


class ChapterGetInfoAPI(DexApiInterface):
    """Get chapter info"""

    def sendRequest(self, **kwargs) -> Any:
        """Parameters: id(UUID)"""
        return super().sendRequest(**kwargs)

    @staticmethod
    def _formRequest(parameters: dict[str, Any]) -> str:
        return (f'https://api.mangadex.org/chapter/{parameters["id"]}?includes[]=manga')

    @staticmethod
    def _validateResponse(json_response: dict) -> bool:
        if json_response['result'] == 'ok':
            return True
        raise errors.ParseChapterInfoError('Most likely an incorrect id')


class ChapterGetPagesAPI(DexApiInterface):
    """Get chapter pages"""

    def sendRequest(self, **kwargs) -> Any:
        """Parameters: id(UUID)"""
        return super().sendRequest(**kwargs)

    @staticmethod
    def _formRequest(parameters: dict[str, Any]) -> str:
        return f'https://api.mangadex.org/at-home/server/{parameters["id"]}'

    @staticmethod
    def _validateResponse(json_response: dict) -> bool:
        if json_response['result'] == 'ok':
            return True
        raise errors.ParseChapterPagesError('Most likely an incorrect id')