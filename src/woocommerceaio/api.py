__version__ = "1.0.1"

import asyncio
import logging
from httpx import AsyncClient, Response, BasicAuth, HTTPError, TimeoutException
from json import dumps as jsonencode
from time import time
from woocommerceaio.oauth import OAuth
from urllib.parse import urlencode

import typing as t


class API(object):
    """API Class"""

    def __init__(
        self,
        url: str,
        consumer_key: str,
        consumer_secret: str,
        max_retries: int = 3,
        timeout: int = 5,
        **kwargs,
    ):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = kwargs.get("wp_api", True)
        self.version = kwargs.get("version", "wc/v3")
        self.is_ssl = self.__is_ssl()
        self.max_retries = max_retries
        self.timeout = timeout
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.query_string_auth = kwargs.get("query_string_auth", False)
        self.user_agent = kwargs.get("user_agent", f"woocommerceaio/{__version__}")

    def __is_ssl(self) -> bool:
        """Check if url use HTTPS"""
        return self.url.startswith("https")

    def __get_url(self, endpoint: str) -> str:
        """Get URL for requests"""
        url = self.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = f"{url}/"

        if self.wp_api:
            api = "wp-json"

        return f"{url}{api}/{self.version}/{endpoint}"

    def __get_oauth_url(self, url: str, method: str, **kwargs: t.Any) -> str:
        """Generate oAuth1.0a URL"""
        oauth = OAuth(
            url=url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            version=self.version,
            method=method,
            oauth_timestamp=kwargs.get("oauth_timestamp", int(time())),
        )

        return oauth.get_oauth_url()

    async def __request(
        self,
        method: str,
        endpoint: str,
        data: t.Optional[t.Any],
        params: t.Optional[t.Dict[str, t.Any]] = None,
        **kwargs: t.Any,
    ) -> Response:
        """Do requests"""
        if params is None:
            params = {}
        url = self.__get_url(endpoint)
        auth = None
        headers = {"user-agent": f"{self.user_agent}", "accept": "application/json"}

        if self.is_ssl is True and self.query_string_auth is False:
            auth = BasicAuth(self.consumer_key, self.consumer_secret)
        elif self.is_ssl is True and self.query_string_auth is True:
            params.update(
                {
                    "consumer_key": self.consumer_key,
                    "consumer_secret": self.consumer_secret,
                }
            )
        else:
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
            url = self.__get_oauth_url(url, method, **kwargs)

        if data is not None:
            data = jsonencode(data, ensure_ascii=False).encode("utf-8")
            headers["content-type"] = "application/json;charset=utf-8"

        follow_redirects: bool = False
        if "allow_redirects" in kwargs:
            follow_redirects = kwargs.pop("allow_redirects")

        async with AsyncClient(
            verify=self.verify_ssl,
            follow_redirects=follow_redirects,
            timeout=self.timeout,
            headers=headers,
            auth=auth,
        ) as client:
            backoff: float = 0.5
            _try: int = 1

            while True:
                try:
                    response: Response = await client.request(
                        method=method,
                        url=url,
                        params=params,
                        content=data,
                        **kwargs,
                    )
                    if response.status_code < 500:
                        return response
                except HTTPError as ex:
                    logging.error(
                        f"Error retrieving {self.__get_url(endpoint)}: {str((ex))}"
                    )

                if _try == self.max_retries:
                    break
                logging.error(f"Awaiting {backoff} seconds before next attempt...")
                await asyncio.sleep(backoff)
                _try += 1
                backoff *= 2

            raise TimeoutException(
                f"Max retries exceeded to {self.__get_url(endpoint)}"
            )

    async def get(self, endpoint: str, **kwargs: t.Any) -> Response:
        """Get requests"""
        return await self.__request("GET", endpoint, None, **kwargs)

    async def post(
        self, endpoint: str, data: t.Optional[t.Dict[str, t.Any]], **kwargs: t.Any
    ) -> Response:
        """POST requests"""
        return await self.__request("POST", endpoint, data, **kwargs)

    async def put(
        self, endpoint: str, data: t.Optional[t.Dict[str, t.Any]], **kwargs: t.Any
    ) -> Response:
        """PUT requests"""
        return await self.__request("PUT", endpoint, data, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Response:
        """DELETE requests"""
        return await self.__request("DELETE", endpoint, None, **kwargs)

    async def options(self, endpoint: str, **kwargs) -> Response:
        """OPTIONS requests"""
        return await self.__request("OPTIONS", endpoint, None, **kwargs)
