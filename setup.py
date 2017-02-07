#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


with open(os.path.join(here, 'gandi', 'cli', '__init__.py')) as v_file:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(v_file.read()).group(1)

requires = ['setuptools', 'pyyaml', 'click>=3.1', 'requests', 'IPy']

tests_require = ['nose', 'coverage', 'tox', 'httpretty==0.8.6']
if sys.version_info < (2, 7):
    tests_require += ['unittest2', 'importlib']

if sys.version_info < (3, 3):
    tests_require.append('mock')

extras_require = {
    'test': tests_require,
}

setup(name='gandi.cli',
    namespace_packages=['gandi'],
    version=version,
    description='Gandi command line interface',
    long_description=README + '\n\n' + CHANGES,
    author='Gandi',
    author_email='feedback@gandi.net',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Terminals',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    url='https://github.com/Gandi/gandi.cli',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'gandi = gandi.cli.__main__:main',
        ],
    },
)
