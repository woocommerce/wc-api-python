# -*- coding: utf-8 -*-

"""
WooCommerce API Class
"""

__title__ = "woocommerce-api"
__version__ = "3.0.0"
__author__ = "Claudio Sanches @ Automattic"
__license__ = "MIT"

from requests import request
from json import dumps as jsonencode
from time import time
from woocommerce.oauth import OAuth
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode


class API(object):
    '''
    This script defines the API class, which provides a wrapper around the requests library to interact with the WooCommerce API.

    The API class takes in three required arguments: url, consumer_key, and consumer_secret. Additionally, the class allows for the following keyword arguments:

    wp_api: a boolean indicating if the API is using the WordPress API (default is True).
    version: the API version to use (default is "wc/v3").
    timeout: the timeout for API requests in seconds (default is 5).
    verify_ssl: a boolean indicating if SSL certificates should be verified for API requests (default is True).
    query_string_auth: a boolean indicating if authentication should be passed as query parameters (default is False).
    user_agent: the user agent string to use for API requests (default is "WooCommerce-Python-REST-API/3.0.0").
    The class has six methods:

    get: sends a GET request to the API.
    post: sends a POST request to the API, with a required data argument.
    put: sends a PUT request to the API, with a required data argument.
    delete: sends a DELETE request to the API.
    options: sends an OPTIONS request to the API.
    __request: a private method that handles sending the actual API request, taking in a method argument for the HTTP method to use, and an optional params argument for any query parameters to include.
    The __get_url method returns the URL for the API, based on the url, wp_api, and version arguments.

    The __get_oauth_url method generates an OAuth 1.0a URL for the API request, using the OAuth class from the woocommerce.oauth module.

    The __is_ssl method is a private helper method that checks if the url uses HTTPS.
    '''   

    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = kwargs.get("wp_api", True)
        self.version = kwargs.get("version", "wc/v3")
        self.is_ssl = self.__is_ssl()
        self.timeout = kwargs.get("timeout", 5)
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.query_string_auth = kwargs.get("query_string_auth", False)
        self.user_agent = kwargs.get("user_agent", f"WooCommerce-Python-REST-API/{__version__}")

    def __is_ssl(self):
        """ Check if url use HTTPS """
        return self.url.startswith("https")

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = f"{url}/"

        if self.wp_api:
            api = "wp-json"

        return f"{url}{api}/{self.version}/{endpoint}"

    def __get_oauth_url(self, url, method, **kwargs):
        """ Generate oAuth1.0a URL """
        oauth = OAuth(
            url=url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            version=self.version,
            method=method,
            oauth_timestamp=kwargs.get("oauth_timestamp", int(time()))
        )

        return oauth.get_oauth_url()

    def __request(self, method, endpoint, data, params=None, **kwargs):
        """ Do requests """
        if params is None:
            params = {}
        url = self.__get_url(endpoint)
        auth = None
        headers = {
            "user-agent": f"{self.user_agent}",
            "accept": "application/json"
        }

        if self.is_ssl is True and self.query_string_auth is False:
            auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        elif self.is_ssl is True and self.query_string_auth is True:
            params.update({
                "consumer_key": self.consumer_key,
                "consumer_secret": self.consumer_secret
            })
        else:
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
            url = self.__get_oauth_url(url, method, **kwargs)

        if data is not None:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')
            headers["content-type"] = "application/json;charset=utf-8"

        return request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            auth=auth,
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        """ Get requests """
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """ DELETE requests """
        return self.__request("DELETE", endpoint, None, **kwargs)

    def options(self, endpoint, **kwargs):
        """ OPTIONS requests """
        return self.__request("OPTIONS", endpoint, None, **kwargs)
