#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mini-sqlmap",
    version="1.0.0",
    author="Rikixz",
    author_email="blaxkmiradev@github.com",
    description="A SQL Injection Vulnerability Scanner for Bug Hunters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blaxkmiradev/mini-sqlmap",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "mini-sqlmap=mini_sqlmap:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
