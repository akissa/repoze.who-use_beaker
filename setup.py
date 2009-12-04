# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='repoze.who.plugins.use_beaker',
      version=version,
      description="Identifier plugin with beaker.session cache implementation",
      long_description=open('README.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='beaker session auth repoze.who userid',
      author='Domen Kozar',
      author_email='domen@dev.si',
      maintainer='Linas Juškevičius',
      maintainer_email='linas@idiles.com',
      url='http://bitbucket.org/kaukas/repoze.who.plugins.use_beaker',
      license='/',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['webob', 'webtest', 'nose'],
      install_requires=[
        "PasteScript",
        "repoze.who",
        "Beaker",
      ],
      )
