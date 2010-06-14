# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
import sys
# Fool distutils to accept more than ASCII
reload(sys).setdefaultencoding('utf-8')

version = '0.4'

setup(name='repoze.who-use_beaker',
    version=version,
    description="Identifier plugin for repoze.who with beaker.session cache implementation",
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='beaker session auth repoze.who userid',
    author='Domen Kozar',
    author_email='domen@dev.si',
    maintainer='Linas Juškevičius',
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
