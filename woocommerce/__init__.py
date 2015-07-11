# -*- coding: utf-8 -*-

"""
woocommerce-api
~~~~~~~~~~~~~~~
A Python wrapper for WooCommerce API.

:copyright: (c) 2015 by WooThemes.
:license: MIT, see LICENSE for details.
"""

__title__ = "woocommerce-api"
__version__ = "1.0.0"
__author__ = "Claudio Sanches @ WooThemes"
__license__ = "MIT"

import re
import requests
from oauthlib.oauth1 import Client as oAuth1


class WooCommerce(object):
    """ API Class """
    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.version = kwargs.get("version", "v3")
        self.is_ssl = self.__is_ssl()
        self.verify_ssl = kwargs.get("verify_ssl", True)

    def __is_ssl(self):
        """ Check if url use HTTPS """
        return re.match(r"^https", self.url) is not None

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url

        if re.match(r".*(/)$", self.url) is None:
            url += "/"

        return url + 'wc-api/' + self.version + '/' + endpoint

    def __request(self, method, endpoint, data):
        """ Do requests """
        url = self.__get_url(endpoint)

        if self.is_ssl is True:
            auth = (self.consumer_key, self.consumer_secret)
        else:
            auth = oAuth1(
                client_key=self.consumer_key,
                client_secret=self.consumer_secret
            ).sign(url, method)
            print auth

        return requests.request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            auth=auth,
            data=data
        ).json()

    def get(self, endpoint):
        """ Get requests """
        return self.__request("GET", endpoint, None)

    def post(self, endpoint, data):
        """ POST requests """
        return self.__request("POST", endpoint, data)

    def put(self, endpoint, data):
        """ PUT requests """
        return self.__request("PUT", endpoint, data)

    def delete(self, endpoint):
        """ DELETE requests """
        return self.__request("DELETE", endpoint, None)
