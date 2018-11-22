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
      install_requires=['path.py>=11', 'setuptools>=24.2.0'],
      python_requires='>=3.6',
      entry_points={
        'console_scripts': ['pdfcomments=pdfcomments.__main__:main'],
      },
      zip_safe=False)
