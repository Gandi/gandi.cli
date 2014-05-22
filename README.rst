Gandi CLI project
=================

Gandi command line interface project

-----------------
You can use Gandi cli as a command line
>>> gandi
>>> gandi list --help

-----------------
You can also use Gandi cli modules as a python modules

>>> from gandi.cli.modules.iaas import Iaas
>>> Iaas.list()
>>> Iaas.info(648)
