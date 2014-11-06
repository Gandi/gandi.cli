Changelog
=========


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
  ftp_server url.
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
