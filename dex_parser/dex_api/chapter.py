from typing import Any
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
    def _validateRequest() -> bool:
        # TODO: make validation to title info
        raise NotImplementedError


class ChapterGetPagesAPI(DexApiInterface):
    """Get chapter pages"""

    def sendRequest(self, **kwargs) -> Any:
        """Parameters: id(UUID)"""
        return super().sendRequest(**kwargs)

    @staticmethod
    def _formRequest(parameters: dict[str, Any]) -> str:
        return f'https://api.mangadex.org/at-home/server/{parameters["id"]}'

    @staticmethod
    def _validateRequest() -> bool:
        # TODO: make validation to title info
        raise NotImplementedError