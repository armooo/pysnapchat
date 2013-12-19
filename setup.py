#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

long_description = """
A Python API for Snapchat

Features
========
    * View all friends and snaps under an account
    * Ability to send snaps(accepts arbitrary data)
    * Ability to download snaps(without marking the snap as viewed)
"""

setup(
    name = "pysnapchat",
    version = "0.1",
    description = "a Python API for Snapchat",
    long_description = long_description,
    keywords = "snapchat api",
    author = "Chad Brubaker",
    author_email = "pencilo.mmotl@gmail.com",
    url = "https://github.com/pencilo/pysnapchat",
    license = "Apache License 2.0",
    packages = find_packages(),
    )
