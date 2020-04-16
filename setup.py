#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE(ProtoThis) Guidelines for Major.Minor.Micro
# - Major means an API contract change
# - Minor means API bugfix or new functionality
# - Micro means change of any kind (unless significant enough for a minor/major).

from setuptools import setup, find_packages
from codecs import open

REPO_URL = "https://github.com/ProtoThis/python-synology"
VERSION = "0.6.0"

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python-synology",
    version=VERSION,
    url=REPO_URL,
    download_url=REPO_URL + "/tarball/" + VERSION,
    description="Python API for communication with Synology DSM",
    long_description=long_description,
    author="FG van Zeelst (ProtoThis)",
    packages=find_packages(include=["synology_dsm*"]),
    install_requires=required,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["synology-dsm", "synology"],
)
