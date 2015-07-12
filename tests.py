""" API Tests """
import unittest
import woocommerce
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

        self.assertEqual(api.version, "v3")

    def test_non_ssl(self):
        """ Test non-ssl """
        api = woocommerce.API(
            url="http://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )
        self.assertFalse(api.is_ssl)

    def test_with_ssl(self):
        """ Test non-ssl """
        api = woocommerce.API(
            url="https://woo.test",
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )
        self.assertTrue(api.is_ssl, True)

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
