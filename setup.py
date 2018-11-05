#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyModelChecking',
      version='0.1.1',
      description='A simple Python model checking package',
      keywords = "model checking temporal logics kripke structure",
      author='Alberto Casagrande',
      author_email='acasagrande@units.it',
      license='GNU General Public License, version 2',
      url='https://github.com/albertocasagrande/pyModelChecking',
      packages=find_packages(),
      test_suite="tests",
      classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
      ]
     )
