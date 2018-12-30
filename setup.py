#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
            self.pytest_args = []
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open(os.path.join(here, 'gandi', 'cli', '__init__.py')) as v_file:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(v_file.read()).group(1)

requires = ['setuptools', 'pyyaml', 'click>=7.0', 'requests', 'IPy']

tests_require = ['pytest', 'pytest-cov', 'tox']

if sys.version_info < (3, 0):
    tests_require += ['mock']
else:
    if sys.version_info < (3, 4):
        raise RuntimeError(
            "Python 3 earlier than 3.4 is not supported"
            " (sys.version: {})".format(sys.version))

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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Terminals',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      url='https://github.com/Gandi/gandi.cli',
      packages=find_packages(),
      cmdclass={'test': PyTest},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require=extras_require,
      entry_points={
          'console_scripts': [
              'gandi = gandi.cli.__main__:main',
          ],
      },
      )
