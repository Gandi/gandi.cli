Changelog
=========

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
