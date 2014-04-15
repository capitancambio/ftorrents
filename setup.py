#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name = "ftorrents",
    version = "0.1",
    packages = find_packages(),
    scripts=['ftorrents.sh'],
    author = "Javier Asensio-Cubero",
    author_email = "capitan.cambio@gmail.com",
    description = "showsrss.info automatic downloader",
    license = "PSF",
    keywords = "showsrss.info",
    install_requires=[
            "pyyaml>=3.10",
            "feedparser>=5.1.2"
            ],

)
