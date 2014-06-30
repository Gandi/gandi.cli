=======
 gandi
=======

-----------------------------------------------------------------
command line interface to Gandi.net products using the public API
-----------------------------------------------------------------

:Author: aegiap@gandi.net
:Date: 2014-06-30
:Copyright: GPL-3
:Version: 0.1
:Manual section: 1
:Manual group: python

SYNOPSIS
========

  gandi [-v] [--version]
  gandi api|config|datacenters|deploy|domain|oper|paas|setup|vm ...

DESCRIPTION
===========

gandi is a command line client to manage, create and delete product for a specific account
on Gandi.net platform.

GETTING STARTED
===============

  Run gandi setup or create $HOME/.config/gandi/config.yaml file.

COMMAND-LINE OPTIONS
=====================

-v          Enable or disable verbose mode.
--version   Display version.

Namespaces:

*  api            Display information about API used.
*  config         Configure default values
*  datacenters    List available datacenters.
*  deploy         Deploy code on a remote vhost.
*  domain create  Buy a domain.
*  domain info    Display information about a domain.
*  domain list    List domains.
*  oper info      Display information about an operation.
*  oper list      List operations.
*  paas clone     Clone a remote vhost in a local git...
*  paas create    Create a new PaaS instance and initialize...
*  paas delete    Delete a PaaS instance.
*  paas info      Display information about a PaaS instance.
*  paas list      List PaaS instances.
*  paas types     List types Paas instances.
*  paas update    Update a PaaS instance.
*  setup          Initialize Gandi CLI configuration.
*  vm console     Open a console to virtual machine.
*  vm create      Create a new virtual machine.
*  vm delete      Delete a virtual machine.
*  vm images      List available system images for virtual...
*  vm info        Display information about a virtual machine.
*  vm list        List virtual machines.
*  vm reboot      Reboot a virtual machine.
*  vm start       Start a virtual machine.
*  vm stop        Stop a virtual machine.
*  vm update      Update a virtual machine.


FILES
=====

Configuration file is $HOME/.config/gandi/config.yaml

AUTHORS
=======

Originaly created by Dejan Filipovic for Gandi S.A.S.
Copyright (c) 2014 - Gandi S.A.S

CONTRIBUTORS
============

 - Dejan Filipovic <dejan.filipovic@gandi.net>
 - Guillaume Gauvrit <guillaume.gauvrit@gandi.net>
 - Alexandre Solleiro <alexandre.solleiro@gandi.net>
 - Nicolas Chipaux <aegiap@gandi.net>

VERSION
=======

This is version 0.1. It is currently a proof of concept.

BUGS
====

None known at the moment.
