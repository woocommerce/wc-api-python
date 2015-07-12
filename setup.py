#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Setup module """

from setuptools import setup
import os
import re


# Get version from __init__.py file
VERSION = ""
with open("woocommerce/__init__.py", "r") as fd:
    VERSION = re.search(r"^__version__\s*=\s*['\"]([^\"]*)['\"]", fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError("Cannot find version information")

# Get long description
README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="woocommerce",
    version=VERSION,
    description="A Python wrapper for the WooCommerce REST API",
    long_description=README,
    author="Claudio Sanches @ WooThemes",
    url="http://www.woothemes.com",
    license="MIT",
    packages=["woocommerce"],
    include_package_data=True,
    install_requires=[
        "requests"
    ]
)
