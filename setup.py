#!/usr/bin/env python3.6

from setuptools import setup

setup(name='pdfcomments',
      version='0.1',
      description='extract comments from PDF',
      author='Michael Hoffman',
      author_email='michael.hoffman@utoronto.ca',
      license='GPLv3',
      packages=['pdfcomments'],
      entry_points = {
        'console_scripts': ['pdfcomments=pdfcomments.__main__:main'],
      },
      zip_safe=False)
