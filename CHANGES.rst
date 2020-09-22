Changelog
=========

1.6
---
* Fixes #289: Spelling errors in manual page
* Gandi change its documentation URL
* Update status command to use statuspage in place of bahobab
* Fix type issue with click >= 7.1

1.5
---
* Fixes #280: Problem with new record
* Fixes #284: Manpage errors
* Fixes #287: Problem with dnssec create with algorithm/flags

1.4
---
* Fixes #268: Drop support of click < 7.0
* Drop support of python 2.6 and 3.3
* Add coverage
* Test python 3.7 and pypy in travis
* PEP8

1.3
---

* Use pytest instead of nose
* Add extra parameter in domain create
* Add support of Python 3.7
* Fixes #245: Add support of DNSSEC
* Fixes #250: Drop support of Python < 3.3

1.2
---

* Add support for paas size s+ for creation/update
* Fixes #232: Update 'gandi record update' command to allow filtering by name
* Fix bug when attempting to migrate a vm which cannot be migrated
* Only display DC closed warning if a date is set

1.1
---

* FR-SD5 is now the default datacenter.
* Add new 'gandi dns update' command.
* Fixes #228: Generate a user password at the creation of a VM
* Improve wait for ssh connectivity after 'gandi vm create' command to handle ipv6
* Fix a bug with 'gandi disk migrate' command not working with multiple datacenters choices
* Improve documentation for generating username/apikey with Gandi V5

1.0
----

* New 'dns' namespace to manage DNS records/dnssec through LiveDNS API.
* Add new 'gandi vm migrate' command.
* Refactor internal click code usage. Remove hackish code to handle
  nested commands which was limited to only 1 nested level.
  - This change will break code of users which were using custom commands
    on top of Gandi CLI, To fix this you have to use the proper click syntax
    to declare a new group for your commands.
  - This change also remove the automatic listing of all namespace commands
    upon a typo or unknown/wrong command.
* Fixes #224: DeprecationWarning makes tests fail with python 3.6.2

0.22
----

* Fixes #223: 'gandi setup' command error
* Fixes #222: AttributeError during vm creation on a private vlan
* Fixes tests for 'gandi deploy' and 'gandi status' commands

0.21
----

* Add new 'gandi disk migrate' command
* Update 'gandi setup' command to ask for apikey for REST API
* Handle deprecated images
  - Add a warning during 'gandi vm create' command
  - Display a * before image labels on 'gandi vm create' help
  - Display a /!\ DEPRECATED on 'gandi vm images' command
* Fixes #220: gandi record update issues
  - Do not cast to int the id of the record, use the retrieve value
  - Handle both record syntax with 'IN' or not when parsing
  - Delete created zone if record.update call fail from xmlrpc API
* Fixes #219: Can't remove disk snapshot profile
* vm: delete: Fix delete when we reach the list limit
  - Fixed a bug when deleting a vm that wasn't listed in the first 500 results
    of gandi.iaas.list.
* Fix issue when updating disk kernel with a kernel from another datacenter
  - CLI was proposing only kernels available on datacenter 1, but some kernels
    are available only on other datacenters, so we list everything for --kernel
    parameters, and for disk update command we add a new check if this kernel is
    available for this disk on this datacenter.
* Add epilog to help messages to notify user about man documentation
* Add one new verbose level for dumping data

0.20
----

* Add support for python3.6
* Debian 8 is the new default VM image
* FR-SD3 is the new default datacenter
* Update 'gandi mail create' command to allow passing password as parameter
* Update 'gandi certificate create' command: duration is now limited to 2 years
* Update 'gandi ip create' command to fix bad units in help message
* Fixes #182: 'gandi disk create' will detect datacenter when creating a new VM disk
* Fixes #184: 'gandi disk list' can now filter for attach/detach state
* Fixes #192: 'gandi certificate info' now still works after 500 certificates
* Fixes #201: 'gandi certificate export' was duplicating intermediate certificate
* Fixes #211: 'gandi paas deploy' tests should work again when using git commands
* Fixes a bug with options not using corrected value when deprecated
* Update unixpipe module to remove usage of posix and non portable imports

0.19
----

* Update create commands for namespaces: vm, paas, ip, disk, vlan, webacc
  to handle new datacenter status:
  - prevent using a closed datacenter for creation
  - display a warning when using a datacenter which will be closed
    in the future
* Update 'gandi mailbox info' command: aliases are now sorted
* Fixes #178: 'gandi account info' command now display prepaid amount
* Fixes #185: 'gandi domain create' command can now change nameservers
* Fixes #187: 'gandi record list' command has a --limit parameter
* Fixes #188: broken links in README
* Fixes certificate unittest for python3

0.18
----

* Update 'gandi paas update' command: --upgrade parameter is now a boolean flag
* Update 'gandi deploy' command:
  - new '--remote' and '--branch' options
  - better handling of case when git configuration is not configured as expected
  - will try and use the gandi remote by default to extract deploy url
  - will deploy the branch master by default
  - will fallback to guessing the Simple Hosting remote from git configuration
    of the branch to deploy
  - improve error message when unable to execute
* Update VM spin up timeout to 5min (from 2min) for bigger VM.
* Add more unittests.

0.17
----

* Gandi CLI now supports python3.5
* Update 'gandi paas' namespace:
  - Add new command 'gandi paas attach' to add an instance vhost's git
    remote to local git repository.
  - Update 'gandi deploy' command:
    - don't need a local configuration file anymore
    - need to be called on attached paas instance
  - Update 'gandi paas clone' command:
    - you can now specify which vhost and local directory to use
  - Use correct prefix for name generation in create command
* Convert 'gandi config' command to a namespace to allow configuration
  display and edition
* Fixes bug with 'gandi account' command which was broken sometimes
* Fixes a bug with 'gandi vlan update' command when using --create flag
* Fixes a bug with mail alias update when using same number of alias
  add/del parameters.
* Fixes a bug when using a resource name and having more than 100 items of
  this resource type
* Fixes size parameter choices for 'gandi paas create' command.
* Fixes bug with 'gandi record update' command and argument parsing
* Fixes bug with 'gandi record' commands:
  - must always exit if wrong/missing input parameter.
* Always display CLI full help message when requesting an unknown command
* Be less aggressive when trying to connect via SSH during 'gandi vm create'
* Better handling of no hosting credits error.
* Add more unittests.
* Fixes #108
* Fixes #128
* Fixes #140
* Fixes #157
* Fixes #161
* Fixes #165
* Fixes #170
* Fixes #173

0.16
----

* Update parameter '--datacenter':
    - allow dc_code as optional value
    - old values: FR/LU/US are still working so it doesn't break
      compatibility but they will be deprecated in next releases
* Update output of IP creation to display IP address:
    - for 'gandi ip create' command
    - for 'gandi vm create' command with --ip option
* Various improvements to modules for library usage:
    - datacenter
    - account
    - domain
    - operations
* Update 'gandi mail info' command:
    - change output of responder and quota information
      to be more user friendly
* Update click requirement version to >= 3.1 so we always use the
  latest version
* Fixes debian python3 packaging
* Fixes #148
* Fixes #147

0.15
----

* New command 'gandi domain renew' command to renew a domain.
* Update 'domain info' command:
    - add creation, update and expiration date to output
    - changes nameservers and services output for easier parsing
* Update 'gandi domain create' command:
    - the domain name can now be passed as argument, the option
    --domain will be deprecated upon next release.
* Update 'gandi disk update' command:
    - add new option '--delete-snapshotprofile' to remove a snapshot
      profile from disk
* Update 'gandi ip delete' command:
    - now accept multiple IP as argument in order to delete a list
      of IP addresses
* Fixes #119
* Fixes #129
* Fixes #141

0.14
----

* New 'certstore' namespace to manage certificates in webaccs.
* New command 'gandi vhost update' to activate ssl on the vhost.
* Update 'gandi vhost create' and 'gandi vhost update' commands
  to handle hosted certificates.
* Update 'gandi paas create' command to handle hosted certificates.
* Update 'gandi webacc create' and add to handle hosted certificates.
* Update 'gandi paas info' command:
    - add new --stat parameter, which will display cached page statistic
      based on the last 24 hours.
    - add snapshotprofile information to output.
* Update 'gandi oper list' command to add filter on step type.
* Update 'gandi paas update' command to allow deleting an existing
  snapshotprofile.
* Update 'gandi status' command to also display current incidents not
  attached to a specific service.
* Fixes #132
* Fixes #131
* Fixes #130
* Fixes #120
* Fixes error message when API is not reachable.

0.13
----

* New 'webacc' namespace for managing web accelerators for virtual machines.
* New command 'gandi status' to display Gandi services statuses.
* New command 'gandi ip update' to update reverse (PTR record)
* Update 'gandi vm create' command to add new parameter --ssh to open a SSH
  session to the machine after creation is complete. This means that the
  previous behavior is changed and vm creation will not automatically open a
  session anymore.
* Update several commands with statistics information:
    - add disk quota usage in 'gandi paas info' command
    - add disk network and vm network stats in 'gandi vm info' command
* Update 'gandi account info' command to display credit usage per hour
* Update 'gandi certificate update' command to displays how to follow and
  retrieve the certificate after completing the process.
* Update 'gandi ip info' command to display reverse information
* Update 'gandi ip list' command to add vlan filtering
* Update 'gandi vm list' command to add datacenter filtering
* Update 'gandi vm create' command to allow usage of a size suffix for
  --size parameter (as in disk commands)
* Update 'gandi vm ssh' command to add new parameter --wait to wait for
* Update 'certificate' namespace:
    - 'gandi certificate follow' command to know in which step of the process
       is the current operation
    - 'gandi certificate packages' display has been enhanced
    - 'gandi certificate create' will try to guess the number of altnames
       or wildcard
    - 'gandi certificate export' will retrieve the correct intermediate
       certificate.
* Update 'gandi disk attach' command to enable mounting in read-only and also
  specify position where disk should be attached.
* Update 'gandi record list' command with new parameter --format
* Update 'gandi record update' command to update only one record in the zone
  file
* Update 'gandi vm list' command to add datacenter filtering
* Refactor code for 'gandi ip attach' and 'gandi ip delete' commands
  virtual machine sshd to come up (timeout 2min).
* Refactor 'gandi vm create' command to pass the script directly to the API
  and not use scp manually after creation.
* Fixes wording and various typos in documentation and help pages.
* Add more unittests.
* Add tox and httpretty to tests packages requirements for unittests


0.12
----

* New 'ip' namespace with commands for managing public/private ip resources.
* New 'vlan' namespace with commands for managing vlans for virtual machines.
* New command 'gandi account info' to display information about credits
  amount for hosting account.
* New command 'gandi contact create' to create a new contact.
* New command 'gandi disk snapshot' to create a disk snapshot on the fly.
* Update 'gandi vm create' command:
    - enabling creation of vlan and ip assignment for this vlan directly
      during vm creation.
    - enabling creation of a private only ip virtual machine.
    - parameter --ip-version is not read from configuration file anymore,
      still defaulting to 4.
* Update 'gandi paas create' command to allow again the use of password provided
  on the command line.
* Update 'record' namespace to add delete/update commands, with option to export
  zones to file.
* Use different prefix for temporary names based on type of resource.
* Switch to use HVM image as default disk image when creating virtual machine.
* Add kernel information to output of 'gandi disk list' command.
* Fixes bug with paas vhost directory creation.
* Fixes bug with 'gandi mail delete' command raising a traceback.
* Fixes bug with duplicates entries in commands accepting multiple resources.
* Fixes various typos in documentation and help pages.
* Add first batch of unittests.


0.11
----

* New command 'gandi disk detach' to detach disks from
  currently attached vm.
* New command 'gandi disk attach' to attach disk to a
  vm.
* New command 'gandi disk rollback' to perform a rollback
  from a snapshot.
* New parameter --source for command 'gandi disk create'
  to allow creation of a new disk from an existing disk
  or snapshot.
* New parameter --script for command 'gandi vm create'
  to allow upload of a local script on freshly created vm
  to be run after creation is completed.
* Update parameter --size of 'gandi disk create/update'
  command to accept optionnal suffix: M,G,T (from megabytes
  up to terabytes).
* Update command 'gandi vm ssh' to accept args to be passed
  to launched ssh command.
* Fixes bug with 'gandi vm create' command and image
  parameter, which failed when having more than 100 disks
  in account.
* Fixes bug with 'gandi paas info' command to display
  sftp_server url.
* Fixes bug with 'gandi record list' command when requesting
  a domain not managed at Gandi.
* Rename --sshkey parameter of 'gandi sshkey create' command
  to --filename.
* Prettify output of list/info commands.
* GANDI_CONFIG environment variable can be used to override
  the global configuration file.
* Bump click requirement version to <= 4.


0.10
----

* Add new dependency to request library, for certificate
  validation during xmlrpc calls.
* New command 'gandi vm kernels' to list available kernels,
  can also be used to filter by vm to know which kernel is
  compatible.
* New parameters --cmdline and --kernels for command
  'gandi disk update' to enable updating of cmdline
  and/or kernel.
* New parameter --size for command 'gandi vm create'
  to specify disk size during vm creation.
* Handle max_memory setting in command 'gandi vm update'
  when updating memory. New parameter --reboot added to
  accept a VM reboot for non-live update.
* Update command 'gandi vm images' to also display usable
  disks as image for vm creation.
* Security: validate server certificate using request as
  xmlrpc transport.
* Security: restrict configuration file rights to owner only.
* Refactor code of custom parameters, to only query API when
  needed, improving overall speed of all commands.
* Fixes bug with sshkey parameter for 'gandi paas create'
  and 'gandi paas update' commands.
* When an API call fail, we can call again using dry-run flag
  to get more explicit errors. Used by 'gandi vhost create'
  command.
* Allow Gandi CLI to load custom modules using
  'GANDICLI_PATH' environment variable, was previously only
  done by commands.


0.9
---

* New command 'gandi docker' to manage docker instance.
  This requires a docker client to work.
* Improve 'vm ssh' command to support identity file, login@
  syntax.
* Login is no longer a mandatory option and saved to configuration
  when creating a virtual machine.
* Add short summary to output when creating a virtual machine.
* Fixes bug when no sshkey available during setup.
* Fixes bug with parameters validation when calling a command
  before having entered api credentials.

0.8
---

* New record namespace to manage domain zone record entries

0.7
---

* Add and update License information to use GPL-3
* Uniformize help strings during creation/deletion commands

0.6
---

* New mail namespace for managing mailboxes and aliases
* New command 'disk create' to create a virtual disk
* New command 'vm ssh' to open a ssh connection to an existing
  virtual machine
* New command 'help' which behave like --help option.
* Using 'gandi namespace' without full command will display list
  of available commands for this namespace and associated short help.
* 'gandi paas create' and 'gandi vm create' commands now use sshkeys,
  and default to LU as default datacenter.

0.5
---

* Fixes Debian packaging


0.4
---

* Fixes bug with snapshotprofile list command preventing
  'gandi setup' to work after clean installation
* Allow Gandi CLI to load custom modules/commands using
  'GANDICLI_PATH' environment variable

0.3
---

* New certificate namespace for managing certificates
* New disk namespace for managing iaas disks
* New snapshotprofile namespace to know which profiles exists
* Allow override of configuration values for apikey, apienv and apihost
  using shell environment variables API_KEY, API_ENV, API_HOST.
* Bugfixes on various vm and paas commands
* Fixes typos in docstrings
* Update man page

0.2
---

* New vhost namespace for managing virtual host for PaaS instances
* New sshkey namespace for managing a sshkey keyring
* Bugfixes on various vm and paas commands
* Bugfixes when using a hostname using only numbers
* Added a random unique name generated for temporary VM and PaaS


0.1
---

* Initial release
