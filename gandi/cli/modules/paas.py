
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
    def list(cls, options):
        """list Paas instances"""

        return cls.call('paas.list', options)

    @classmethod
    def info(cls, id):
        """display information about a Paas instance"""

        return cls.call('paas.info', cls.usable_id(id))

    @classmethod
    def delete(cls, id):
        """delete a Paas instance"""

        return cls.call('paas.delete', cls.usable_id(id))

    @classmethod
    def create(cls, name, size, type, quantity, duration, datacenter, vhosts,
               password, snapshot_profile, interactive, ssh_key):
        """create a new PaaS instance.

        you can specify a configuration entry named 'ssh_key' containing
        path to your ssh_key file

        >>> gandi config ssh_key ~/.ssh/id_rsa.pub

        """

        if interactive and not cls.intty():
            interactive = False

        # priority to command line parameters
        # then env var
        # then local configuration
        # then global configuration
        name_ = name or cls.get('paas.name')
        size_ = size or cls.get('paas.size')
        type_ = type or cls.get('paas.type')
        password_ = password or cls.get('paas.password')
        duration_ = duration or cls.get('paas.duration')

        if datacenter:
            datacenter_id_ = int(Datacenter.usable_id(datacenter))
        else:
            datacenter_id_ = int(Datacenter.usable_id(cls.get('paas.datacenter')))

        paas_params = {
            'name': name_,
            'size': size_,
            'type': type_,
            'password': password_,
            'duration': duration_,
            'datacenter_id': datacenter_id_,
        }
        vhosts_ = vhosts or cls.get('paas.vhosts', mandatory=False)
        if vhosts_ is not None:
            paas_params['vhosts'] = vhosts_

        quantity_ = quantity or int(cls.get('paas.quantity', 0,
                                            mandatory=False))
        if quantity_ is not None:
            paas_params['quantity'] = quantity_

        ssh_key_ = ssh_key or cls.get('ssh_key', mandatory=False)
        if ssh_key_ is not None:
            with open(ssh_key_) as fdesc:
                ssh_key_ = fdesc.read()
            if ssh_key_ is not None:
                paas_params['ssh_key'] = ssh_key_

        result = cls.call('paas.create', paas_params)
        if not interactive:
            return result

        # interactive mode, run a progress bar
        cls.echo("We're creating your first PaaS with default settings.")
        cls.display_progress(result)
        cls.echo('Your PaaS %s have been created.' % name_)

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
