Changelog
=========

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
