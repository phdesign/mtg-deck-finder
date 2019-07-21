#!/usr/bin/env python3

"""
Python setuptools install script.

Usage:
$ python setup.py install               # install globally
$ python setup.py install --user        # install for user
$ python setup.py develop               # install symlink for development
$ python setup.py develop --uninstall   # uninstall for development
$ python setup.py sdist                 # create package in /dist
"""

from setuptools import setup, find_packages

VERSION = "0.3"

setup(
    name="mtg-deck",
    version=VERSION,
    description="Magic The Gathering deck operations",
    author="Paul Heasley",
    author_email="paul@phdesign.com.au",
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": ["mtg-deck=mtg_deck.__main__:main", "mtg-deck-finder=mtg_deck_finder.__main__:main"]
    },
    include_package_data=True,
    license="MIT",
    install_requires=[],
    zip_safe=True,
)
