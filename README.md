# Gandi CLI

[![Build Status](https://travis-ci.org/Gandi/gandi.cli.svg?branch=master)](https://travis-ci.org/Gandi/gandi.cli)
[![Coverage Status](https://coveralls.io/repos/Gandi/gandi.cli/badge.svg?branch=master)](https://coveralls.io/r/Gandi/gandi.cli?branch=master)
[![Pip Version](https://img.shields.io/pypi/v/gandi.cli.svg)](https://pypi.python.org/pypi/gandi.cli)
[![Python Version](https://img.shields.io/pypi/pyversions/gandi.cli.svg)](https://pypi.python.org/pypi/gandi.cli)

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
    * [Deploying a Web Application with Simple Hosting](#deploying-a-web-application-with-simple-hosting)
    * [Creating a SSL Certificate](#creating-a-ssl-certificate)
    * [Adding a Web Application vhost with SSL](#adding-a-web-application-vhost-with-ssl)
    * [Creating a Private VLAN](#creating-a-private-vlan)
  * [Advanced Usage](#advanced-usage)
    * [All Commands](#all-commands)
    * [Build manpage](#build-manpage)
    * [Configuration](#configuration)
  * [Contributing](#contributing)
  * [Code status](#code-status)
  * [License](#license)

## Requirements

* A compatible operating system (Linux, BSD, Mac OS X/Darwin, Windows)
* Python 2.7/3.4/3.5/3.6/3.7
* openssl
* openssh
* git

Recommended tools
* [pip](https://pip.pypa.io/en/latest/installing.html)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
* docker

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
Using our classic (V4) website:
1. To get started, you can create a [free Gandi account](https://v4.gandi.net/contact/create) and get your Gandi Handle
2. [Generate your Production API Token](https://v4.gandi.net/admin/api_key) from the account admin section
3. You may also want to [top-up your prepaid account](https://v4.gandi.net/prepaid)
4. To manipulate VMs, you also need to [purchase credits](https://www.gandi.net/credit/buy) (you can use funds from your prepaid account)

Using our latest (V5) website:
1. To get started, you can create a [free Gandi account](https://account.gandi.net/en/create_account) and get your Gandi username
2. [Generate your Production API Token](https://account.gandi.net/en/) from within the account Security section
3. You may also want to [top-up your prepaid account](https://admin.gandi.net/billing/)
4. To manipulate VMs, you currently need to follow above steps to create an account on our classic (V4) website.


Then run the setup

    $ gandi setup
    > API Key: x134z5x4c5c          # copy-paste your api key
    > Environment [production] :    # press enter for Production, the default
    > SSH key [~/.ssh/id_rsa.pub] : # your SSH public key for hosting instances and servers

See the [Advanced Usage](#advanced-usage) section for more details on configuration.

## Use cases

  * [Registering a domain name](#registering-a-domain-name)
  * [Creating a virtual machine](#creating-a-virtual-machine)
  * [Deploying a web application with Simple Hosting](#deploying-a-web-application-with-simple-hosting)
  * [Creating a SSL Certificate](#creating-a-ssl-certificate)
  * [Adding a Web Application vhost with SSL](#adding-a-web-application-vhost-with-ssl)
  * [Creating a Private VLAN](#creating-a-private-vlan)

### Registering a Domain Name

Gandi has been a domain name registrar since 1999. The oldest in France and one of the world's leading, Gandi is recognized for its No Bullshit™ trademark and approach to domain names.

You can now buy and manage domains in any of the 500+ TLD's that Gandi offers from the command line.

[Learn more about Gandi Domains on the website](https://www.gandi.net/domain).

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

#### 5. Manage NS records for your domains

##### Create a new record

    $ gandi record create example.com --name www --type A --value 127.0.0.1

Add a new record to the domain's current zone file and activate it.

##### List your records

    $ gandi record list example.com

List a domain's zone file records. You can use the `--format` parameter to change the output format to `text` or `json`.

##### Update one record

    $ gandi record update example.com --record "@ 3600 IN A 127.0.0.1" --new-record "@ 3600 IN A 0.0.0.0"

This command is useful to update only one record at the time. The pattern to use is `name TTL CLASS TYPE value`.

You can easily check or copy-paste the values you need to replace using the `--format text` parameter:

    $ gandi record list example.com --format text


##### Update many records

    $ gandi record list example.com --format text > file.zone

Use this command to extract your zone records into a file called `file.zone` (or something else).

Simply edit the file to your liking and then update the entire zone file with it.

    $ gandi record update example.com -f file.zone

##### Delete records

    $ gandi record delete example.com --value 127.0.0.1

Delete all records that match the given parameters from a domain's zone file. In this example, if there were many records with '127.0.0.1' as their value, all of them would be deleted.

### Creating a Virtual Machine

Gandi Server offers powerful Xen- and Linux-based virtual machines since 2007.

Virtual machines can be configured and upgraded on the fly to your liking. For example, you can start with 1GB of RAM, and run a command to add 2GB of RAM and 2 CPUs without even having to restart it.

Gandi Server measures consumption by the hour and uses a prepaid credit system. To learn more, [check out the Gandi Server website](https://www.gandi.net/hosting/server/).

#### 1. Create and access a VM

    $ gandi vm create
    * root user will be created.
    * SSH key authorization will be used.
    * No password supplied for vm (required to enable emergency web console access).
    * Configuration used: 1 cores, 256Mb memory, ip v4+v6, image Debian 8, hostname: temp1415183684, datacenter: LU

Create a virtual machine with the default configuration and a random hostname.

#### 2. Upgrade a VM

    $ gandi vm update temp1415183684 --memory 2048 --cores 2

Set the VM's RAM to 2GB and add a CPU core on the fly.

#### 3. Create a custom VM

    $ gandi vm create --datacenter US --hostname docker --cores 2 --memory 3072 --size 10240 --image "Ubuntu 14.04 64 bits LTS (HVM)" --run "curl -sSL https://get.docker.com/ubuntu/ | sh"
    * root user will be created.
    * SSH key authorization will be used.
    * No password supplied for vm (required to enable emergency web console access).
    * Configuration used: 2 cores, 3072Mb memory, ip v4+v6, image Ubuntu 14.04 64 bits LTS, hostname: docker, datacenter: LU

This command will setup the above VM, and install docker by running `curl -sSL https://get.docker.com/ubuntu/ | sh` after creation.

#### 4. View your resources

    $ gandi vm list

#### 5. Get all the details about a VM

    $ gandi vm info docker


### Deploying a Web Application with Simple Hosting

Gandi Simple Hosting is a PaaS (Platform as a Service) offering fast code deployment and easy scaling, powering over 50,000 apps since its inception in 2012.

Instances can run apps in 4 languages (PHP, Python, Node.js and Ruby) along with one of 3 popular databases (MySQL, PostgreSQL and MongoDB) and operate on a managed platform with built-in http caching.

Plans cover all scales, from small to world-class projects. [Check out the website for more information](https://www.gandi.net/hosting/simple).

#### 1. Create a Simple Hosting instance

    $ gandi paas create --name myapp --type nodejspgsql --size S --datacenter FR --duration 1

#### 2. Attach and push to your instance's git repository

Simple Hosting offers two "modes": the **App mode**, where an instance offers a single git repository (`default.git`) and the **Sites mode**, where you can have multiple git repositories per instance (one for each VHOST, for example `www.myapp.com.git`).

Node.js, Python and Ruby instances run in App mode, whereas PHP instances run in Sites mode by default.
Note: If you create a wildcard VHOST for your PHP instance, the App mode will be activated.

Assuming you have local directory called `app` where you have placed your code base, you can use the following commands to create a git remote (called "gandi" by default) and push your code.

    $ cd app
    $ gandi paas attach myapp # App mode
    $ gandi paas attach myapp --vhost www.myapp.com # Sites mode
    $ git push gandi master

#### 3. Deploy your code

Still inside the `app` folder, you can use the following command to start the deploy process, which will checkout your code, install dependencies and launch (or relaunch) the app process:

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

WARNING: This command is billable.

To request a certificate, you need to use a private key to generate and sign a CSR (Certificate Signing Request) that will be supplied to Gandi.

The `create` command will take care of this for you if you don't have them already, or you can supply your CSR directly.

Check out the examples below or [our wiki](https://docs.gandi.net/en/ssl/) for more information on how SSL certificates work.

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

Find information on how to use your certificate with different servers on [our wiki](https://docs.gandi.net/en/ssl/).


### Adding a Web Application vhost with SSL


Gandi allows you to associate a certificate with your vhost.


#### 1. You already have the matching certificate at Gandi


Just create the vhost giving it the private key used to generate that certificate.

    $ gandi vhost create domain.tld --paas "PaasName" \
        --ssl --private-key "domain.tld.key"


#### 2. You have the matching certificate but not at Gandi (or in another account)


Declare the hosted certificate.

    $ gandi certstore create --pk "domain.tld.key" --crt "domain.tld.crt"

And then create the vhost.

    $ gandi vhost create domain.tld --paas "PaasName" --ssl


#### 3. You don't have any certificates but you plan to get one at Gandi


Create the certificate.

    $ gandi certificate create --cn "domain.tld.key" --type std

And then create the vhost.

    $ gandi vhost create domain.tld --paas "PaasName" \
        --ssl --private-key "domain.tld.key"


### Creating a private VLAN

You can use Gandi CLI to create and setup your private VLANs. For more detailed information on how VLANs and networking in general works at Gandi, please check out our resources:

* [Networking on Gandi Wiki](https://docs.gandi.net/en/cloud/resource_management/network_interface_management.html)

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
  * `api.host`       # the URL of the API endpoint to use (i.e. OTE or Production)
  * `api.key`        # the relevant API key for the chosen endpoint


## Contributing

We <3 contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

You can check the [contributors list](https://github.com/Gandi/gandi.cli/graphs/contributors).

## License / Copying

Copyright © 2014-2018 Gandi S.A.S

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
