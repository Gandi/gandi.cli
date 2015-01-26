# Gandi CLI

Use `$ gandi` to easily create and manage web resources from the command line.

* `$ gandi domain` to buy and manage your domain names
* `$ gandi paas` to create and deploy your web applications
* `$ gandi vm` to spin up and upgrade your virtual machines
* `$ gandi certificate` to manage your ssl certificates
* `$ gandi` to list all available commands
* [Detailed examples](#use-cases)
* [All commands](#all-commands)

## Table of contents

  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Getting started](#getting-started)
  * [Use cases](#use-cases)
    * [Registering a Domain Name](#registering-a-domain-name)
    * [Creating a Virtual Machine](#creating-a-virtual-machine)
    * [Deploying a Web Application](#deploying-a-web-application)
    * [Creating a SSL Certificate](#creating-a-ssl-certificate)
    * [Creating a Private VLAN](#creating-a-private-vlan)
  * [Advanced Usage](#advanced-usage)
    * [All Commands](#all-commands)
    * [Build manpage](#build-manpage)
    * [Configuration](#configuration)
    * [Development](#development)
  * [Contributing](#contributing)
  * [Code status](#code-status)
  * [License](#license)

## Requirements

* A compatible operating system (Linux, BSD, Mac OS X/Darwin, Windows)
* Python 2.6/2.7/3.2/3.3/3.4

Recommended tools
* [pip](https://pip.pypa.io/en/latest/installing.html)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

## Installation

### Install with pip and virtualenv

    $ virtualenv /some/directory/gandi.cli
    $ source /some/directory/gandi.cli/bin/activate
    $ pip install gandi.cli

### Build from source

    $ cd /path/to/the/repository
    $ python setup.py install --user

### From the Debian package

    $ ln -sf packages/debian debian && debuild -us -uc -b && echo "Bisou"

## Getting started

1. To get started, you can create a [free Gandi account](https://www.gandi.net/contact/create) and get your Gandi Handle
2. [Generate your Production API Token](https://www.gandi.net/admin/api_key) from the account admin section
3. You may also want to [top-up your prepaid account](https://www.gandi.net/prepaid)
4. To manipulate VM's, you also need to [purchase credits](https://www.gandi.net/credit/buy) (you can use funds from your prepaid account)

Then run the setup

    $ gandi setup
    > API Key: x134z5x4c5c          # copy-paste your api key
    > Environment [production] :    # press enter for Production, the default
    > SSH key [~/.ssh/id_rsa.pub] : # your SSH public key for hosting instances and servers

See the [Advanced Usage](#advanced-usage) section for more details on configuration.

## Use cases

  * [Registering a domain name](#registering-a-domain-name)
  * [Creating a virtual machine](#creating-a-virtual-machine)
  * [Deploying a web application](#deploying-a-web-application)

### Registering a Domain Name

Gandi is a domain name registrar since 1999. The oldest in France and one of the world's leading, Gandi is recognized for its No Bullshit™ trademark and approach to domain names.

You can now buy and manage domains in any of the 500+ TLD's that Gandi offers from the command line.

[Know more about Gandi Domains on the website](https://www.gandi.net/domain).

#### 1. Buy a domain using the interactive prompt

    $ gandi domain create
    > Domain: example.com      # enter the domain name here
    > example.com is available
    > Duration [1] : 1         # enter the duration in years

This will create a domain and use your default information for Ownership, Admin, Technical and Billing info.


#### 2. Buy a domain in one line

    $ gandi domain create --domain example.com --duration 1

#### 3. Buy a domain with custom contacts

    $ gandi domain create --domain example.com --duration 1 --owner XYZ123-GANDI --admin XYZ123-GANDI --tech XYZ123-GANDI --bill XYZ123-GANDI

You can use the information of Gandi handles associated to Contacts in your account to setup Owner, Admin, Technical and Billing info.

#### 3. List your domains

    $ gandi domain list

#### 4. Get information about a domain

    $ gandi domain info example.com

#### 5. List NS records of a domain
    $ gandi record list example.com

You can use `--output` to extract your zone records in a file, then edit it and use `gandi record update example.com -f file` to update it easily.

### Creating a Virtual Machine

Gandi Server offers powerful Xen- and Linux-based virtual machines since 2007.

Virtual machines can be configured and upgraded on the fly to your liking. For example, you can start with 1GB of RAM, and run a command to add 2GB of RAM and 2 CPUs without even having to restart it.

Gandi Server measures consumption by the hour and uses a prepaid credit system. To learn more, [check out the Gandi Server website](https://www.gandi.net/hosting/server/).

#### 1. Create and access a VM

    $ gandi vm create
    * root user will be created.
    * SSH key authorization will be used.
    * No password supplied for vm (required to enable emergency web console access).
    * Configuration used: 1 cores, 256Mb memory, ip v4+v6, image Debian 7, hostname: temp1415183684

Create a virtual machine with the default configuration and a random hostname.

#### 2. Upgrade a VM

    $ gandi vm update temp1415183684 --memory 2048 --cores 2

Set the VM's RAM to 2GB and add a CPU core on the fly.

#### 3. Create a custom VM

    $ gandi vm create --datacenter US --hostname docker --cores 2 --memory 3072 --size 10240 --image "Ubuntu 14.04 64 bits LTS (HVM)" --run "curl -sSL https://get.docker.com/ubuntu/ | sh"
    * root user will be created.
    * SSH key authorization will be used.
    * No password supplied for vm (required to enable emergency web console access).
    * Configuration used: 2 cores, 3072Mb memory, ip v4+v6, image Ubuntu 14.04 64 bits LTS, hostname: docker

This command will setup the above VM, and install docker by running `curl -sSL https://get.docker.com/ubuntu/ | sh` after creation.

#### 4. View your ressources

    $ gandi vm list

#### 5. Get all the details about a VM

    $ gandi vm info docker


### Deploying a Web Application

Gandi Simple Hosting is a PaaS (Platform as a Service) offering fast code deployment and easy scaling, powering over 50,000 apps since its inception in 2012.

Instances can run apps in 4 languages (PHP, Python, Node.js and Ruby) along with one of 3 popular databases (MySQL, PostgreSQL and MongoDB) and operate on a managed platform with built-in http caching.

Plans cover all scales, from small to world-class projects. [Check out the website for more information](https://www.gandi.net/hosting/simple).

#### 1. Create an instance for your app


    $ gandi paas create --name myapp --type phpmysql --size S --datacenter FR --duration 1


#### 2. Update code and deploy

    $ cd myapp
    $ git init .
    $ git add .
    $ git commit -m 'first commit'
    $ git push gandi master
    $ gandi deploy


### Creating a SSL Certificate

Gandi SSL offers a range of SSL certificates to help you secure your projects.

You can order, obtain, update and revoke your certificates from the command line.

#### 1. Find the right plan for you


    $ gandi certificate plans

Our Standard, Pro and Business plans offer different validation methods and guarantees. Each plan supports all or some of these types of certificates: single address, wildcard and/or multiple subdomains.

To discover our offering and find the right certificate for your project, [compare our plans](https://www.gandi.net/ssl/compare) and [try our simulator](https://www.gandi.net/ssl/which-ssl-certificate).

Gandi CLI can choose the right certificate type for you depending on the number of domains (altnames) you supply at creation time. You only need to set it if you plan on adding more domains to the certificate in the future.

#### 2. Create the Certificate

WARNING : This command is billable.

To request a certificate, you need to use a private key to generate and sign a CSR (Certificate Signing Request) that will be supplied to Gandi.

The `create` command will take care of this for you if you don't have them already, or you can supply your CSR directly.

Check out the examples below or [our wiki](http://wiki.gandi.net/ssl) for more information on how SSL certificates work.

To create a single domain Standard certificate:

    $ gandi certificate create --cn "domain.tld"

For a wildcard Standard certificate:

    $ gandi certificate create --cn "*.domain.tld"

For a multi domain Standard certificate:

    $ gandi certificate create --cn "*.domain.tld" --altnames "host1.domain.tld" --altnames "host2.domain.tld"

You can also specify a plan type. For example, for a single domain Business certificate:

    $ gandi certificate create --cn "domain.tld" --type "bus"

If you have a CSR (you can give the CSR content or the path):

    $ gandi certificate create --csr /path/to/csr/file


#### 3. Follow the Certificate create operation


    $ gandi certificate follow <operation_id>


#### 4. Get the Certificate


As soon as the operation is DONE, you can export the certificate.

    $ gandi certificate export "domain.tld"


You can also retrieve intermediate certificates if needed.

    $ gandi certificate export "domain.tld" --intermediate

Find information on how to use your certificate with different servers on [our wiki](http://wiki.gandi.net/en/ssl).

### Creating a private VLAN

You can use Gandi CLI to create and setup your private VLANs. For more detailed information on how VLANs and networking in general works at Gandi, please check out our resources:

    * Tutorial: [Creating a private VLAN with Gandi CLI](http://wiki.gandi.net/en/tutorials/cli/pvlan)
    * Reference: [VLAN on Gandi Wiki](http://wiki.gandi.net/en/iaas/references/network/pvlan)
    * Reference: [Networking on Gandi Wiki](http://wiki.gandi.net/en/iaas/references/network)

#### Create a VLAN

    $ gandi vlan create --name my-vlan-in-lu --datacenter LU \
    --subnet "192.168.1.0/24" --gateway 192.168.1.1

To create a VLAN you need to determine its `name` and `datacenter`.

You can also set the `subnet` at creation time, or a default subnet will be chosen for you. The `gateway` setting is also optional and you can update both of these settings at any moment.

    $ gandi vlan update my-vlan-in-lu --gateway 192.168.1.254

#### Attach an existing VM to a VLAN

To add an existing VM to a VLAN, you can create a private network interface and attach it to the VM.

    $ gandi ip create --vlan my-vlan-in-lu --attach my-existing-vm --ip 192.168.1.254

If you don't specify the IP you want to use, one will be chosen for you from the VLAN's subnet.

#### Create a "Private VM"

In fact there's no such thing as a "Private VM", but you can create a VM and only attach a private interface to it.

    $ gandi vm create --hostname my-private-vm --vlan my-vlan-in-lu --ip 192.168.1.2

Please note that a private VM cannot be accessed through the emergency console. You'll need a public VM that also has a private interface on the same VLAN to gain access.

You can check out [our tutorial](http://wiki.gandi.net/en/tutorials/cli/pvlan) for an example of how to achieve this.

#### More options

    $ gandi vlan --help

Use the `--help` flag for more VLAN management options.


## Advanced Usage

### All Commands

To list all available commands, type `$ gandi --help`

For extended instructions, check out the `man` page.

### Build manpage

Install python-docutils and run:

    $ rst2man --no-generator gandicli.man.rst > gandi.1.man

Then to read the manpage:

    $ man ./gandi.1.man

### Configuration

Run `$ gandi setup` to configure your settings (see [Getting started](#getting-started))

Use `$ gandi config` to set and edit custom variables.
The default variables are:
  * `sshkey`         # path to your public ssh key
  * `api.host`       # the URL of the API endpoint to use (i.e OTE or Production)
  * `api.key`        # the relevant API key for the chosen endpoint


## Contributing

We <3 contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Code status

[![Build Status](https://travis-ci.org/Gandi/gandi.cli.svg?branch=master)](https://travis-ci.org/Gandi/gandi.cli)

## License / Copying

Copyright © 2014 Gandi S.A.S

Gandi CLI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gandi CLI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gandi CLI.  If not, see <http://www.gnu.org/licenses/gpl.txt>.
