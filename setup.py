#!/usr/bin/env python

from setuptools import setup

setup(name='pdfcomments',
      version='0.1',
      description='extract comments from PDF',
      author='Michael Hoffman',
      author_email='michael.hoffman@utoronto.ca',
      license='GPLv3',
      packages=['pdfcomments'],
      package_data={'pdfcomments': ['data/*']},
      install_requires=['PyPDF2'],
      python_requires='>=3.6',
      entry_points={
        'console_scripts': ['pdfcomments=pdfcomments.__main__:main'],
      },
      zip_safe=False)
