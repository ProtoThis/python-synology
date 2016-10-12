#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io

from setuptools import setup


# NOTE(StaticCube) Guidelines for Major.Minor.Micro
# - Major means an API contract change
# - Minor means API bugfix or new functionality
# - Micro means change of any kind (unless significant enough for a minor/major).
version = '0.0.1'


setup(name='python-synology',
      version=version,
      description='Python API for communication with Synology DSM',
      long_description=io.open('README.rst', encoding='UTF-8').read(),
      keywords='synology dsm',
      author='Ferry van Zeelst',
      author_email='info@StaticCube.com',
      url='https://github.com/StaticCube/python-synology/',
      packages=['synology'],
      install_requires=['requests>=1.0.0']
      )