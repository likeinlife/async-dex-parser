from typing import Any

from .base import DexApiInterface


class TitleGetInfoAPI(DexApiInterface):
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
    def _validateRequest() -> bool:
        # TODO: make validation to title info
        raise NotImplementedError


class TitleGetChaptersAPI(DexApiInterface):
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
        return (f'https://api.mangadex.org/manga/{parameters["id"]}'
                f'/feed?limit={parameters["limit"]}&includes[]=scanlation_group&includes[]=user&order[volume]=desc&'
                f'order[chapter]=desc&offset={parameters["offset"]}&contentRating[]=safe&contentRating[]=suggestive&'
                f'contentRating[]=erotica&contentRating[]=pornographic')

    @staticmethod
    def _validateRequest() -> bool:
        # TODO: make validation to title get chapters
        raise NotImplementedError


class TitleGetByNameAPI(DexApiInterface):
    """Get title by name"""

    def sendRequest(self, **kwargs) -> Any:
        """Parameters: 
            name(str)
        """
        return super().sendRequest(**kwargs)

    @staticmethod
    def _formRequest(parameters: dict[str, Any]) -> Any:
        return (f'https://api.mangadex.org/manga?title={parameters["name"]}&limit=10&contentRating[]=safe&'
                f'contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc')

    @staticmethod
    def _validateRequest() -> bool:
        # TODO: make validation to title name finding
        raise NotImplementedError