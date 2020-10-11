"""Sphinx configuration."""
from datetime import datetime


project = "Python API for Synology DSM"
author = "Ferry van Zeelst"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_rtd_theme"]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
