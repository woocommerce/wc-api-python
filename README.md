# woocommerceaio

An async Python wrapper for the WooCommerce REST API based on [httpx](https://www.python-httpx.org/). 

This is an _unofficial_ fork of the [WooCommerce-provided Python client](https://github.com/woocommerce/wc-api-python), originally created by Claudio Sanches.

The main difference between `woocommerceaio` and the official client resides in the use of the async HTTP library [httpx](https://www.python-httpx.org/) instead of [requests](https://requests.readthedocs.io/en/latest/).

Other differences include:

- Support for retries.
- Type hints.
- And more to come (as I use the library I need to add more features)

## Installation

```sh
pip install woocommerceaio
```

## Getting started

Generate API credentials (Consumer Key & Consumer Secret) following this instructions at http://woocommerce.github.io/woocommerce-rest-api-docs/#rest-api-keys.

Check out the WooCommerce API endpoints and data that can be manipulated in http://woocommerce.github.io/woocommerce-rest-api-docs/.

## Setup

```python
    from woocommerceaio import API

    wcapi = API(
        url="http://example.com",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        version="wc/v3"
    )
```

## Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `url` | `string` | yes | Your Store URL, example: http://woo.dev/ |
| `consumer_key` | `string`  | yes | Your API secret key |
| `consumer_secret` | `string` | yes | Your API consumer secret |
| `version` | `string` | no | API version, default is `wc/v3` |
| `timeout` | `integer` | no | Connection timeout, default is `5` |
| `verify_ssl` | `bool` | no | Verify SSL when connect, use this option as `False` when need to test with self-signed certificates |
| `query_string_auth` | `bool` | no | Force Basic Authentication as query string when `True` and using under HTTPS, default is `False` |
| `user_agent` | `string` | no | Set a custom User-Agent, default is `woocommerceaio/<version>` |
| `oauth_timestamp` | `integer` | no | Custom timestamp for requests made with oAuth1.0a |
| `wp_api` | `bool` | no | Set to `False` in order to use the legacy WooCommerce API (deprecated) |

## Methods

You can interact with the WooCommerce API using via the exposed methods `get()`, `post()`, `put()`, `delete()`, `options()`.

- All methods

 the following parameters.

| Params | Type | Description |
|--------|------|-------------|
| `endpoint` | `string` | WooCommerce API endpoint, example: `customers` or `order/12` |
| `data` | `dictionary` | Data that will be converted to JSON |
| `**kwargs` | `dictionary` | Accepts `params`, also other `httpx` arguments (see next section) |

### kwargs params

`woocommerceaio` allows you to pass any `httpx` arguments as `kwargs` params. This is useful if you want to customize headers, timeouts, and other request parameters. For a list of available params, refer to the [httpx documentation](https://www.python-httpx.org/api/#request).

Additionally, `woocommerceaio` provides the following custom `kwargs` params:

| Params | Type | Description |
|--------|------|-------------|
| `max_retries` | `bool` | Maximum number of retries on failed requests. Default is `3` |
| `retry_backoff` | `float` | Backoff time to apply between attempts after the second try (most errors are resolved immediately by a second try without a delay). Default is `0.5` seconds. This value will be multiplied by a factor of two for each consequent retry. So the default delay sequence will be `0.5`, `1`, `2`, `4`, `8` etc. seconds |

### Response

All methods will return an httpx [`Response`](https://www.python-httpx.org/api/#response) object. For more information on how to use this object, refer to the [httpx documentation](https://www.python-httpx.org/api/#response).

## Examples

### Retrieving store products

```python
    >>> r = await wcapi.get("products")
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'application/json; charset=UTF-8'
    >>> r.encoding
    'UTF-8'
    >>> r.text
    u'{"products":[{"title":"Flying Ninja","id":70,...' // Json text
    >>> r.json()
    {u'products': [{u'sold_individually': False,... // Dictionary data
```

### Making requests with `params`

```python
    from woocommerceaio import API

    async def example():
        wcapi = API(
            url="http://example.com",
            consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            version="wc/v3"
        )

        # Force delete example.
        response = await wcapi.delete("products/100", params={"force": True})
        print(response.json())

        # Query example.
        response = await wcapi.get("products", params={"per_page": 20})
        print(response.json())

    if __name__ == "__main__":
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(example())
```

## Changelog

See `CHANGELOG.md`.
