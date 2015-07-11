#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Testing """
import woocommerce


WC = woocommerce.WooCommerce(
    url="http://test.woo.com/",
    consumer_key="ck_38d5d5d8e55936cb7d67ad00492aa96b47fd325f",
    consumer_secret="cs_0c13a7221ecbceee1715879d9349fa52cec20b93"
)

print WC.get("customers")
