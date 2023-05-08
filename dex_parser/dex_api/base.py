import abc
from typing import Any

import httpx


class DexApiInterface(abc.ABC):

    def __init__(self,
                 headers: dict,
                 params: dict | None = None,
                 proxies: Any | None = None,
                 timeout: httpx.Timeout | None = None) -> None:
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.timeout = timeout

    def sendRequest(self, **kwargs) -> Any:
        """Make request

        Returns:
            Any: json
        """
        url = self._formRequest(kwargs)
        return httpx.get(
            url,
            headers=self.headers,
            params=self.params,
            proxies=self.proxies,
            verify=False,
            timeout=self.timeout,
        ).json()

    @staticmethod
    @abc.abstractmethod
    def _formRequest(parameters: dict[str, Any]) -> str:
        """Make url to request

        Returns:
            str: URL
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def _validateRequest() -> bool:
        """Validate json

        Returns:
            bool: True if ok else Error
        """
        ...
