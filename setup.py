# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='repoze.who-use_beaker',
      version=version,
      description="Identifier plugin for repoze.who with beaker.session cache implementation",
      long_description=open('README.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='beaker session auth repoze.who userid',
      author='Domen Kozar',
      author_email='domen@dev.si',
      maintainer='Linas Juskevicius',
      maintainer_email='linas@idiles.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      namespace_packages=['repoze', 'repoze.who', 'repoze.who.plugins'],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['webob', 'webtest', 'nose'],
      install_requires=[
          "PasteScript",
          "repoze.who>=1.0.18",
          "Beaker>=1.4",
      ],
      )
