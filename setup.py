#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


with open(os.path.join(here, 'gandi', 'cli', '__init__.py')) as v_file:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(v_file.read()).group(1)

requires = ['pyyaml', 'click<=3.1', 'requests']


setup(name='gandi.cli',
      namespace_packages=['gandi'],
      version=version,
      description='Gandi command line interface',
      long_description=README + '\n\n' + CHANGES,
      author='Gandi',
      author_email='feedback@gandi.net',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
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
      entry_points="""\
[console_scripts]
gandi = gandi.cli.__main__:main
""",
      )
