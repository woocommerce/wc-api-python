# -*- coding: utf-8 -*-

"""
WC API Class
"""

__title__ = "wc-api"
__version__ = "1.2.0"
__author__ = "Claudio Sanches @ WooThemes"
__license__ = "MIT"

from json import dumps as jsonencode
from wc.oauth import OAuth
import aiohttp


class API(object):
    """ API Class """

    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = kwargs.get("wp_api", False)
        self.version = kwargs.get("version", "v3")
        self.is_ssl = self.__is_ssl()
        self.timeout = kwargs.get("timeout", 5)
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.query_string_auth = kwargs.get("query_string_auth", False)

    def __is_ssl(self):
        """ Check if url use HTTPS """
        return self.url.startswith("https")

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = "%s/" % url

        if self.wp_api:
            api = "wp-json"

        return "%s%s/%s/%s" % (url, api, self.version, endpoint)

    def __get_oauth_url(self, url, method):
        """ Generate oAuth1.0a URL """
        oauth = OAuth(
            url=url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            version=self.version,
            method=method
        )

        return oauth.get_oauth_url()

    async def __request(self, method, endpoint, data):
        """ Do requests """
        url = self.__get_url(endpoint)
        auth = None
        params = {}
        headers = {
            "user-agent": "WooCommerce API Client-Python/%s" % __version__,
            "content-type": "application/json;charset=utf-8",
            "accept": "application/json"
        }

        if self.is_ssl is True and self.query_string_auth is False:
            auth = aiohttp.BasicAuth(self.consumer_key, self.consumer_secret)
        elif self.is_ssl is True and self.query_string_auth is True:
            params = {
                "consumer_key": self.consumer_key,
                "consumer_secret": self.consumer_secret
            }
        else:
            url = self.__get_oauth_url(url, method)

        if data is not None:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')

        return await aiohttp.request(
            method=method,
            url=url,
            #verify=self.verify_ssl,
            auth=auth,
            params=params,
            data=data,
            #timeout=self.timeout,
            headers=headers
        )

    async def get(self, endpoint):
        """ Get requests """
        return await self.__request("GET", endpoint, None)

    async def post(self, endpoint, data):
        """ POST requests """
        return await self.__request("POST", endpoint, data)

    async def put(self, endpoint, data):
        """ PUT requests """
        return await self.__request("PUT", endpoint, data)

    async def delete(self, endpoint):
        """ DELETE requests """
        return await self.__request("DELETE", endpoint, None)

    async def options(self, endpoint):
        """ OPTIONS requests """
        return await self.__request("OPTIONS", endpoint, None)
