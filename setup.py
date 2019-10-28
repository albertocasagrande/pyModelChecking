#!/usr/bin/env python

from setuptools import setup, find_packages
from pyModelChecking import __version__

with open('README.md') as f:
    long_desc = f.read()

setup(name='pyModelChecking',
      version=__version__,
      description='A simple Python model checking package',
      long_description=long_desc,
      long_description_content_type='text/markdown', 
      keywords = "model checking temporal logics kripke structure",
      author='Alberto Casagrande',
      author_email='acasagrande@units.it',
      license='GNU General Public License, version 2',
      url='https://github.com/albertocasagrande/pyModelChecking',
      packages=find_packages(),
      install_requires=[
          'lark-parser',
      ],
      test_suite="pyModelChecking.tests",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
      ],
      python_requires='>=3.6',
     )
