
import os
import uuid
from gandi.cli.core.conf import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Vhost(GandiModule):

    @classmethod
    def list(cls, options=None):
        """list virtual hosts"""

        if not options:
            options = {}

        return cls.call('paas.vhost.list', options)


class Paas(GandiModule):

    @classmethod
    def type_list(cls, options={}):
        """list type of Paas instances"""

        return cls.call('paas.type.list', options)

    @classmethod
    def list(cls, options):
        """list Paas instances"""

        return cls.call('paas.list', options)

    @classmethod
    def info(cls, id):
        """display information about a Paas instance"""

        return cls.call('paas.info', cls.usable_id(id))

    @classmethod
    def delete(cls, id, interactive=False):
        """delete a Paas instance"""

        result = cls.call('paas.delete', cls.usable_id(id))
        if not interactive:
            return result

        # interactive mode, run a progress bar
        cls.echo("Delete your Paas instance.")
        cls.display_progress(result)

    @classmethod
    def update(cls, id, name, size, quantity, password, ssh_key, upgrade,
               console, snapshot_profile, reset_mysql_password, interactive):
        """update a Paas instance"""

        if interactive and not cls.intty():
            interactive = False

        paas_params = {}

        if name is not None:
            paas_params['name'] = name

        if size is not None:
            paas_params['size'] = size

        if quantity is not None:
            paas_params['quantity'] = quantity

        if password is not None:
            paas_params['password'] = password

        ssh_key_ = ssh_key or cls.get('ssh_key')
        if ssh_key_ is not None:
            with open(ssh_key_) as fdesc:
                ssh_key_ = fdesc.read()
            if ssh_key_ is not None:
                paas_params['ssh_key'] = ssh_key_

        if upgrade is not None:
            paas_params['upgrade'] = upgrade

        if console is not None:
            paas_params['console'] = console

        if snapshot_profile is not None:
            paas_params['snapshot_profile'] = snapshot_profile

        if reset_mysql_password is not None:
            paas_params['reset_mysql_password'] = reset_mysql_password

        result = cls.call('paas.update', cls.usable_id(id), paas_params)
        if not interactive:
            return result

        # interactive mode, run a progress bar
        cls.echo("Updating your Paas instance.")
        cls.display_progress(result)

    @classmethod
    def create(cls, name, size, type, quantity, duration, datacenter, vhosts,
               password, snapshot_profile, interactive, ssh_key):
        """create a new PaaS instance.

        you can specify a configuration entry named 'ssh_key' containing
        path to your ssh_key file

        >>> gandi config -g ssh_key ~/.ssh/id_rsa.pub

        """

        if interactive and not cls.intty():
            interactive = False

        datacenter_id_ = int(Datacenter.usable_id(datacenter))

        paas_params = {
            'name': name,
            'size': size,
            'type': type,
            'password': password,
            'duration': duration,
            'datacenter_id': datacenter_id_,
        }
        # generate a default vhost value
        if not vhosts:
            digest = uuid.uuid4().hex[:10]
            vhosts = ['%s.url-de-test.ws' % digest]
        paas_params['vhosts'] = vhosts

        if quantity is not None:
            paas_params['quantity'] = quantity

        ssh_key_ = ssh_key or cls.get('ssh_key')
        if ssh_key_ is not None:
            with open(ssh_key_) as fdesc:
                ssh_key_ = fdesc.read()
            if ssh_key_ is not None:
                paas_params['ssh_key'] = ssh_key_

        if snapshot_profile is not None:
            paas_params['snapshot_profile'] = snapshot_profile

        result = cls.call('paas.create', paas_params)
        if not interactive:
            return result

        # interactive mode, run a progress bar
        cls.echo("We're creating your PaaS instance.")
        cls.display_progress(result)
        cls.echo('Your PaaS %s have been created.' % name)

    @classmethod
    def init_conf(cls, id):
        """ Initialize local configuration with PaaS information. """

        paas = Paas.info(cls.usable_id(id))
        if paas['vhosts']:
            vhost = paas['vhosts'][0]['name']
        else:
            vhost = 'default'

        if 'php' not in paas['type']:
            vhost = 'default'

        cls.debug('save PaaS instance information to local configuration')

        git_server = paas['git_server']
        # hack for dev
        if 'dev' in paas['console']:
            git_server = 'git.hosting.dev.gandi.net'
        paas_access = '%s@%s' % (paas['user'], git_server)
        cls.shell('git clone ssh+git://%s/%s.git' % (paas_access, vhost))
        # go into directory to save configuration file in this directory
        os.chdir(os.getcwd() + ('/%s' % vhost))
        cls.configure(False, 'paas.user', paas['user'])
        cls.configure(False, 'paas.name', paas['name'])
        cls.configure(False, 'paas.deploy_git_host', '%s.git' % vhost)
        cls.configure(False, 'paas.access', paas_access)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a hostname
            qry_id = cls.from_hostname(id)
            if not qry_id:
                # id is maybe a vhost
                qry_id = cls.from_vhost(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def from_vhost(cls, vhost):
        """retrieve paas instance id associated to a vhost"""

        result = Vhost().list()
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['paas_id']

        return paas_hosts.get(vhost)

    @classmethod
    def from_hostname(cls, hostname):
        """retrieve paas instance id associated to a host"""

        result = cls.list({})
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['id']

        return paas_hosts.get(hostname)
