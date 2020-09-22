=======
 gandi
=======

-----------------------------------------------------------------
command line interface to Gandi.net products using the public API
-----------------------------------------------------------------

:Author: aegiap@gandi.net
:Date: 2019-04-03
:Copyright: GPL-3
:Version: 1.6
:Manual section: 1

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

  Run `gandi setup` or create `$HOME/.config/gandi/config.yaml` file.

OPTIONS
=======

-v
    Enable or disable verbose mode, can be used multiple times to increase verbose level.

--version
    Display version.

NAMESPACES
==========

* account info            Display information about hosting account.
* api                     Display information about API used.
* certificate change-dcv  Change the DCV for a pending certificate.
* certificate create      Create a new certificate.
* certificate delete      Revoke the certificate.
* certificate follow      Follow the certificate operation run.
* certificate export      Write the certificate to <output> or <fqdn>.
* certificate info        Display information about a certificate.
* certificate list        List certificates.
* certificate packages    List certificate packages (deprecated).
* certificate plans       List certificate plans (replace packages).
* certificate resend-dcv  Resend the DCV mail for a pending certificate.
* certificate update      Update a certificate CSR.
* certstore create        Create an hosted certificate.
* certstore delete        Delete an hosted certificate.
* certstore info          Display information about an hosted certificate.
* certstore list          List hosted certificates.
* config delete           Delete a key/value pair from loaded configuration and save.
* config edit             Open configuration file in preferred editor.
* config get              Get value of a given key from loaded configuration.
* config list             List content of loaded configuration.
* config set              Set a key/value pair in loaded configuration and save.
* contact create          Create a new contact in interactive mode.
* datacenters             List available datacenters.
* deploy                  Deploy code on a remote vhost.
* disk attach             Attach a disk to a vm.
* disk create             Create a new disk.
* disk delete             Delete a disk.
* disk detach             Detach a disk from a vm.
* disk info               Display information about a disk.
* disk list               List disks.
* disk migrate            Migrate a disk to another datacenter.
* disk rollback           Rollback a disk from a snapshot.
* disk update             Update a disk.
* dns create              Create new record entry for a domain.
* dns delete              Delete record entry for a domain.
* dns domain.list         List domains manageable by REST API.
* dns keys create         Create key for a domain.
* dns keys delete         Delete a key for a domain.
* dns keys info           Display information about a domain key.
* dns keys list           List domain keys.
* dns keys recover        Recover deleted key for a domain.
* dns list                Display records for a domain.
* dns update              Update record entry for a domain.
* dnssec create           Create DNSSEC key.
* dnssec delete           Delete DNSSEC key.
* dnssec list             List DNSSEC keys.
* docker                  Manage docker instances.
* domain create           Buy a domain.
* domain renew            Renew a domain.
* domain info             Display information about a domain.
* domain list             List domains.
* forward create          Create a domain mail forward.
* forward delete          Delete a domain mail forward.
* forward list            List mail forwards for a domain.
* forward update          Update a domain mail forward.
* help                    Display help for a command.
* ip list                 List all ips.
* ip info                 Display information about an ip.
* ip create               Create a new ip.
* ip attach               Attach an ip to a vm.
* ip detach               Detach an ip from a vm.
* ip delete               Delete an ip.
* ip update               Update an ip.
* mail create             Create a mailbox.
* mail delete             Delete a mailbox.
* mail info               Display information about a mailbox.
* mail list               List mailboxes created on a domain.
* mail purge              Purge a mailbox.
* mail update             Update a mailbox.
* oper info               Display information about an operation.
* oper list               List operations.
* paas attach             Add an instance vhost's git remote to local git repository.
* paas clone              Clone a remote vhost in a local git repository.
* paas console            Open a console on a PaaS.
* paas create             Create a new PaaS instance and initialize associated git repository.
* paas delete             Delete a PaaS instance.
* paas info               Display information about a PaaS instance.
* paas list               List PaaS instances.
* paas restart            Restart a PaaS instance.
* paas types              List types PaaS instances.
* paas update             Update a PaaS instance.
* record create           Create new DNS zone record entry for a domain.
* record delete           Delete a record entry for a domain.
* record list             List DNS zone records for a domain.
* record update           Update records entries for a domain.
* setup                   Initialize Gandi CLI configuration.
* snapshotprofile info    Display information about a snapshot profile.
* snapshotprofile list    List possible snapshot profiles.
* sshkey create           Create a new SSH key.
* sshkey delete           Delete SSH keys.
* sshkey info             Display information about an SSH key.
* sshkey list             List SSH keys.
* status                  Display current status from status.gandi.net.
* vhost create            Create a new vhost.
* vhost delete            Delete a vhost.
* vhost info              Display information about a vhost.
* vhost list              List vhosts.
* vhost update            Update a vhost.
* vlan create             Create a new vlan
* vlan delete             Delete a vlan.
* vlan info               Display information about a vlan.
* vlan list               List vlans.
* vlan update             Update a vlan
* vm console              Open a console to virtual machine.
* vm create               Create a new virtual machine.
* vm delete               Delete a virtual machine.
* vm images               List available system images for virtual machines.
* vm info                 Display information about a virtual machine.
* vm kernels              List available kernels for virtual machines.
* vm list                 List virtual machines.
* vm migrate              Migrate a virtual machine to another datacenter.
* vm reboot               Reboot a virtual machine.
* vm ssh                  Spawn an SSH session to virtual machine.
* vm start                Start a virtual machine.
* vm stop                 Stop a virtual machine.
* vm update               Update a virtual machine.
* webacc add              Add a backend or a vhost on a webaccelerator
* webacc create           Create a webaccelerator
* webacc delete           Delete a webaccelerator, a vhost or a backend
* webacc disable          Disable a backend or a probe on a webaccelerator
* webacc enable           Enable a backend or a prove on a webaccelerator
* webacc info             Display information about a webaccelerator
* webacc list             List webaccelerators
* webacc probe            Manage a probe for a webaccelerator
* webacc update           Update a webaccelerator


Details:

* ``gandi account info`` display information about the hosting account currently in use.

* ``gandi api`` display information about the Gandi.net API.

* ``gandi certificate change-dcv resource``: Change the domain validation process for a specific certificate request. Mandatory option is ``--dcv-method TEXT`` where the method could be email, dns, file or auto.

* ``gandi certificate create``: Request the creation of a certificate. If a private key is present as ``--private-key`` and not a CSR, the CSR will be generated. If no CSR or private key are present in the parameters, both are generated. Possible options are ``--csr TEXT`` and ``--private-key TEXT`` which could be the content of a certificate request and a private key or path to the files, ``--country TEXT``, ``--state TEXT``, ``--city TEXT``, ``-organisation TEXT``, ``--branch TEXT`` to specify new administrative information, ``--duration INTEGER`` how many years of validity (up to 5 years), ``--package TEXT`` is the type of certificate as listed by ``gandi certificate package``, ``--package`` is now deprecated and should be replaced by ``--type``, ``--max-altname`` and ``--warranty``, ``--type`` is the certificate type in std (standard), bus (business) and pro, ``--max-altname`` is the maximum number of altnames that this multi domain certificate will be able to have (by default it's calculated on the number of ``--altnames`` param you have, but you can override it with a bigger value), ``--warranty`` is the value of the financial transaction under warranty (only appliable with Pro certificates), ``--altnames LIST`` is a list of all alternative names and ``--dcv-method TEXT`` where the method could be email, dns, file or auto.

* ``gandi certificate delete resource`` delete a certificate. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``). Note that a resource can be a cn entry or an integer id.

* ``gandi certificate follow resource`` display the current status of a certificate operation. Resource is an operation id.

* ``gandi certificate export resource`` write the selected certificate to a file. Possible option is ``--output TEXT`` for the path of the output file, ``--force`` overwrite any existing file, ``--intermediate`` will retrieve the needed intermediate certificates. Note that a resource can be a cn entry or an integer id.

* ``gandi certificate info resource`` show detailed view of a specific certificate. Possible options are ``--id``, ``--altnames``, ``--csr``, ``--cert`` which show the integer id, the alternative names, the certificate request and the full certificate, ``--all-status`` show the certificate without regard for its status. Note that a resource can be a cn entry or an integer id.

* ``gandi certificate list`` Possible options are ``--id``, ``--altnames``, ``--csr``, ``--cert`` which show the integer id, the alternative names, the certificate request and the full certificate for each element of the list, ``--all-status`` show certificates without regards to their status, ``--status``, ``--dates`` show the status of the certificate and the creation and expiration dates, ``--limit INTEGER`` show a subset of the list.

* ``gandi certificate packages`` show a full list of all available certificate types, this is deprecated, replace it by ``certificate plans``.

* ``gandi certificate plans`` show a full list of all available certificate plans.

* ``gandi certificate resend-dcv resource`` send the validation email again (only for the 'email' DCV method). Note that a resource can be a cn entry or an integer id.

* ``gandi certificate update resource`` modify the options of a certificate. Possible options are ``--csr TEXT``, ``--private-key TEXT`` could be either the content of a certificate request and a private key or a path to the files, ``--country TEXT``, ``--state TEXT``, ``--city TEXT``, ``--organisation TEXT``, ``--branch TEXT`` to specify new administrative information, ``--altnames LIST`` to change all the alternative names (comma separated text without space), ``--dcv-method TEXT`` with domain validation process method in email, dns, file, auto. Note that a resource can be a CN entry or an integer id.

* ``gandi certstore create`` create a new hosted certificate that will be associated to paas vhost or webaccs. Possible options are ``--private-key PK`` (or ``--pk``) to give the private key and ``--certificate CERT`` (or ``--crt``) to give the certificate (the certificate can also be given by its id with ``--certificate-id ID``.

* ``gandi certstore delete resource`` delete all hosted certificate corresponding to the resource (/!\ if you give an FQDN, it will delete all hosted certificate that correspond). Possible option is ``--force`` (or ``-f``) to continue deleting without asking.

* ``gandi certstore info resource`` show detailed view of hosted certificates corresponding to the resource.

* ``gandi certstore list`` list all the hosted certificates for this account. Possible options are ``--id`` to show the id, ``--vhosts`` to show the associated vhosts, ``--fqdns`` to show the fqdns contained in that certificate, ``--dates`` to show the create and expire dates and ``--limit`` to limit the number of elements in the list.

* ``gandi config key value`` configure value in the configuration file. With no option, configuration setting is stored in the local directory, which makes it suitable for code repositories. Using the ``-g`` flag, the change is stored in the global configuration file.

* ``gandi contact create`` create a new contact in interactive mode.

* ``gandi datacenters`` list all the datacenters of the Gandi.net platform. Possible option is ``--id`` to obtain the id of the datacenter. Most of the time you will be able to use the dc_code as parameter to the methods.

* ``gandi deploy`` deploy the remote git repository to the virtualhost setup on a Gandi Simple Hosting instance. Available options are ``--remote`` to specify the git remote to extract deploy url from, and ``--branch`` to specify the branch to deploy. By default, the command uses the ``gandi`` remote to extract deploy url, and deploys the ``master`` branch. In case the supplied remote is not a valid Simple Hosting git remote, the command will fallback to guessing the Simple Hosting remote from git configuration of the branch to deploy. Requires a Simple Hosting git remote attached to the current directory.

* ``gandi disk create`` create a new virtual disk. Possible options are ``--name TEXT`` for the label of the virtual disk (if not present, will be autogenerated), ``--size SIZE[M|G|T]`` for the new size of the disk, ``--datacenter FR-SD2|LU-BI1|FR-SD3`` for the geographical datacenter as listed by ``gandi datacenters``, ``--vm TEXT`` to attach the newly create virtual disk to an existing virtual machine instance, ``--snapshotprofile 1|2|3|7`` to select a profile of snapshot to apply to the disk for keeping multiple version of data in a timeline. ``--source TEXT`` to create a disk from another existing source e.g a disk, snapshot or from a public image as listed by ``gandi vm images``. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk delete resource`` delete a virtual disk identified as resource. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk info resource`` show a detailed view of a specific virtual disk identified as resource.

  ``gandi disk list`` show a list of virtual disk. Possible options to filter the list are : ``--only-data`` and ``--only-snapshot`` which limit the list to regular disk and to snapshots, ``--attached`` which limit the list to only attached disks, ``--detached`` which limit the list to only detached disks,``--type`` add the type of the virtual disk, ``--id`` add the integer id of each virtual disk, ``--vm`` show the virtual machines by which the disk are used, ``--snapshotprofile`` show the profile of data retention associated, ``--datacenter`` which filter the output according to disk datacenter location and ``--limit INTEGER`` show only a limit amount of disks.

* ``gandi disk update resource`` modify the options of a virtual disk. Possible options are ``--kernel KERNEL`` to setup or update disk kernel, ``--cmdline TEXT`` to change kernel cmdline, ``--name TEXT`` for the label of the virtual disk, ``--size [+]SIZE[M|G|T]`` for the new size of the disk, if optional + prefix is provided, size value will be added to current disk size, a size suffix (M for megabytes up to T for terabytes) is optional, megabytes is the default if no suffix is present, ``--snapshotprofile TEXT`` to select a profile of snapshot to apply to the disk for keeping multiple version of data in a timeline, ``--delete-snapshotprofile`` to remove snapshot profile associated to this virtual disk. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk attach disk vm`` attach the given disk to the given vm, if the disk is currently attached, it will start by detaching it. Possible options: ``--force`` to skip all questions about detaching and attaching; ``--position INTEGER`` (or ``-p``) to specify the position at which the disk should be attached (0 for system disk); ``--read-only`` (or ``-r``) to attach the disk in read-only mode. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk detach disk`` detach the disk from the vm it is currently attached. Possible option is ``--force`` to skip all questions about detaching. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk rollback resource`` will rollback a disk from a snapshot. This modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi disk migrate resource`` will migrate a disk from current disk datacenter to a new one. If multiple datacenters are available, the user will be prompted to select one. This modification can be done as background process using the option ``--background`` (or ``--bg``). Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi disk snapshot resource`` will create a snapshot on the fly from a disk. Possible option is ``--name TEXT`` for the name of the snapshot (if not present, will be autogenerated). The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi dnssec create`` will create a DNSSEC key for the domain ``domain.tld``. It taks 4 parameters, ``fqdn`` which is the domain for which we want to create the key and ``flag`` which is the flag to use for creation (ZSK or KSK) and ``algorithm`` for the choice of the algorithm for the key and the ``public_key`` in a base64 encoded form.

* ``gandi dnssec delete resource`` will remove a DNSSEC key identified by a resource identificator.

* ``gandi dnssec list domain.tld`` will list DNSSEC keys for domain ``domain.tld``.

* ``gandi docker`` will setup ssh forwarding towards a gandi VM, remotely feeding a docker unix socket. This, for example, can be used for zeroconf access to scripted temporary build VMs. The ``--vm`` option alters the ``dockervm`` configuration parameter and can be used to set the VM used for future docker connections. ``dockervm`` can also be set locally for per-project vms (See ``gandi config``). *NOTE*: passing option parameters to docker require the usage of the POSIX argument parsing ``--`` separator. *NOTE*: a local docker client is required for this command to operate.

* ``gandi dns create`` will creating a new DNS record entry for specific domain ``domain.tld``. It takes 4 parameters, ``FQDN`` which is the domain on which to add the record, ``NAME`` which is the record relative name, ``TYPE`` which is the record type, ``VALUE`` which is the record value. Multiple values can be provided for ``VALUE`` parameter. Possible options are ``--ttl INTEGER`` to set record time to live value in seconds.

* ``gandi dns delete`` will delete a DNS record entry. It takes 3 parameters, ``FQDN`` which is the domain on which to delete the record, ``NAME`` which is the record relative name to delete, ``TYPE`` which is the record type to delete. ``NAME`` and ``TYPE`` parameters are both optional to allow deletion of multiple record entries at once, you can either delete all ``NAME`` records or all records for a ``FQDN``. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi dns domain.list`` will list all domains registered in LiveDNS, and manageable by the ``gandi dns`` commands through Gandi REST API.

* ``gandi dns list domain.tld`` will display all records for domain ``domain.tld``. Possible parameters are ``NAME`` to filter records by name, ``RRSET_TYPE`` to filter records by type. Possible options are ``--sort [name|ttl|type|values]`` to sort results (does not work with ``--text`` option), ``--type [A|AAAA|CAA|CDS|CNAME|DNAME|DS|LOC|MX|NS|PTR|SPF|SRV|SSHFP|TLSA|TXT|WKS]`` to filter results by type (does not work with ``--text`` option), ``--text`` to output result in text format.

* ``gandi dns update domain.tld`` will update record entry for domain ``domain.tld``. It takes 4 parameters, ``FQDN`` which is the domain on which to add the record, ``NAME`` which is the record relative name, ``TYPE`` which is the record type, ``VALUE`` which is the record value. Multiple values can be provided for ``VALUE`` parameter. Possible options are ``--ttl INTEGER`` to set record time to live value in seconds and ``--file`` which will ignore other parameters and overwrite current zone content with provided file content.

* ``gandi dns keys create`` will create a new DNSKEY for a domain and have LiveDNS sign the zone for you. It takes 2 parameters, ``FQDN`` which is the domain for which we want to create the key and ``FLAG`` which is the flag value to use for creation.

* ``gandi dns keys delete`` will delete a DNSKEY of a domain. It takes 2 parameters, ``FQDN`` which is the domain using the key, ``KEY`` which the key uuid, retrieved by using ``gandi dns key list`` command. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi dns keys info`` will display information about a DNSKEY, including ``DS`` value for the key. It takes 2 parameters, ``FQDN`` which is the domain using the key, ``KEY`` which the key uuid, retrieved by using ``gandi dns keys list`` command.

* ``gandi dns keys list domain.tld`` will list all DNSKEY for domain ``domain.tld``.

* ``gandi dns keys recover`` will recover a deleted key for a domain. If you mistakenly delete a key and the DS if present at the registry, or still present in the caches, you can recover it. It takes 2 parameters, ``FQDN`` which is the domain using the key, ``KEY`` which the key uuid, retrieved by using ``gandi dns keys list`` command.

* ``gandi domain create domain.tld`` helps register a domain. Options are ``--domain domain.tld`` for the domain you want to get (/!\ this option is deprecated and will be removed upon next release), ``--duration INTEGER RANGE`` for the registration period, ``--owner TEXT``, ``--admin TEXT``, ``--tech TEXT``, ``--bill TEXT`` for the four contacts to pass to the creation process, ``--nameserver TEXT`` for adding custom nameservers, ``--extra_parameter XTRANAME XTRAVALUE`` for adding extra parameters (see http://doc.rpc.gandi.net/domain/reference.html#DomainExtraParameters). All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi domain renew domain.tld`` will renew a domain. Available option is ``--duration INTEGER RANGE`` for the registration period. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi domain info domain.tld`` show information about the specific domain ``domain.tld`` : owner, admin, billing and technical contacts, fully qualified domain name, nameservers, associated zone, associated tags and more.

* ``gandi domain list`` show all the domains in the Gandi account. Possible option is ``--limit INTEGER`` which will show a subset of the list.

* ``gandi forward create address@domain.tld`` create a new mail forward. Mandatory option is ``-d, --destination TEXT`` to define a forward destination for this domain mail, this option can be used multiple times.

* ``gandi forward delete address@domain.tld`` delete mail forward ``address@domain.tld``. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi forward list domain.tld`` show all existing mail forwards for specific domain ``domain.tld``. Possible option to filter the list: ``--limit INTEGER`` show only a limited amount of mail forwards.

* ``gandi forward update address@domain.tld`` update mail forward ``address@domain.tld``. Possible options are ``-a, --dest-add TEXT`` to add a forward destination for this mail forward, can be used multiple times, ``-d, --dest-del TEXT`` to delete a forward destination for this mail forward, can be used multiple times.

* ``gandi help command`` display help for command, if command is a namespace it will display list of available commands for this namespace.

* ``gandi ip list`` show all the ip created in Gandi hosting for the account. Possible options to filter the list are : ``--attached`` to only show attached ips, ``--detached`` to only show detached ips, ``--vlan`` to filter by vlan name, and ``--type`` (being in ``public`` or ``private``) to only show public or private ips. Possible options to get more details are : ``--version`` to get the ip version, ``--reverse`` to get the ip reverse, and ``--vm`` to get the attached vm if any, ``--id`` to add the integer id of each ip.

* ``gandi ip info`` show information about specific ip.

* ``gandi ip create`` create new ip. Possible options are ``--datacenter FR-SD2|LU-BI1|FR-SD3`` for the geographical datacenter as listed by ``gandi datacenters`` if ``--attach`` is specified this option is useless, ``--ip-version 4|6`` for version of created IP, ``--bandwidth INTEGER`` to set network bandwidth in bits/s on first network interface created, ``--vlan`` to specify which private vlan should be used, ``--ip`` to specify an ip in the vlan, ``--attach`` to attach this new ip to a vm, and ``--background`` (or ``--bg``) to process in background.

* ``gandi ip attach`` attach an ip to a vm. It takes two parameters, ``ip`` the wanted ip, and ``vm`` the vm to attach, ``ip`` the ip to attach. If the ip is already attached, it will be detached from the previous vm before being attached to the given one. Possible options are ``--force`` to bypass the validation question; useful in non-interactive mode when scripting, and ``--background`` (or ``--bg``) to process in background.

* ``gandi ip detach`` detach an ip from a vm. It only takes one parameter, the ``ip``. Possible options are ``--force`` to bypass the validation question; useful in non-interactive mode when scripting, and ``--background`` (or ``--bg``) to process in background.

* ``gandi ip delete`` delete one or more ips. If the ip is still attached, it will detach it before deleting it. Possible options are ``--force`` to bypass the validation question; useful in non-interactive mode when scripting, and ``--background`` (or ``--bg``) to process in background.

* ``gandi ip update`` update an ip. The only available parameter is now ``--reverse``, to specify a reverse (PTR record) name for this ip address.

* ``gandi mail create login@domain.tld`` create a new mailbox. Possible options are ``-q, --quota INTEGER`` to define a quota for this mailbox, ``-f, --fallback TEXT`` to define a fallback addresse, ``-a, --alias TEXT`` to add an alias for this mailbox, this option can be used multiple times, ``-p, --password TEXT`` to provide a password for this mailbox.

* ``gandi mail delete login@domain.tld`` delete mailbox ``login@domain.tld``. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi mail info login@domain.tld`` show information about mailbox ``login@domain.tld``.

* ``gandi mail list domain.tld`` show all existing mailboxes for specific domain ``domain.tld``.

* ``gandi mail purge login@domain.tld`` purge mailbox ``login@domain.tld``. Possible options are ``-a, --alias`` to purge all aliases on this mailbox, ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi mail update login@domain.tld`` update mailbox ``login@domain.tld``. Possible options are ``-p, --password`` will prompt for a new password for this mailbox, ``-q, --quota INTEGER`` to define a quota for this mailbox, ``-f, --fallback TEXT`` to define a fallback addresse, ``-a, --alias-add TEXT`` to add an alias for this mailbox, can be used multiple times, ``-d, --alias-del TEXT`` to delete an alias for this mailbox, can be used multiple times.

* ``gandi oper info id`` show information about the operation ``id``.

* ``gandi oper list`` show all the running operation on your product at Gandi (for example Simple Hosting, domain, hosting). Possible option is ``--limit INTEGER`` which list only a subset of the full list of running operations (default is 100), ``--step`` to filter on specific step possible values are: BILL, WAIT, RUN, ERROR (default to BILL, WAIT, RUN).

* ``gandi paas attach instance`` Add the Simple Hosting instance's vhost git remote to a local git repository. By default, the git remote's name is gandi; it can be overridden by using the ``--remote TEXT`` option.

* ``gandi paas clone instance`` clone all files of a remote virtual host, for a given Simple Hosting instance, to a local git repository. Override the default vhost by passing ``--vhost TEXT``. The destination directory to clone to can be overridden by using the ``--directory`` option. By default the origin name is set to gandi, it can be overridden with the ``--origin TEXT`` option.

* ``gandi paas console resource`` open a console to the SimpleHosting. Note that resource could be a full qualified domain name or an integer id.

* ``gandi paas create``: Create a Simple Hosting instance. Mandatory option is  ``--password TEXT`` for the password of the instance. Possible option are ``--name TEXT`` for the name of the instance (if not present, will be autogenerated), ``--size s|s+|m|x|xl|xxl`` for the size (amount of RAM and processes), ``--type TYPE`` for the type as listed by the ``gandi paas types`` command, ``--quantity INTEGER`` for the additional disk space, ``--duration TEXT`` for the number of month suffixed with 'm', ``--datacenter FR-SD2|LU-BI1|FR-SD3`` for the geographical datacenter as listed by ``gandi datacenters``, ``--vhosts TEXT`` for a list of virtual hosts to link to this instance, ``--ssl`` to activate SSL on all vhosts, ``--pk`` to give the private key used to generate the certificate if it's linked to the same account in certificate section, and ``--poll-cert`` to wait for certificate generation in case you want to get one with Gandi (certificate create can take some time to achieve), ``--snapshotprofile INTEGER`` for the snapshot profile for the disk of the instance, ``--delete-snapshotprofile`` to remove the snapshotprofile on the instance , ``--sshkey TEXT`` to specify a name of a SSH key. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas delete resource`` delete a Simple Hosting instance. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas info resource`` show details about a specific Simple Hosting instance. Possible option is ``--stat`` in order to get statistic of the cached pages (it's based on the last 24 hours).

* ``gandi paas list`` show all the Simple Hosting instances. Possible options are ``--state TEXT`` for filtering the output by a specific state, ``--id`` which display the integer identificator, ``--vhosts`` which show all the virtual hosts associated with each instances, ``--type`` which display the type of Simple Hosting and ``--limit INTEGER`` which show only a subset of the full Simple Hosting list (default is 100).

* ``gandi paas restart resource``: Restart a Simple Hosting instance. Possible option is ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi paas types`` show all the Simple Hosting type available. For example: phpmysql which provides PHP and MySQL or pythonmongodb which provides Python and MongoDB.

* ``gandi paas updates resource`` modify the options of a Simple Hosting. Possible options are ``--name TEXT`` which renames a instance, ``--size s|s+|m|x|xl|xxl`` to change the size of the instance, ``--quantity INTEGER`` to add disk space, ``--password`` to change the password of the instance, ``--sshkey TEXT`` to specify a name of a SSH key, ``--upgrade`` flag to upgrade the instance to the latest system image, ``--console TEXT`` to enable or disable the console, ``--snapshotprofile TEXT`` to set the snapshot profile for the disk of the instance, ``--reset-mysql-password TEXT`` to reset the root password of MySQLd running on the instance. All these modification can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi record create domain.tld`` will create new DNS zone record entry for specific domain ``domain.tld`` in a new zone version and activate it. Mandatory options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used, ``--name TEXT`` to set record relative name, may contains leading wildcard, use @ for empty name, ``--type A|AAAA|CNAME|MX|NS|TXT|WKS|SRV|LOC|SPF`` to set record type, ``--value TEXT`` to set record value, may contains up to 1024 ascii characters. Possible options are ``--ttl INTEGER`` to set record time to live value.

* ``gandi record delete domain.tld`` will delete DNS zone record entries for a specific domain ``domain.tld`` from a zone, and use a new zone version which will be activated after deletion. Mandatory options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used, ``--name TEXT`` to specify relative name of record to delete, may contains leading wildcard, use @ for empty name, ``--type A|AAAA|CNAME|MX|NS|TXT|WKS|SRV|LOC|SPF`` to specify record type, ``--value TEXT`` for record to delete value, may contains up to 1024 ascii characters.

* ``gandi record list domain.tld`` show the list of DNS zone records for specific domain ``domain.tld``. Possible options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used, ``--limit INTEGER`` show a subset of the list.

* ``gandi record update domain.tld`` will update DNS zone record entries for a specific domain ``domain.tld``. Mandatory options are ``--zone-id INTEGER`` to specify a zone id to use, if not provided default zone will be used. You can update an individual record using ``--record`` and ``--new-record`` parameters which both use the same format `'name TTL IN TYPE [A, AAAA, MX, TXT, SPF] value'`. Or you can use a plaintext file using ``--file FILENAME`` parameter to update all records of a DNS zone. Note that if you want to update an individual record and fail to provide all fields for ``--record`` parameter, it will try to retrieve the record entry using only the name, but if there are several records entries with the same name, only the first one will be updated.

* ``gandi setup`` initialize the configuration for the tool.

* ``gandi snapshotprofile info resource`` detail the information about a profile : frequency of snapshot and retention period.

* ``gandi snapshotprofile list`` show the list of all profile for virtual disk snapshot. Possible options are ``--only-paas`` and ``--only-vm`` to filter the output and show only the subset of profile for the Simple Hosting or the Gandi Hosting.

* ``gandi sshkey create --name label`` add a SSH key identified by ``label`` which could be used for authentication. Possible option are ``--value TEXT``  with the content of the SSH public key or ``--filename FILENAME`` with the path to a file containing the SSH public key.

* ``gandi sshkey delete resource`` remove a SSH key. Resource can be a name or the specific id.

* ``gandi sshkey info resource`` show details of an SSH key: name and fingeprint in MD5 hash. Possible option are ``--id`` which also show the id of theSSH key and ``--value`` which show the content of the SSH key.

* ``gandi sshkey list`` show all the SSH keys registered. Possible option are ``--id`` which add numeric identificator and ``--limit INTEGER`` which show only a subset of the SSH keys.

* ``gandi status`` shows the current status for all services as seen on status.gandi.net. Possible option is to provide a service name to the command to retrieve only the status of this service.

* ``gandi vhost create virtualhost.domain.tld`` adds a virtual host. Use the mandatory option ``--paas TEXT`` to specify the Simple Hosting instance on which it will create the virtual host, ``--alter-zone`` will update the domain zone, ``--ssl`` to activate SSL on that host, ``--pk`` to give the private key used to generate the certificate if it's linked to the same account in certificate section, and ``--poll-cert`` to wait for certificate generation in case you want to get one with Gandi (certificate create can take some time to achieve). Creation can be done as background process using the option ``--background`` (or ``--bg``) it will have no effet on the certificate creation process.

* ``gandi vhost delete host.domain.tld`` delete a virtual host after asking for user validation. Possible option is ``--force`` to bypass the validation question; useful in non-interactive mode when scripting. Deletion can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vhost info host.domain.tld`` show details about a specific virtual host. Possible option is ``--ids`` which show the integer identificator.

* ``gandi vhost list`` show all the virtual host defined in Simple Hosting. Possible option are ``--names`` which add the name of the Simple Hosting instance on which the virtual host is setup, ``--ids`` which show the integer identificator and ``--limit INTEGER`` which show a subset of the full list of virtual host.

* ``gandi vhost update host.domain.tld``: Activate SSL on this host. Possible options are ``--ssl`` to activate SSL on that host, ``--pk`` to give the private key used to generate the certificate if it's linked to the same account in certificate section, and ``--poll-cert`` to wait for certificate generation in case you want to get one with Gandi (certificate create can take some time to achieve).

* ``gandi vlan create`` add a new vlan. Mandatory options are ``--name TEXT`` for the label of the vlan, ``--datacenter FR-SD2|US-BA1|LU-SD1`` for the geographical datacenter as listed by ``gandi datacenters``. Possible options are ``--subnet`` to set a subnet and ``--gateway`` to set the gateway. The operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vlan delete resource`` delete a vlan after asking for user validation. Possible option is ``--force`` to bypass the validation question; useful in non-interactive mode when scripting. Deletion can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vlan info resource`` show details of a specific vlan.

* ``gandi vlan list`` show all the vlan created in Gandi hosting for the account. Possible options are ``--id`` to obtain the id of each vlan, ``--datacenter FR-SD2|LU-BI1|FR-SD3`` which filter by geograhical datacenter.

* ``gandi vlan update`` update a vlan. Mandatory options are ``--name TEXT`` for the label of the vlan.

* ``gandi vm console resource`` open a console on the virtual machine and give you a shell access.

* ``gandi vm create`` create a new virtual machine. Possible options are ``--hostname TEXT`` for the hostname of the machine (if not present, will be autogenerated), ``--datacenter FR-SD2|US-BA1|LU-SD1`` for the geographical datacenter as listed by ``gandi datacenters``, ``--memory INTEGER`` for quantity of memory, ``--cores INTEGER`` for number of virtual CPU, ``--ip-version 4|6`` for version of created IP, it can be omitted if ``--vlan`` is given, ``--vlan`` to set the vm on the specified vlan and ``--ip`` to set the ip in that vlan, ``--bandwidth INTEGER`` to set network bandwidth in bits/s on first network interface created, ``--login TEXT`` to define login to created on virtual machine, ``--image TEXT`` for the disk image to be used to boot the virtual machine as listed by ``gandi vm images``, ``--sshkey TEXT`` to specify name of a SSH key, ``--password`` will prompt for a password to set for the created login, ``--run TEXT`` to specify shell command that will run at the first boot of virtual machine. The operation can be done as background process using the option ``--background`` (or ``--bg``). You can specify the virtual machine system disk size with the ``--size`` parameter (unit MiB). If not run in background, this command will spawn an ssh session to the created virtual machine. You can use the ``--script`` option to upload, then run a script on the VM after creation. Be sure to provide an executable file as an argument to the ``--script`` option. The ``--script-args TEXT`` optional argument allows you to complete script invocation with arguments. You can open a ssh session to the virtual machine after creation by using ``--ssh`` parameter. The ``--gen-password`` optional argument will generate a random password to be set for the root account, and the created login if needed, the password will be displayed during the creation.

* ``gandi vm delete resource`` destroy a virtual machine, its main disk and its first virtual network interface. This operation can be done as background process using the option ``--background`` (or ``--bg``). Another possible parameter is ``--force`` to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi vm images pattern`` list all the available images of system whose name contains the pattern. Possible option is ``--datacenter FR-SD2|LU-BI1|FR-SD3`` which filter by geograhical datacenter.

* ``gandi vm kernel pattern`` list all the available kernels whos name contains the pattern. Possible options are ``--flavor TEXT`` to filter given kernel flavors, ``--vm TEXT`` to only show kernels available for a given vm, ``--datacenter FR-SD2|LU-BI1|FR-SD3`` to specify a given datacenter.

* ``gandi vm list`` show all the virtual machine created in Gandi hosting for the account. Possible options are ``--state`` which filter the output according to define virtual machine state, ``--datacenter`` which filter the output according to virtual machine datacenter, ``--id`` to obtain the id of each virtual machine, ``--limit INTEGER`` which list only a subset of the full list of virtual machines.

* ``gandi vm migrate resource`` will migrate a virtual machine from current datacenter to a new one. This modification can be done as background process using the option ``--background`` (or ``--bg``). Possible option is ``--finalize`` to finalize migration when migration process requires this action, ``--force`` (or ``-f``) to bypass the validation question; useful in non-interactive mode when scripting.

* ``gandi vm info resource`` show details of a specific operation. Use ``--stat`` in order to get general statistics of the VM's resources.

* ``gandi vm ssh resource [args]`` open a ssh connection on the virtual machine and give you a shell access. The ``-i TEXT`` option (or ``--identity TEXT``) refers to a local ssh key, as used in the ssh command. The ``-l TEXT``, ``--login TEXT`` or ``user@host`` form specifies remote username in the same way. Using ``--wipe-key``, previous entry for that host is discarded from the known_hosts file first. Using ``--wait`` parameter, the command will wait for sshd to spin up on virtual machine before trying to open a ssh connection. You can add arguments (be sure to prefix options with the POSIX argument parsing ``--`` separator) and commands to ssh, as used in the ssh command.

* ``gandi vm start resource``: Start a virtual machine (a resource can either be a hostname as defined in the creation process or the id of the virtual machine). This operation can be done as background process using the option ``--background`` (or ``--bg``).

* ``gandi vm stop resource``, same parameter as start but instead stops the virtual machine. Obviously.

* ``gandi vm reboot resource``, same parameter as start but instead reboots a virtual machine.

* ``gandi vm update resource``: Change the quantity of memory (using ``--memory INTEGER``), the number of virtual CPU (using ``--cores INTEGER``), enable the virtual console which gets a shell to the virtual machine even without network interfaces on the virtual machine (using ``--console``) or change the root password (using ``--password``). All these modification can be done as background process using the option ``--background`` (or ``--bg``). *NOTE*: Because of the cost of page table setup, a maximum memory limit has to be given for some kernels, limiting dynamic updates. You cannot online resize a VM memory crossing this value, and the ``--reboot`` option allows you to acknowledge the required reboot.

* ``gandi webacc add resource`` add a backend or a vhost on a webaccelerator. Possible options are ``--vhost TEXT`` to add the fully qualified domain name (FQDN like host.domain.tld) to the webaccelerator, can be used multiple times, ``--backend TEXT`` to specify an IP address, can be used multiple times, using format ip[:port], ``--port INTEGER`` to set a default port value for backend parameters if not specified in backend format, ``--ssl`` to activate ssl for vhost, ``--private-key TEXT`` to provide the private key used to generate the ssl certificate, ``--zone-alter`` to alter and activate zone file if Gandi DNS are used for the domain, ``--poll-cert`` will wait for the certificate creation to be finished, be warned that this can take a long time.

* ``gandi webacc create NAME`` create a new webaccelerator. Mandatory options are ``--datacenter FR-SD2|LU-BI1|FR-SD3`` for the geographical datacenter as listed by ``gandi datacenters`` where the webaccelerator will be created. Possible options are ``--backend TEXT`` to specify an IP address, can be used multiple times, using format ip[:port], ``--port INTEGER`` to set a default port value for backend parameters if not specified in backend format, ``--vhost TEXT`` to add the fully qualified domain name (FQDN like host.domain.tld) to the webaccelerator, can be used multiple times, ``--ssl`` to activate ssl for vhost, ``--private-key TEXT`` to provide the private key used to generate the ssl certificate, ``--zone-alter`` to alter and activate zone file if Gandi DNS are used for the domain, ``--poll-cert`` will wait for the certificate creation to be finished, be warned that this can take a long time, ``--ssl-enable`` to activate SSL support on the webaccelerator, ``--algorithm [client-ip, round-robin]`` to choose the loadbalancer algorithm defaulting to ``client-ip``.

* ``gandi webacc delete`` delete a webaccelerator, a vhost or a backend. Possible options are ``--webacc TEXT`` to specify the webaccelerator name to be deleted, ``--backend TEXT`` to specify an IP address to be deleted, can be used multiple times, using format ip[:port], ``--port INTEGER`` to set a default port value for backend parameters if not specified in backend format, ``--vhost TEXT`` to remove the fully qualified domain name (FQDN like host.domain.tld) from the webaccelerator, can be used multiple times.

* ``gandi webacc disable`` disable a backend or a probe on a webaccelerator. Possible options are ``--backend TEXT`` to specify an IP address to be disabled, can be used multiple times, using format ip[:port], ``--port INTEGER`` to set a default port value for backend parameters if not specified in backend format, ``--probe`` to disable probe for the webaccelerator, requires the webaccelerator name to be passed to the command.

* ``gandi webacc enable`` enable a backend or a probe on a webaccelerator. Possible options are ``--backend TEXT`` to specify an IP address to be enabled, can be used multiple times, using format ip[:port], ``--port INTEGER`` to set a default port value for backend parameters if not specified in backend format, ``--probe`` to enable probe for the webaccelerator, requires the webaccelerator name to be passed to the command.

* ``gandi webacc info resource`` display information about a webaccelerator. Possible options are ``--format [json, pretty-json]`` to specify output format to be used.

* ``gandi webacc list`` show all the webaccelerators. Possible options are ``--limit INTEGER`` which shows only a subset of the webaccelerators list, ``--format [json, pretty-json]`` to specify output format to be used.

* ``gandi webacc probe resource`` manage a probe for a webaccelerator. Possible options are ``--enable`` to enable the probe on the webaccelerator, ``--disable`` to disable the probe on the webaccelerator, ``--host TEXT`` to set the host value for testing the probe, ``--test`` to test the probe on the webaccelerator, ``--interval INTEGER`` to set interval for the probe to be checked, ``--url TEXT`` to set the probe url in the virtual host, ``--window INTEGER`` to set total number of probes to consider health decision, ``--threshold INTEGER`` to set number of probes to consider in the window, ``--timeout INTEGER`` to set the timeout in seconds, ``--http-method [GET, POST, PUT, DELETE, OPTIONS]`` to set HTTP method used for the probe check, ``--http-response INTEGER`` to set HTTP response code expected by the probe

* ``gandi webacc update resource`` update a webaccelerator.  Possible options are ``--name TEXT`` to change the name of the webaccelerator, ``--algorithm [client-ip, round-robin]`` to change the loadbalancer algorithm, ``--ssl-enable`` to activate SSL support on the webaccelerator, ``--ssl-disable`` to deactivate SSL support on the webaccelerator.


ENVIRONMENT
===========

`API_ENV`
    Switch between environment: the production API and the OT&E one.

    Example:

        API_ENV=production gandi domain list

`API_HOST`
    Specify a HTTP URL to connect and to send the API commands.

`API_KEY`
    Specify an API key for the chosen environment. This option is useful when you work with multiple account.

`APIREST_KEY`
    Specify a REST API key for the chosen environment. This option is useful when you work with multiple account.

`GANDI_CONFIG`
    Override the global configuration file.

FILES
=====

`$HOME/.config/gandi/config.yaml`
    Configuration file, overridden by the GANDI_CONFIG environment variable as described above.

AUTHORS
=======

Originaly created by Dejan Filipovic for Gandi S.A.S.
Copyright (c) 2014-2018 - Gandi S.A.S

CONTRIBUTORS
============

* Alexandre Solleiro <alexandre.solleiro@gandi.net>
* Ben Finney <ben+gandi@benfinney.id.au>
* Dejan Filipovic <sayoun@gandi.net>
* Guillaume Gauvrit <guillaume.gauvrit@gandi.net>
* Nicolas Chipaux <aegiap@gandi.net>
* Olivier Roussy <olivier@gandi.net>

VERSION
=======

This is Gandi-cli version 1.6.

CHANGELOG
=========

See CHANGES.rst in the project directory or in the documentation directory of your system. For Debian, the CHANGES file will be in /usr/share/doc/gandicli/.

TODO
====

Add missing Gandi product like ``virtual network interface`` or ``private vlan``.

BUGS
====

Please report any bugs or issue on https://github.com/Gandi/gandi.cli by opening an issue using this form https://github.com/Gandi/gandi.cli/issues/new. You can send patches by email to feedback@gandi.net.
