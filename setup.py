# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
import sys
# Fool distutils to accept more than ASCII
reload(sys).setdefaultencoding('utf-8')

REQUIRES = [
    "PasteScript",
    "repoze.who>=1.0.18",
    "Beaker>=1.4",
]
if sys.version_info < (2, 7):
    REQUIRES.append('ordereddict')
DES = (
    "Identifier plugin for repoze.who with "
    "beaker.session cache implementation"
)

VERSION = '0.4'

setup(
    name='repoze.who-use_beaker',
    version=VERSION,
    description=DES,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    classifiers=[],
    keywords='beaker session auth repoze.who userid',
    author='Domen Kozar, Linas Juškevičius, Andrew Colin Kissa',
    author_email='domen@dev.si, linas@idiles.com, andrew@topdog.za.net',
    maintainer='Andrew Colin Kissa',
    maintainer_email='andrew@topdog.za.net',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages=['repoze', 'repoze.who', 'repoze.who.plugins'],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['webob', 'webtest', 'nose'],
    install_requires=REQUIRES,
)
