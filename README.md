# woocommerceaio

An async Python wrapper for the WooCommerce REST API. Easily interact with the WooCommerce REST API using this library.

This library is a fork of the original work by Claudio Sanches on [wc-api-python](https://github.com/woocommerce/wc-api-python).

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

| Option                | Type        | Required | Description                                                                                           |
|-----------------------|-------------|----------|-------------------------------------------------------------------------------------------------------|
| `url`               | `string`  | yes      | Your Store URL, example: http://woo.dev/                                                              |
| `consumer_key`      | `string`  | yes      | Your API consumer key                                                                                 |
| `consumer_secret`   | `string`  | yes      | Your API consumer secret                                                                              |
| `version`           | `string`  | no       | API version, default is ``wc/v3``                                                                     |
| `timeout`           | `integer` | no       | Connection timeout, default is ``5``                                                                  |
| `verify_ssl`        | `bool`    | no       | Verify SSL when connect, use this option as `False` when need to test with self-signed certificates |
| `query_string_auth` | `bool`    | no       | Force Basic Authentication as query string when ``True`` and using under HTTPS, default is `False`  |
| `user_agent`        | `string`  | no       | Set a custom User-Agent, default is `woocommerceaio/<version>`                             |
| `oauth_timestamp`   | `integer` | no       | Custom timestamp for requests made with oAuth1.0a                                                     |
| `wp_api`            | `bool`    | no       | Set to `False` in order to use the legacy WooCommerce API (deprecated)    

## Methods

|    Params    |      Type      |                           Description                            |
---------------|----------------|------------------------------------------------------------------|
| `endpoint` | `string``     | WooCommerce API endpoint, example: `customers` or `order/12` |
| `data`     | `dictionary` | Data that will be converted to JSON                              |
| `**kwargs` | `dictionary` | Accepts `params`, also other `httpx` arguments                   |

### GET

- `.get(endpoint, **kwargs)`

### POST

- `.post(endpoint, data, **kwargs)`

### PUT

- `.put(endpoint, data), **kwargs`

### DELETE

- `.delete(endpoint, **kwargs)`

### OPTIONS

- `.options(endpoint, **kwargs)`

## Response


All methods will return an httpx [`Response`](https://www.python-httpx.org/api/#response) object.

Example of returned data:

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

### Request with `params` example

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
