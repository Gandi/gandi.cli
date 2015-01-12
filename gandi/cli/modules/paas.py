""" PaaS commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.metric import Metric
from gandi.cli.modules.vhost import Vhost
from gandi.cli.modules.datacenter import Datacenter
from gandi.cli.modules.sshkey import SshkeyHelper


class Paas(GandiModule, SshkeyHelper):

    """ Module to handle CLI commands.

    $ gandi paas clone
    $ gandi paas console
    $ gandi paas create
    $ gandi paas delete
    $ gandi paas info
    $ gandi paas list
    $ gandi paas restart
    $ gandi paas types
    $ gandi paas update

    """

    @classmethod
    def type_list(cls, options={}):
        """List type of PaaS instances."""
        return cls.safe_call('paas.type.list', options)

    @classmethod
    def list(cls, options=None):
        """List PaaS instances."""
        return cls.call('paas.list', options)

    @classmethod
    def info(cls, id):
        """Display information about a PaaS instance."""
        return cls.call('paas.info', cls.usable_id(id))

    @classmethod
    def quota(cls, id):
        """return disk quota used/free"""
        sampler = {'unit': 'minutes', 'value': 1, 'function': 'avg'}
        query = 'vfs.df.bytes.all'
        metrics = Metric.query(id, 60, query, 'paas', sampler)

        df = {'free': 0, 'used': 0}
        for metric in metrics:
            what = metric['size'].pop()
            # we need the most recent points
            metric['points'].reverse()
            for point in metric['points']:
                if 'value' in point:
                    df[what] = point['value']
                    break
        return df

    @classmethod
    def delete(cls, resources, background=False):
        """Delete a PaaS instance."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('paas.delete', cls.usable_id(item))
            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Deleting your PaaS instance.')
        cls.display_progress(opers)

    @classmethod
    def update(cls, id, name, size, quantity, password, sshkey, upgrade,
               console, snapshot_profile, reset_mysql_password, background):
        """Update a PaaS instance."""
        if not background and not cls.intty():
            background = True

        paas_params = {}

        if name:
            paas_params['name'] = name

        if size:
            paas_params['size'] = size

        if quantity:
            paas_params['quantity'] = quantity

        if password:
            paas_params['password'] = password

        paas_params.update(cls.convert_sshkey(sshkey))

        if upgrade:
            paas_params['upgrade'] = upgrade

        if console:
            paas_params['console'] = console

        if snapshot_profile:
            paas_params['snapshot_profile'] = snapshot_profile

        if reset_mysql_password:
            paas_params['reset_mysql_password'] = reset_mysql_password

        result = cls.call('paas.update', cls.usable_id(id), paas_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Updating your PaaS instance.')
        cls.display_progress(result)

    @classmethod
    def create(cls, name, size, type, quantity, duration, datacenter, vhosts,
               password, snapshot_profile, background, sshkey):
        """Create a new PaaS instance."""
        if not background and not cls.intty():
            background = True

        datacenter_id_ = int(Datacenter.usable_id(datacenter))

        paas_params = {
            'name': name,
            'size': size,
            'type': type,
            'duration': duration,
            'datacenter_id': datacenter_id_,
        }

        if password:
            paas_params['password'] = password

        if quantity:
            paas_params['quantity'] = quantity

        paas_params.update(cls.convert_sshkey(sshkey))

        if snapshot_profile:
            paas_params['snapshot_profile'] = snapshot_profile

        result = cls.call('paas.create', paas_params)

        if not background:
            # interactive mode, run a progress bar
            cls.echo('Creating your PaaS instance.')
            cls.display_progress(result)
            cls.echo('Your PaaS instance %s has been created.' % name)

        cls.init_conf(name, created=not background, vhosts=vhosts)
        return result

    @classmethod
    def restart(cls, resources, background=False):
        """Restart a PaaS instance."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('paas.restart', cls.usable_id(item))
            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Restarting your PaaS instance.')
        cls.display_progress(opers)

    @classmethod
    def resource_list(cls):
        """ Get the possible list of resources (name, id and vhosts). """
        items = cls.list()
        ret = [paas['name'] for paas in items]
        ret.extend([str(paas['id']) for paas in items])
        for paas in items:
            paas = cls.info(paas['id'])
            ret.extend([vhost['name'] for vhost in paas['vhosts']])

        return ret

    @classmethod
    def console(cls, id):
        """Open a console to a PaaS instance."""
        oper = cls.call('paas.update', cls.usable_id(id), {'console': 1})
        cls.echo('Activation of the console on your PaaS instance')
        cls.display_progress(oper)
        console_url = Paas.info(cls.usable_id(id))['console']
        access = 'ssh %s' % console_url
        cls.execute(access)

    @classmethod
    def init_conf(cls, id, vhost=None, created=True, vhosts=None,
                  background=False):
        """ Initialize local configuration with PaaS information. """
        paas = Paas.info(cls.usable_id(id))
        cls.debug('save PaaS instance information to local configuration')

        if vhost and not vhosts:
            vhosts = [vhost]
        if not vhosts:
            if 'php' not in paas['type']:
                vhost = 'default'
            elif paas['vhosts']:
                vhosts = [vht['name'] for vht in paas['vhosts']]
            else:
                return

        for vhost in vhosts:
            Vhost.create(paas, vhost, True, background)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be hostname, vhost, id."""
        try:
            # id is maybe a hostname
            qry_id = cls.from_hostname(id)
            if not qry_id:
                # id is maybe a vhost
                qry_id = cls.from_vhost(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def from_vhost(cls, vhost):
        """Retrieve paas instance id associated to a vhost."""
        result = Vhost().list()
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['paas_id']

        return paas_hosts.get(vhost)

    @classmethod
    def from_hostname(cls, hostname):
        """Retrieve paas instance id associated to a host."""
        result = cls.list({})
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['id']

        return paas_hosts.get(hostname)

    @classmethod
    def list_names(cls):
        """Retrieve paas id and names."""
        ret = dict([(item['id'], item['name'])
                    for item in cls.list({})])
        return ret
