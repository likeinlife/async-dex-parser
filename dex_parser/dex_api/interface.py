import abc
from typing import Any

import httpx


class ApiInterface(abc.ABC):
    def __init__(
        self,
        headers: dict[str, Any],
        params: dict[str, Any] | None = None,
        proxies: Any | None = None,
        timeout: httpx.Timeout | None = None,
    ) -> None:
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.timeout = timeout

    def send_request(self, **kwargs) -> Any:
        """Make request

        Returns:
            Any: json
        """
        url = self._form_request(kwargs)
        json_response = httpx.get(
            url,
            headers=self.headers,
            params=self.params,
            proxies=self.proxies,
            verify=False,
            timeout=self.timeout,
        ).json()
        self._validate_response(json_response)
        return json_response

    @staticmethod
    @abc.abstractmethod
    def _validate_response(json_response: dict[str, Any]) -> bool:
        """Validate json

        Returns:
            bool: True if ok else Error
        """

    @staticmethod
    @abc.abstractmethod
    def _form_request(parameters: dict[str, Any]) -> str:
        """Make url to request

        Returns:
            str: URL
        """
