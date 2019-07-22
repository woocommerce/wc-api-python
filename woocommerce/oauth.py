# -*- coding: utf-8 -*-

"""
WooCommerce OAuth1.0a Class
"""

__title__ = "woocommerce-oauth"
__version__ = "2.1.1"
__author__ = "Claudio Sanches @ Automattic"
__license__ = "MIT"

from time import time
from random import randint
from hmac import new as HMAC
from hashlib import sha1, sha256
from base64 import b64encode

try:
    from urllib.parse import urlencode, quote, unquote, parse_qsl, urlparse
except ImportError:
    from urllib import urlencode, quote, unquote
    from urlparse import parse_qsl, urlparse

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class OAuth(object):
    """ API Class """

    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.version = kwargs.get("version", "v3")
        self.method = kwargs.get("method", "GET")
        self.timestamp = kwargs.get("oauth_timestamp", int(time()))

    def get_oauth_url(self):
        """ Returns the URL with OAuth params """
        params = OrderedDict()

        if "?" in self.url:
            url = self.url[:self.url.find("?")]
            for key, value in parse_qsl(urlparse(self.url).query):
                params[key] = value
        else:
            url = self.url

        params["oauth_consumer_key"] = self.consumer_key
        params["oauth_timestamp"] = self.timestamp
        params["oauth_nonce"] = self.generate_nonce()
        params["oauth_signature_method"] = "HMAC-SHA256"
        params["oauth_signature"] = self.generate_oauth_signature(params, url)

        query_string = urlencode(params)

        return "%s?%s" % (url, query_string)

    def generate_oauth_signature(self, params, url):
        """ Generate OAuth Signature """
        if "oauth_signature" in params.keys():
            del params["oauth_signature"]

        base_request_uri = quote(url, "")
        params = self.sorted_params(params)
        params = self.normalize_parameters(params)
        query_params = ["{param_key}%3D{param_value}".format(param_key=key, param_value=value)
                        for key, value in params.items()]

        query_string = "%26".join(query_params)
        string_to_sign = "%s&%s&%s" % (self.method, base_request_uri, query_string)

        consumer_secret = str(self.consumer_secret)
        if self.version not in ["v1", "v2"]:
            consumer_secret += "&"

        hash_signature = HMAC(
            consumer_secret.encode(),
            str(string_to_sign).encode(),
            sha256
        ).digest()

        return b64encode(hash_signature).decode("utf-8").replace("\n", "")

    @staticmethod
    def sorted_params(params):
        ordered = OrderedDict()
        base_keys = sorted(set(k.split('[')[0] for k in params.keys()))

        for base in base_keys:
            for key in params.keys():
                if key == base or key.startswith(base + '['):
                    ordered[key] = params[key]

        return ordered

    @staticmethod
    def normalize_parameters(params):
        """ Normalize parameters """
        params = params or {}
        normalized_parameters = OrderedDict()

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

    @staticmethod
    def generate_nonce():
        """ Generate nonce number """
        nonce = ''.join([str(randint(0, 9)) for i in range(8)])
        return HMAC(
            nonce.encode(),
            "secret".encode(),
            sha1
        ).hexdigest()
