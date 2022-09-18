# -*- coding: utf-8 -*-

"""
WooCommerce API Class
"""

__title__ = "woocommerce-api"
__version__ = "3.0.1"
__author__ = "Claudio Sanches & Antoine C"
__license__ = "MIT"

from json import dumps as jsonencode
from time import time
from urllib.parse import urlencode

from .oauth import OAuth
from requests import session
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth


class API(object):
    """API Class"""

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
        self.user_agent = kwargs.get(
            "user_agent", f"WooCommerce-Python-REST-API/{__version__}"
        )
        self.retries = kwargs.get("retries", 3)
        self.backoff_factor = kwargs.get("backoff_factor", 0.3)
        self.status_forcelist = kwargs.get(
            "status_forcelist", [500, 502, 503, 504, 429]
        )
        self.session = self.__requests_retry_session()

    def __is_ssl(self):
        """Check if url use HTTPS"""
        return self.url.startswith("https")

    def __requests_retry_session(self):
        """create a session and link a Retry adapter to it"""
        s = session()
        retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)

        if self.is_ssl:
            s.mount("https://", adapter)
        else:
            s.mount("http://", adapter)

        return s

    def __get_url(self, endpoint):
        """Get URL for requests"""
        url = self.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = f"{url}/"

        if self.wp_api:
            api = "wp-json"

        return f"{url}{api}/{self.version}/{endpoint}"

    def __get_oauth_url(self, url, method, **kwargs):
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

    def __request(self, method, endpoint, data, params=None, **kwargs):
        """Do requests"""
        if params is None:
            params = {}
        url = self.__get_url(endpoint)
        auth = None
        headers = {"user-agent": f"{self.user_agent}", "accept": "application/json"}

        if self.is_ssl is True and self.query_string_auth is False:
            auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
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

        return self.session.request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            auth=auth,
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs,
        )

    def get(self, endpoint, **kwargs):
        """Get requests"""
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        """POST requests"""
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """PUT requests"""
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """DELETE requests"""
        return self.__request("DELETE", endpoint, None, **kwargs)

    def options(self, endpoint, **kwargs):
        """OPTIONS requests"""
        return self.__request("OPTIONS", endpoint, None, **kwargs)
