# WooCommerce API - Python Client

A Python wrapper for the WooCommerce REST API. Easily interact with the WooCommerce REST API using this library.

[![build status](https://secure.travis-ci.org/woothemes/wc-api-python.svg)](http://travis-ci.org/woothemes/wc-api-python)

## Installation

```
pip install woocommerce
```

## Getting started

Generate API credentials (Consumer Key & Consumer Secret) following this instructions <http://docs.woothemes.com/document/woocommerce-rest-api/>
.

Check out the WooCommerce API endpoints and data that can be manipulated in <http://woothemes.github.io/woocommerce-rest-api-docs/>.

## Setup

```py
from woocommerce import WooCommerce

var WooCommerce = new WooCommerceAPI({
  url: 'http://example.com',
  consumerKey: 'ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  consumerSecret: 'cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
});
```

### Options

|      Option      |   Type   | Required |                                             Description                                             |
| ---------------- | -------- | -------- | --------------------------------------------------------------------------------------------------- |
| `url`            | `string` | yes      | Your Store URL, example: http://woo.dev/                                                            |
| `consumerKey`    | `string` | yes      | Your API consumer key                                                                               |
| `consumerSecret` | `string` | yes      | Your API consumer secret                                                                            |
| `version`        | `string` | no       | API version, default is `v3`                                                                        |
| `verify_ssl`     | `bool`   | no       | Verify SSL when connect, use this option as `false` when need to test with self-signed certificates |

## Methods

|   Params   |     Type     |                         Description                          |
| ---------- | ------------ | ------------------------------------------------------------ |
| `endpoint` | `string`     | WooCommerce API endpoint, example: `customers` or `order/12` |
| `data`     | `dictionary` | Data that will be converted to JSON                          |

### GET

- `.get(endpoint)`

### POST

- `.post(endpoint, data)`

### PUT

- `.put(endpoint, data)`

### DELETE

- `.delete(endpoint)`

## Response

All methods will return [Requests](http://docs.python-requests.org/en/latest/) object.

Example of returned data:

```bash
>>> woocommerce.get("products")
>>> woocommerce.status_code
200
>>> woocommerce.headers['content-type']
'application/json; charset=UTF-8'
>>> woocommerce.encoding
'UTF-8'
>>> woocommerce.text
u'{"products":[{"title":"Flying Ninja","id":70,...' // Json text
>>> woocommerce.json()
{u'products': [{u'sold_individually': False,... // Dictionary data
```
