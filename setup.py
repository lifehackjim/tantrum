#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Package setup."""
import os

from codecs import open

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, "tantrum", "version.py")


about = {}
with open(version_path, "r", "utf-8") as f:
    x = f.readlines()
    contents = "\n".join(a for a in x if not a.startswith("#"))
    exec(contents, about)  # nosec


with open("README.md", "r", "utf-8") as f:
    readme = f.read()

packages = find_packages()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_data={"": ["LICENSE"]},
    package_dir={"tantrum": "tantrum"},
    scripts=[],  # TODO(!)
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=["requests[security,socks]", "six", "xmltodict"],
    tests_require=[],
    license=about["__license__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
