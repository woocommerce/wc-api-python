""" API Tests """
import unittest
import woocommerceaio
from woocommerceaio import oauth
from pytest_httpx import HTTPXMock
import pytest

@pytest.fixture()
def api():
    yield woocommerceaio.API(
        url="https://woo.test",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )

@pytest.fixture()
def api_http():
    yield woocommerceaio.API(
        url="http://woo.test",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )

class TestWooCommerceAPI:
    """Test case for the client methods."""

    def test_version(self, api: woocommerceaio.API):
        """ Test default version """
        api.version == "wc/v3"

    def test_non_ssl(self, api_http: woocommerceaio.API):
        """ Test non-ssl """
        assert api_http.is_ssl is False

    def test_with_ssl(self, api: woocommerceaio.API):
        """ Test ssl """
        assert api.is_ssl is True

    @pytest.mark.asyncio
    async def test_with_timeout(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test timeout """
        api = woocommerceaio.API(
            url="https://woo.test",
            consumer_key=api.consumer_key,
            consumer_secret=api.consumer_secret,
            timeout=10,
        )
        assert api.timeout == 10

        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.get("products")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test GET requests """

        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.get("products")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_with_parameters(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test GET requests w/ url params """

        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.get("products", params={"per_page": 10, "page": 1, "offset": 0})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_with_requests_kwargs(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test GET requests w/ optional requests-module kwargs """

        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.get("products", allow_redirects=True)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test POST requests """

        httpx_mock.add_response(status_code=201, content="OK")

        response = await api.post("products", {})
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_put(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test PUT requests """
        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.put("products", {})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete(self, api: woocommerceaio.API, httpx_mock: HTTPXMock):
        """ Test DELETE requests """

        httpx_mock.add_response(status_code=200, content="OK")

        response = await api.delete("products")
        assert response.status_code == 200

    def test_oauth_sorted_params(self):
        """ Test order of parameters for OAuth signature """
        def check_sorted(keys, expected):
            params = oauth.OrderedDict()
            for key in keys:
                params[key] = ''

            ordered = list(oauth.OAuth.sorted_params(params).keys())
            assert ordered == expected

        check_sorted(['a', 'b'], ['a', 'b'])
        check_sorted(['b', 'a'], ['a', 'b'])
        check_sorted(['a', 'b[a]', 'b[b]', 'b[c]', 'c'], ['a', 'b[a]', 'b[b]', 'b[c]', 'c'])
        check_sorted(['a', 'b[c]', 'b[a]', 'b[b]', 'c'], ['a', 'b[c]', 'b[a]', 'b[b]', 'c'])
        check_sorted(['d', 'b[c]', 'b[a]', 'b[b]', 'c'], ['b[c]', 'b[a]', 'b[b]', 'c', 'd'])
        check_sorted(['a1', 'b[c]', 'b[a]', 'b[b]', 'a2'], ['a1', 'a2', 'b[c]', 'b[a]', 'b[b]'])
