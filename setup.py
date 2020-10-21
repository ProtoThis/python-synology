#!/usr/bin/env python
"""Synology DSM setup."""

# NOTE(ProtoThis) Guidelines for Major.Minor.Micro
# - Major means an API contract change
# - Minor means API bugfix or new functionality
# - Micro means change of any kind (unless significant enough for a minor/major).

from setuptools import setup, find_packages

REPO_URL = "https://github.com/ProtoThis/python-synology"
VERSION = "1.0.0"

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
    author="Quentin POLLET (Quentame) & FG van Zeelst (ProtoThis)",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=required,
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=["synology-dsm", "synology"],
)
