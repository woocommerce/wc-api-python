# -*- coding: utf-8 -*-

"""
WooCommerce OAuth1.0a Class
"""

__title__ = "woocommerce-oauth"
__version__ = "1.0.0"
__author__ = "Claudio Sanches @ WooThemes"
__license__ = "MIT"

from time import time
from random import randint
from hmac import new as HMAC
from hashlib import sha1, sha256
from collections import OrderedDict
from base64 import b64encode

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from urllib import urlencode, quote, unquote
except ImportError:
    from urllib.parse import urlencode, quote, unquote


class OAuth(object):
    """ API Class """

    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.version = kwargs.get("version", "v3")
        self.method = kwargs.get("method", "GET")

    def get_oauth_url(self):
        """ Returns the URL with OAuth params """
        params = {}

        if "?" in self.url:
            url = self.url[:self.url.find("?")]
            for key, value in urlparse.parse_qsl(urlparse.urlparse(self.url).query):
                params[key] = value
        else:
            url = self.url

        params["oauth_consumer_key"] = self.consumer_key
        params["oauth_timestamp"] = int(time())
        params["oauth_nonce"] = HMAC(
            str(time() + randint(0, 99999)).encode(),
            "secret".encode(),
            sha1
        ).hexdigest()
        params["oauth_signature_method"] = "HMAC-SHA256"
        params["oauth_signature"] = self.generate_oauth_signature(params, url)

        query_string = urlencode(params)

        return "%s?%s" % (url, query_string)

    def generate_oauth_signature(self, params, url):
        """ Generate OAuth Signature """
        if "oauth_signature" in params.keys():
            del params["oauth_signature"]

        base_request_uri = quote(url, "")
        params = self.normalize_parameters(params)
        params = OrderedDict(sorted(params.items()))
        query_params = ["{param_key}%3D{param_value}".format(param_key=key, param_value=value)
                        for key, value in params.items()]

        query_string = "%26".join(query_params)
        string_to_sign = "%s&%s&%s" % (self.method, base_request_uri, query_string)

        consumer_secret = str(self.consumer_secret)
        if self.version == "v3":
            consumer_secret += "&"

        hash_signature = HMAC(
            consumer_secret.encode(),
            str(string_to_sign).encode(),
            sha256
        ).digest()

        return b64encode(hash_signature).decode("utf-8").replace("\n", "")

    @staticmethod
    def normalize_parameters(params):
        """ Normalize parameters """
        params = params or {}
        normalized_parameters = {}

        def get_value_like_as_php(val):
            """ Prepare value for quote """
            try:
                base = basestring
            except NameError:
                base = (str, bytes)

            if isinstance(val, base):
                return val
            elif isinstance(val, bool):
                return "1" if val else ""
            elif isinstance(val, int):
                return str(val)
            elif isinstance(val, float):
                return str(int(val)) if val % 1 == 0 else str(val)
            else:
                return ""

        for key, value in params.items():
            value = get_value_like_as_php(value)
            key = quote(unquote(str(key))).replace("%", "%25")
            value = quote(unquote(str(value))).replace("%", "%25")
            normalized_parameters[key] = value

        return normalized_parameters
