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

`gandi` is a command line client to manage, create and delete product for a specific account
on Gandi.net platform.

GETTING STARTED
===============

  Run `gandi setup` or create $HOME/.config/gandi/config.yaml file.

ENVIRONMENT VARIABLES
=====================

`API_ENV` allow to switch between environment: the production API and the OT&E one.

Example:
  API_ENV=production gandi domain list


`API_HOST` allow to specify a HTTP URL to connect and to send the API commands.

`API_KEY` allow to specify an API key for the chosen environment. This option is useful when you work with multiple account.

COMMAND-LINE OPTIONS
=====================

-v          Enable or disable verbose mode.
--version   Display version.

Namespaces:

*  api                     Display information about API used.
*  certificate change-dcv  Change the DCV for a pending certificate.
*  certificate create      Create a new certificate.
*  certificate delete      Revoke the certificate.
*  certificate export      Write the certificate to <output> or <fqdn>.
*  certificate info        Display information about a certificate.
*  certificate list        List certificates.
*  certificate packages    List certificate packages.
*  certificate resend-dcv  Resend the DCV mail for a pending certificate.
*  certificate update      Update a certificate CSR.
*  config                  Configure default values.
*  datacenters             List available datacenters.
*  deploy                  Deploy code on a remote vhost.
*  disk create             Create a new disk.
*  disk delete             Delete a disk.
*  disk info               Display information about a disk.
*  disk list               List disks.
*  disk update             Update a disk.
*  docker                  Manage docker instances.
*  domain create           Buy a domain.
*  domain info             Display information about a domain.
*  domain list             List domains.
*  help                    Display help for a command.
*  mail create             Create a mailbox.
*  mail delete             Delete a mailbox.
*  mail info               Display information about a mailbox.
*  mail list               List mailboxes created on a domain.
*  mail purge              Purge a mailbox.
*  mail update             Update a mailbox.
*  oper info               Display information about an operation.
*  oper list               List operations.
*  paas clone              Clone a remote vhost in a local git repository.
*  paas console            Open a console on a PaaS.
*  paas create             Create a new PaaS instance and initialize associated git repository.
*  paas delete             Delete a PaaS instance.
*  paas info               Display information about a PaaS instance.
*  paas list               List PaaS instances.
*  paas restart            Restart a PaaS instance.
*  paas types              List types PaaS instances.
*  paas update             Update a PaaS instance.
*  record create           Create new DNS zone record entry for a domain.
*  record list             List DNS zone records for a domain.
*  setup                   Initialize Gandi CLI configuration.
*  snapshotprofile info    Display information about a snapshot profile.
*  snapshotprofile list    List possible snapshot profiles.
*  sshkey create           Create a new SSH key.
*  sshkey delete           Delete SSH keys.
*  sshkey info             Display information about an SSH key.
*  sshkey list             List SSH keys.
*  vhost create            Create a new vhost.
*  vhost delete            Delete a vhost.
*  vhost info              Display information about a vhost.
*  vhost list              List vhosts.
*  vm console              Open a console to virtual machine.
*  vm create               Create a new virtual machine.
*  vm delete               Delete a virtual machine.
*  vm images               List available system images for virtual machines.
*  vm info                 Display information about a virtual machine.
*  vm list                 List virtual machines.
*  vm reboot               Reboot a virtual machine.
*  vm ssh                  Spawn an SSH session to virtual machine.
*  vm start                Start a virtual machine.
*  vm stop                 Stop a virtual machine.
*  vm update               Update a virtual machine.


Details:

* ``gandi api`` display information about the Gandi.net API.

* ``certificate change-dcv resource`` allow to change the domain validation process for a specific certificate request. Mandatory option is ``--dcv-method TEXT`` where the method could be email, dns, file or auto.

* ``certificate create`` allow to request the creation of a certificate. If a private key is present as ``--private-key`` and not a CSR, the CSR will be generated. If no CSR or private key are present in the parameters, both are generated. Possible options are ``--csr TEXT`` and ``--private-key TEXT`` which could be the content of a certificate request and a private key or path to the files, ``--country TEXT``, ``--state TEXT``, ``--city TEXT``, ``-organisation TEXT``, ``--branch TEXT`` to specify new administrative informations, ``--duration INTEGER`` how many years of validity (up to 5 years), ``--package TEXT`` is the type of certificate as listed by ``gandi certificate package``, ``--altnames LIST`` is a list of all alternative names and ``--dcv-method TEXT`` where the method could be email, dns, file or auto.

* ``certificate delete resource`` delete a certificate. Possible option is ``--force`` (or ``-f``) to bypass the validation question; usefull in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``). Note that a resource can be a cn entry or an integer id.

* ``certificate export resource`` write the selected certificate to a file. Possible option is ``--output TEXT`` for the path of the output file, ``--force`` overwrite any existing file. Note that a resource can be a cn entry or an integer id.

* ``certificate info resource`` show detailed view of a specific certificate. Possible options are ``--id``, ``--altnames``, ``--csr``, ``--cert`` which show the integer id, the alternative names, the certificate request and the full certificate, ``--all-status`` show the certificate without regard for its status. Note that a resource can be a cn entry or an integer id.

* ``certificate list`` Possible options are ``--id``, ``--altnames``, ``--csr``, ``--cert`` which show the integer id, the alternative names, the certificate request and the full certificate for each element of the list, ``--all-status`` show certificates without regards to their status, ``--status``, ``--dates`` show the status of the certificate and the creation and expiration dates, ``--limit INTEGER`` show a subset of the list.

* ``certificate packages`` show a full list of all available certificate types.

* ``certificate resend-dcv resource`` send the validation email again (only for the 'email' DCV method). Note that a resource can be a cn entry or an integer id.

* ``certificate update resource`` modify the options of a certificate. Possible options are ``--csr TEXT``, ``--private-key TEXT`` could be either the content of a certificate request and a private key or a path to the files, ``--country TEXT``, ``--state TEXT``, ``--city TEXT``, ``--organisation TEXT``, ``--branch TEXT`` to specify new administrative informations, ``--altnames LIST`` to change all the alternative names (comma separated text without space), ``--dcv-method TEXT`` with domain validation process method in email, dns, file, auto. Note that a resource can be a CN entry or an integer id.

* ``gandi config key value`` configure value in the configuration file. With no option, configuration setting is stored in the local directory, which makes it suitable for code repositories. Using the ``-g`` flag, the change is stored in the global configuration file.

* ``gandi datacenters`` list all the datacenters of the Gandi.net platform. Possible option is ``--id`` to obtain the id of the datacenter. Most of the time you will be able to use the datacenter name as parameter to the methods.

* ``gandi deploy virtualhost.domain.tld1`` push the files in the current directory to the virtualhost setup on a Gandi Simple Hosting instance.

* ``gandi disk create`` create a new virtual disk. Possible options are ``--name TEXT`` for the label of the virtual disk, ``--size INTEGER`` for the new size of the disk, ``--datacenter FR|US|LU`` for the geographical datacenter as listed by ``gandi datacenters``, ``--vm TEXT`` to attach the newly create virtual disk to an existing virtual machine instance, ``--snapshotprofile 1|2|3|7`` to select a profile of snapshot to apply to the disk for keeping multiple version of data in a timeline. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk delete resource`` delete a virtual disk identified as resource. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk info resource`` show a detailed view of a specific virtual disk identified as resource.

  ``gandi disk list`` show a list of virtual disk. Possible options to filter the list are : ``--only-data`` and ``--only-snapshot`` which limit the list to regular disk and to snapshots, ``--type`` add the type of the virtual disk, ``--id`` add the integer id of each virtual disk, ``--vm`` show the virtual machines by which the disk are used, ``--snapshotprofile`` show the profile of data retention associated and ``--limit INTEGER`` show only a limit amount of disks.

* ``gandi disk update resource`` modify the options of a virtual disk. Possible options are ``--name TEXT`` for the label of the virtual disk, ``--size INTEGER`` for the new size of the disk, ``--snapshotprofile TEXT`` to select a profile of snapshot to apply to the disk for keeping multiple version of data in a timeline. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi docker`` will setup ssh forwarding towards a gandi VM, remotely feeding a docker unix socket. This, for example, can be used for zeroconf access to scripted temporary build VMs. The ``--vm`` option alters the ``dockervm`` configuration parameter and can be used to set the VM used for future docker connections. ``dockervm`` can also be set locally for per-project vms (See ``gandi config``). *NOTE*: passing option parameters to docker require the usage of the POSIX argument parsing ``--`` separator. *NOTE*: a local docker client is required for this command to operate.

* ``gandi domain create`` helps register a domain. Options are ``--domain domain.tld`` for the domain you want to get, ``--duration INTEGER RANGE`` for the registration period, ``--owner TEXT``, ``--admin TEXT``, ``--tech TEXTE``, ``--bill TEXT`` for the four contacts to pass to the creation process. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi domain info domain.tld`` show information about the specific domain ``domain.tld`` : owner, admin, billing and technical contacts, fully qualified domain name, nameservers, associated zone, associated tags and more.

* ``gandi domain list`` show all the domains in the Gandi account. Possible option is ``--limit INTEGER`` which will show a subset of the list.

* ``gandi help command`` display help for command, if command is a namespace it will display list of available commands for this namespace.

* ``gandi mail create login@domain.tld`` create a new mailbox. Possible options are ``-q, --quota INTEGER`` to define a quota for this mailbox, ``-f, --fallback TEXT`` to define a fallback addresse, ``-a, --alias TEXT`` to add an alias for this mailbox, this last option can be used multiple times.

* ``gandi mail delete login@domain.tld`` delete mailbox ``login@domain.tld``. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi mail info login@domain.tld`` show information about mailbox ``login@domain.tld``.

* ``gandi mail list domain.tld`` show all existing mailboxes for specific domain ``domain.tld``.

* ``gandi mail purge login@domain.tld`` purge mailbox ``login@domain.tld``. Possible options are ``-a, --alias`` to purge all aliases on this mailbox, ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi mail update login@domain.tld`` update mailbox ``login@domain.tld``. Possible options are ``-p, --password`` will prompt for a new password for this mailbox, ``-q, --quota INTEGER`` to define a quota for this mailbox, ``-f, --fallback TEXT`` to define a fallback addresse, ``-a, --alias-add TEXT`` to add an alias for this mailbox, can be used multiple times, ``-d, --alias-del TEXT`` to delete an alias for this mailbox, can be used multiple times.

* ``gandi oper info id`` show information about the operation ``id``.

* ``gandi oper list`` show all the running operation on your product at Gandi (for example Simple Hosting, domain, hosting). Possible option is ``--limit INTEGER`` which list only a subset of the full list of running operations.

* ``gandi paas clone host.domain.tld`` clone all files of a remote virtual host to a local git repository.

* ``gandi paas console resource`` open a console to the SimpleHosting. Note that resource could be a full qualified domain name or an integer id.

* ``gandi paas create`` allow to create a Simple Hosting instance. Mandatory option is  ``--password TEXT`` for the password of the instance. Possible option are ``--name TEXT`` for the name of the instance (if not present, will be autogenerated), ``--size s|m|x|xl|xxl`` for the size (amount of RAM and processes), ``--type TYPE`` for the type as listed by the ``gandi paas types`` command, ``--quantity INTEGER`` for the additional disk space, ``--duration TEXT`` for the number of month suffixed with 'm', ``--datacenter FR|US|LU`` for the geographical datacenter as listed by ``gandi datacenters``, ``--vhosts TEXT`` for a list of virtual hosts to link to this instance, ``--snapshotprofile TEXT`` for the snapshot profile for the disk of the instance, ``--sshkey TEXT`` to specifiy a name of a SSH key. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas delete resource`` delete a Simple Hosting instance. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas info resource`` show details about a specific Simple Hosting instance.

* ``gandi paas list`` show all the Simple Hosting instances. Possible options are ``--state TEXT`` for filtering the output by a specific state, ``--id`` which display the integer identificator, ``--vhosts`` which show all the virtual hosts associated with each instances, ``--type`` which display the type of Simple Hosting and ``--limit INTEGER`` which show only a subset of the full Simple Hosting list (default is 100).

* ``gandi paas restart resource`` allow to restart a Simple Hosting instance. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas types`` show all the Simple Hosting type available. For example: phpmysql which provides PHP and MySQL or pythonmongodb which provides Python and MongoDB.

* ``gandi paas updates resource`` modify the options of a Simple Hosting. Possible options are ``--name TEXT`` which allow to rename a instance, ``--size s|m|x|xl|xxl`` to change the size of the instance, ``--quantity INTEGER`` to add disk space, ``--password`` to change the password of the instance, ``--sshkey TEXT`` to specifiy a name of a SSH key, ``--upgrade TEXT`` to upgrade the instance to the latest system image, ``--console TEXT`` to enable or disable the console, ``--snapshotprofile TEXT`` to set the snapshot profile for the disk of the instance, ``--reset-mysql-password TEXT`` to reset the root password of MySQLd running on the instance. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi record create domain.tld`` will create new DNS zone record entry for specific domain ``domain.tld`` in a new zone version and activate it. Mandatory options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used, ``--name TEXT`` to set record relative name, may contains leading wildcard, use @ for empty name, ``--type A|AAAA|CNAME|MX|NS|TXT|WKS|SRV|LOC|SPF`` to set record type, ``--value TEXT`` to set record value, may contains up to 1024 ascii characters. Possible options are ``--ttl INTEGER`` to set record time to live value.

* ``gandi record list domain.tld`` show the list of DNS zone records for specific domain ``domain.tld``. Possible options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used.

* ``gandi setup`` initialize the configuration for the tool.

* ``gandi snapshotprofile info resource`` detail the information about a profile : frequency of snapshot and retention period.

* ``gandi snapshotprofile list`` show the list of all profile for virtual disk snapshot. Possible options are ``--only-paas`` and ``--only-vm`` to filter the output and show only the subset of profile for the Simple Hosting or the Gandi Hosting.

* ``gandi sshkey create --name label`` add a SSH key identified by ``label`` which could be used for authentification. Possible option are ``--value TEXT``  with the content of the SSH public key or ``--sshkey FILENAME`` with the path to a file containing the SSH public key.

* ``gandi sshkey delete resource`` remove a SSH key. Resource can be a name or the specific id.

* ``gandi sshkey info resource`` show details of an SSH key: name and fingeprint. Possible option are ``--id`` which also show the id of theSSH key and ``--value`` which show the content of the SSH key.

* ``gandi sshkey list`` show all the SSH keys registered. Possible option are ``--id`` which add numeric identificator and ``--limit INTEGER`` which show only a subset of the SSH keys.

* ``gandi vhost create`` add a virtual host. Mandatory options are ``--vhost TEXT`` for the fully qualified domain name (FQDN like host.domain.tld) and ``--paas TEXT`` for the Simple Hosting instance on which it will create the virtual host, ``--alter-zone`` will update the domain zone. Creation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vhost delete host.domain.tld`` delete a virtual host after asking for user validation. Possible option is ``--force`` to bypass the validation question; useful in non-interactive mode when scripting. Deletion can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vhost info host.domain.tld`` show details about a specific virtual host. Possible option is ``--ids`` which show the integer identificator.

* ``gandi vhost list`` show all the virtual host defined in Simple Hosting. Possible option are ``--names`` which add the name of the Simple Hosting instance on which the virtual host is setup, ``--ids`` which show the integer identificator and ``--limit INTEGER`` which show a subset of the full list of virtual host.

* ``gandi vm console resource`` open a console on the virtual machine and give you a shell access.

* ``gandi vm create`` create a new virtual machine. Possible options are ``--hostname TEXT`` for the hostname of the machine (if not present, will be autogenerated), ``--datacenter FR|US|LU`` for the geographical datacenter as listed by ``gandi datacenters``, ``--memory INTEGER`` for quantity of memory, ``--cores INTEGER`` for number of virtual CPU, ``--ip-version 4|6`` for version of created IP, ``--bandwidth INTEGER`` to set network bandwidth in bits/s on first network interface created, ``--login TEXT`` to define login to created on virtual machine, ``--image TEXT`` for the disk image to be used to boot the virtual machine as listed by ``gandi vm images``, ``--sshkey TEXT`` to specifiy name of a SSH key, ``--password`` will prompt for a password to set for the created login, ``--run TEXT`` to specify shell command that will run at the first boot of virtual machine. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vm delete resource`` destroy a virtual machine, its main disk and its first virtual network interface. This operation can be done as background process using the option ``--background`` (or ``--bg``). Another possible parameter is ``--force`` to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi vm images pattern`` list all the available images of system whose name contains the pattern. Possible option is ``--datacenter FR|US|LU`` which filter by geograhical datacenter.

* ``gandi vm list`` show all the virtual machine created in Gandi hosting for the account. Possible options are ``--state`` which filter the output according to define virtual machine state, ``--id`` to obtain the id of each virtual machine, ``--limit INTEGER`` which list only a subset of the full list of virtual machines.

* ``gandi vm info resource`` show details of a specific operation.

* ``gandi vm ssh resource`` open a ssh connection on the virtual machine and give you a shell access. The ``-i TEXT`` option (or ``--identity TEXT``) refers to a local ssh key, as used in the ssh command. The ``-l TEXT``, ``--login TEXT`` or ``user@host`` form specifies remote username in the same way. Using ``--wipe-key``, previous entry for that host is discarded from the known_hosts file first.

* ``gandi vm start resource`` allow to start a virtual machine (a resource can either be a hostname as defined in the creation process or the id of the virtual machine). This operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vm stop resource``, same parameter as start but allow to stop the virtual machine. Obviously.

* ``gandi vm reboot resource``, same parameter as start but allow to reboot a virtual machine.

* ``gandi vm update resource`` allow to change the quantity of memory (using ``--memory INTEGER``), the number of virtual CPU (using ``--cores INTEGER``), enable the virtual console which allow to get a shell to the virtual machine even without network interfaces on the virtual machine (using ``--console``) or change the root password (using ``--password``). All these modification can be done as background process using the option ``--background`` (or ``--bg``).


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

This is version 0.1.

CHANGELOG
=========

See CHANGES.rst in the project directory or in the documentation directory of your system. For Debian, the CHANGES file will be in /usr/share/doc/gandicli/.

TODO
====

Add missing Gandi product like ``virtual network interface`` or ``private vlan``.

BUGS
====

Please report any bugs or issue on https://github.com/Gandi/gandi.cli by opening an issue using this form https://github.com/Gandi/gandi.cli/issues/new. You can send patches by email to feedback@gandi.net.
