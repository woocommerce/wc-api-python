""" API Tests """
import unittest
import woocommerce
from woocommerce import oauth
from httmock import all_requests, HTTMock


class WooCommerceTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.consumer_key = "ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.consumer_secret = "cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.api = woocommerce.API(
            url="http://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )

    def test_version(self):
        """ Test default version """
        api = woocommerce.API(
            url="https://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )

        self.assertEqual(api.version, "wc/v3")

    def test_non_ssl(self):
        """ Test non-ssl """
        api = woocommerce.API(
            url="http://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )
        self.assertFalse(api.is_ssl)

    def test_with_ssl(self):
        """ Test ssl """
        api = woocommerce.API(
            url="https://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )
        self.assertTrue(api.is_ssl, True)

    def test_with_timeout(self):
        """ Test timeout """
        api = woocommerce.API(
            url="https://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            timeout=10,
        )
        self.assertEqual(api.timeout, 10)

        @all_requests
        def woo_test_mock(*args, **kwargs):
            """ URL Mock """
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = api.get("products").status_code
        self.assertEqual(status, 200)

    def test_get(self):
        """ Test GET requests """
        @all_requests
        def woo_test_mock(*args, **kwargs):
            """ URL Mock """
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.get("products").status_code
        self.assertEqual(status, 200)

    def test_get_with_parameters(self):
        """ Test GET requests w/ url params """
        @all_requests
        def woo_test_mock(*args, **kwargs):
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.get("products", params={"per_page": 10, "page": 1, "offset": 0}).status_code
            self.assertEqual(status, 200)

    def test_get_with_requests_kwargs(self):
        """ Test GET requests w/ optional requests-module kwargs """

        @all_requests
        def woo_test_mock(*args, **kwargs):
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.get("products", allow_redirects=True).status_code
            self.assertEqual(status, 200)

    def test_post(self):
        """ Test POST requests """
        @all_requests
        def woo_test_mock(*args, **kwargs):
            """ URL Mock """
            return {'status_code': 201,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.post("products", {}).status_code
        self.assertEqual(status, 201)

    def test_put(self):
        """ Test PUT requests """
        @all_requests
        def woo_test_mock(*args, **kwargs):
            """ URL Mock """
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.put("products", {}).status_code
        self.assertEqual(status, 200)

    def test_delete(self):
        """ Test DELETE requests """
        @all_requests
        def woo_test_mock(*args, **kwargs):
            """ URL Mock """
            return {'status_code': 200,
                    'content': 'OK'}

        with HTTMock(woo_test_mock):
            # call requests
            status = self.api.delete("products").status_code
        self.assertEqual(status, 200)

    def test_oauth_sorted_params(self):
        """ Test order of parameters for OAuth signature """
        def check_sorted(keys, expected):
            params = oauth.OrderedDict()
            for key in keys:
                params[key] = ''

            ordered = list(oauth.OAuth.sorted_params(params).keys())
            self.assertEqual(ordered, expected)

        check_sorted(['a', 'b'], ['a', 'b'])
        check_sorted(['b', 'a'], ['a', 'b'])
        check_sorted(['a', 'b[a]', 'b[b]', 'b[c]', 'c'], ['a', 'b[a]', 'b[b]', 'b[c]', 'c'])
        check_sorted(['a', 'b[c]', 'b[a]', 'b[b]', 'c'], ['a', 'b[c]', 'b[a]', 'b[b]', 'c'])
        check_sorted(['d', 'b[c]', 'b[a]', 'b[b]', 'c'], ['b[c]', 'b[a]', 'b[b]', 'c', 'd'])
        check_sorted(['a1', 'b[c]', 'b[a]', 'b[b]', 'a2'], ['a1', 'a2', 'b[c]', 'b[a]', 'b[b]'])
