#!/usr/bin/env python

from setuptools import setup

version = {}
with open("pdfcomments/_version.py") as fh:
    exec(fh.read(), version)

setup(
    name="pdfcomments",
    version=version["__version__"],
    description="extract comments from PDF",
    author="Michael Hoffman",
    author_email="michael.hoffman@utoronto.ca",
    license="GPLv3",
    package_data={"pdfcomments": ["py.typed"]},
    packages=["pdfcomments"],
    install_requires=["PyPDF2"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["pdfcomments=pdfcomments.__main__:main"],},
    zip_safe=False,
)
