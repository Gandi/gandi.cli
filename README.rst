Gandi CLI project
=================

Gandi command line interface project

-----------------
You can use Gandi cli as a command line
>>> gandi
>>> gandi vm list --help

-----------------
You can also use Gandi cli modules as a python modules

>>> from gandi.cli.modules.iaas import Iaas
>>> Iaas.list()
>>> Iaas.info(648)


Build man page
--------------

install python-docutils and run:
  rst2man --no-generator gandicli.man.rst > gandi.1.man

then to read the manpage:
  man ./gandi.1.man


How to install
--------------

Use pypy installation:
  virtualenv /some/directory/gandicli
  source /some/directory/gandicli/bin/enable
  pip install python-yaml python-click gandicli

and you will be able to start:
  gandi --help


Distribution packages
----------------------

See packages/README.rst
