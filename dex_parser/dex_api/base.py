from typing import Any

import httpx

from .interface import ApiInterface


class BaseApi(ApiInterface):
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
