# Gandi CLI

Use `$ gandi` to easily create and manage web resources from the command line.

* `$ gandi domain` to buy and manage your domain names
* `$ gandi paas` to create and deploy your web applications
* `$ gandi vm` to spin up and upgrade your virtual machines
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
  * [Advanced Usage](#advanced-usage)
    * [All Commands](#all-commands)
    * [Build manpage](#build-manpage)
    * [Configuration](#configuration)
    * [Development](#development)
  * [Contributing](#contributing)
  * [License](#license)

## Requirements

* A compatible operating system (Linux, BSD, Mac OS X/Darwin, Windows)
* Python 2.6/2.7/3.2/3.3/3.4

Recommended tools
* [pip](https://pip.pypa.io/en/latest/installing.html)
* [virtualenv](https://virtualenv.pypa.io/en/latest/virtualenv.html#installation)

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

### Creating a Virtual Machine

Gandi Server offers powerful Xen- and Linux-based virtual machines since 2007.

Virtual machines can be configured and upgraded on the fly to your liking. For example, you can start with 1GB of RAM, and run a command to add 2GB of RAM and 2 CPUs without even having to restart it.

Gandi Server measures consumption by the hour and uses a prepaid credit system. To learn more, [check out the Gandi Server website](https://www.gandi.net/hosting/server/).

#### 1. Create and access a VM

    $ gandi vm create
    > datacenter: FR
    > memory: 256
    > cores: 1
    > ip_version: 4
    > bandwidth: 102400
    > login: admin
    > hostname: tempo

Create a virtual machine with the default configuration and a random hostname.

#### 2. Upgrade a VM

    $ gandi vm update tempo --memory 2024 --cores 2

Set the VM's RAM to 2GB and add a CPU core on the fly.

#### 3. Create a custom VM

    $ gandi vm create --datacenter US --hostname docker --cores 2 --ram 3036GB --disk 10GB --image "Ubuntu 14.04 64 bits" --run "curl -s https://get.docker.io/ubuntu | sh"
    > datacenter: US
    > memory: 3036
    > cores: 2
    > ip_version: 4
    > bandwidth: 102400
    > login: admin
    > hostname: docker
    > image: Ubuntu 14.04 64 bits

This command will setup the above VM, and install docker by running `curl -s https://get.docker.io/ubuntu | sh` after creation.

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

### Development

To add a new command to the CLI:
  * check if there's an existing namespace to either add a command or an option to an already existing one
  * each command is composed of 2 python files, located in the `commands/` and `modules/` directories
    * `commands/` contains everything that is related to shell arguments, parameter validation, default values
    * `modules/` contains code that uses the Gandi API and can be used by other python scripts, or in the python shell.
    * `packages/` contains packaging code (see `packages/README.rst`)

Code must follow PEP8 recommendations: http://www.python.org/dev/peps/pep-0008/

Docstrings should follow PEP257 recommendations: http://www.python.org/dev/peps/pep-0257/


## Contributing

Create a git branch with your new feature or bugfix and either:
* mail the patch to feedback@gandi.net,
* send the URL for your branch and we will review/merge it if correct,
* open a merge request on GitHub

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
