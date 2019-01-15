WooCommerce API - Python Client
===============================

A Python wrapper for the WooCommerce REST API. Easily interact with the WooCommerce REST API using this library.

.. image:: https://secure.travis-ci.org/woocommerce/wc-api-python.svg
    :target: http://travis-ci.org/woocommerce/wc-api-python

.. image:: https://img.shields.io/pypi/v/woocommerce.svg
    :target: https://pypi.python.org/pypi/WooCommerce


Installation
------------

.. code-block:: bash

    pip install woocommerce

Getting started
---------------

Generate API credentials (Consumer Key & Consumer Secret) following this instructions http://woocommerce.github.io/woocommerce-rest-api-docs/#rest-api-keys.

Check out the WooCommerce API endpoints and data that can be manipulated in http://woocommerce.github.io/woocommerce-rest-api-docs/.

Setup
-----

.. code-block:: python

    from woocommerce import API

    wcapi = API(
        url="http://example.com",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        wp_api=True,
        version="wc/v3"
    )

Options
~~~~~~~

+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
|         Option        |     Type    | Required |                                              Description                                              |
+=======================+=============+==========+=======================================================================================================+
| ``url``               | ``string``  | yes      | Your Store URL, example: http://woo.dev/                                                              |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``consumerKey``       | ``string``  | yes      | Your API consumer key                                                                                 |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``consumerSecret``    | ``string``  | yes      | Your API consumer secret                                                                              |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``wp_api``            | ``bool``    | no       | Allow requests to the WP REST API (WooCommerce 2.6 or later)                                          |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``version``           | ``string``  | no       | API version, default is ``v3``                                                                        |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``timeout``           | ``integer`` | no       | Connection timeout, default is ``5``                                                                  |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``verify_ssl``        | ``bool``    | no       | Verify SSL when connect, use this option as ``False`` when need to test with self-signed certificates |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``query_string_auth`` | ``bool``    | no       | Force Basic Authentication as query string when ``True`` and using under HTTPS, default is ``False``  |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+
| ``oauth_timestamp`` | ``integer``    | no       | Custom timestamp for requests made with oAuth1.0a                                                    |
+-----------------------+-------------+----------+-------------------------------------------------------------------------------------------------------+

Methods
-------

+--------------+----------------+------------------------------------------------------------------+
|    Params    |      Type      |                           Description                            |
+==============+================+==================================================================+
| ``endpoint`` | ``string``     | WooCommerce API endpoint, example: ``customers`` or ``order/12`` |
+--------------+----------------+------------------------------------------------------------------+
| ``data``     | ``dictionary`` | Data that will be converted to JSON                              |
+--------------+----------------+------------------------------------------------------------------+
| ``**kwargs`` | ``dictionary`` | Accepts ``params``, also other Requests arguments                |
+--------------+----------------+------------------------------------------------------------------+

GET
~~~

- ``.get(endpoint, **kwargs)``

POST
~~~~

- ``.post(endpoint, data, **kwargs)``

PUT
~~~

- ``.put(endpoint, data), **kwargs``

DELETE
~~~~~~

- ``.delete(endpoint, **kwargs)``

OPTIONS
~~~~~~~

- ``.options(endpoint, **kwargs)``

Response
--------

All methods will return `Response <http://docs.python-requests.org/en/latest/api/#requests.Response>`_ object.

Example of returned data:

.. code-block:: bash

    >>> r = wcapi.get("products")
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


Changelog
---------

2.0.0 - 2019/01/15
~~~~~~~~~~~~~~~~~~

- Updated "Requests" library to version 2.20.0.
- Added support for custom timestamps in oAuth1.0a requests with ``oauth_timestamp``.
- Allow pass custom arguments to "Requests" library.

1.2.1 - 2016/12/14
~~~~~~~~~~~~~~~~~~

- Fixed WordPress 4.7 compatibility.

1.2.0 - 2016/06/22
~~~~~~~~~~~~~~~~~~

- Added option ``query_string_auth`` to allow Basic Auth as query strings.

1.1.1 - 2016/06/03
~~~~~~~~~~~~~~~~~~

- Fixed oAuth signature for WP REST API.

1.1.0 - 2016/05/09
~~~~~~~~~~~~~~~~~~

- Added support for WP REST API.
- Added method to do HTTP OPTIONS requests.

1.0.5 - 2015/12/07
~~~~~~~~~~~~~~~~~~

- Fixed oAuth filters sorting.

1.0.4 - 2015/09/25
~~~~~~~~~~~~~~~~~~

- Implemented ``timeout`` argument for ``API`` class.

1.0.3 - 2015/08/07
~~~~~~~~~~~~~~~~~~

- Forced utf-8 encoding on ``API.__request()`` to avoid ``UnicodeDecodeError``

1.0.2 - 2015/08/05
~~~~~~~~~~~~~~~~~~

- Fixed handler for query strings

1.0.1 - 2015/07/13
~~~~~~~~~~~~~~~~~~

- Fixed support for Python 2.6

1.0.1 - 2015/07/12
~~~~~~~~~~~~~~~~~~

- Initial version
