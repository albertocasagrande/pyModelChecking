#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyModelChecking',
      version='0.1',
      description='A simple Python model checking package',
      author='Alberto Casagrande',
      author_email='acasagrande@units.it',
      license='GNU General Public License, version 2',
      url='https://github.com/albertocasagrande/pyModelChecking',
      packages=find_packages(),
      test_suite="tests",
     )
