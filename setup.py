#!/usr/bin/env python
# -*- coding:utf-8 -*-

# NOTE(StaticCube) Guidelines for Major.Minor.Micro
# - Major means an API contract change
# - Minor means API bugfix or new functionality
# - Micro means change of any kind (unless significant enough for a minor/major).

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python-synology",
    version="0.4.0",
    url="https://github.com/StaticCube/python-synology/",
    download_url="https://github.com/StaticCube/python-synology/tarball/0.4.0",
    description="Python API for communication with Synology DSM",
    long_description=long_description,
    author="FG van Zeelst (StaticCube)",
    author_email="GitHub@StaticCube.com",
    packages=["synology_dsm"],  # this must be the same as the name above
    install_requires=["requests>=1.0.0"],
    python_requires=">=2.7.0",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["synology-dsm", "synology"],
)
