""" PaaS commands module. """

import re
import sys

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.metric import Metric
from gandi.cli.modules.vhost import Vhost
from gandi.cli.modules.datacenter import Datacenter
from gandi.cli.modules.sshkey import SshkeyHelper


class Paas(GandiModule, SshkeyHelper):

    """ Module to handle CLI commands.

    $ gandi paas attach
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
    def type_list(cls, options=None):
        """List type of PaaS instances."""
        return cls.safe_call('paas.type.list', options)

    @classmethod
    def clone(cls, name, vhost, directory, origin):
        """Clone a PaaS instance's vhost into a local git repository."""
        paas_info = cls.info(name)

        if 'php' in paas_info['type'] and not vhost:
            cls.error('PHP instances require indicating the VHOST to clone '
                      'with --vhost <vhost>')

        paas_access = '%s@%s' % (paas_info['user'], paas_info['git_server'])
        remote_url = 'ssh+git://%s/%s.git' % (paas_access, vhost)

        command = 'git clone %s %s --origin %s' \
                  % (remote_url, directory, origin)

        init_git = cls.execute(command)
        if init_git:
            cls.echo('Use `git push %s master` to push your code to the '
                     'instance.' % (origin))
            cls.echo('Then `$ gandi deploy` to build and deploy your '
                     'application.')

    @classmethod
    def attach(cls, name, vhost, remote_name):
        """Attach an instance's vhost to a remote from the local repository."""
        paas_access = cls.get('paas_access')

        if not paas_access:
            paas_info = cls.info(name)
            paas_access = '%s@%s' \
                          % (paas_info['user'], paas_info['git_server'])

        remote_url = 'ssh+git://%s/%s.git' % (paas_access, vhost)

        ret = cls.execute('git remote add %s %s' % (remote_name, remote_url,))

        if ret:
            cls.echo('Added remote `%s` to your local git repository.'
                     % (remote_name))
            cls.echo('Use `git push %s master` to push your code to the '
                     'instance.' % (remote_name))
            cls.echo('Then `$ gandi deploy` to build and deploy your '
                     'application.')

    @classmethod
    def deploy(cls, remote_name, branch):
        """Deploy a PaaS instance."""
        def get_remote_url(remote):
            return 'git config --local --get remote.%s.url' % (remote)

        remote_url = cls.exec_output(get_remote_url(remote_name)) \
            .replace('\n', '')

        if not remote_url or not re.search('gpaas.net|gandi.net', remote_url):
            remote_name = ('$(git config --local --get branch.%s.remote)' %
                           branch)
            remote_url = cls.exec_output(get_remote_url(remote_name)) \
                .replace('\n', '')

        error = None

        if not remote_url:
            error = True
            cls.echo('Error: Could not find git remote '
                     'to extract deploy url from.')
        elif not re.search('gpaas.net|gandi.net', remote_url):
            error = True
            cls.echo('Error: %s is not a valid Simple Hosting git remote.'
                     % (remote_url))
        if error:
            cls.echo("""This usually happens when:
- the current directory has no Simple Hosting git remote attached,
  in this case, please see $ gandi paas attach --help
- the local branch being deployed hasn't been pushed to the \
remote repository yet,
  in this case, please try $ git push <remote> %s
""" % (branch))
            cls.echo('Otherwise, it\'s recommended to use'
                     ' the --remote and/or --branch options:\n'
                     '$ gandi deploy --remote <remote> [--branch <branch>]')
            sys.exit(2)

        remote_url_no_protocol = remote_url.split('://')[1]
        splitted_url = remote_url_no_protocol.split('/')

        paas_access = splitted_url[0]
        deploy_git_host = splitted_url[1]

        command = "ssh %s 'deploy %s %s'" \
                  % (paas_access, deploy_git_host, branch)

        cls.execute(command)

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
    def cache(cls, id):
        """return the number of query cache for the last 24H"""
        sampler = {'unit': 'days', 'value': 1, 'function': 'sum'}
        query = 'webacc.requests.cache.all'
        metrics = Metric.query(id, 60 * 60 * 24, query, 'paas', sampler)

        cache = {'hit': 0, 'miss': 0, 'not': 0, 'pass': 0}
        for metric in metrics:
            what = metric['cache'].pop()
            for point in metric['points']:
                value = point.get('value', 0)
                cache[what] += value
        return cache

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

        # XXX to delete a snapshot_profile the value has to be an empty string
        if snapshot_profile is not None:
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

        if vhosts:
            paas_info = cls.info(name)
            Vhost.create(paas_info, vhosts, True, background)

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
        items = cls.list({'items_per_page': 500})
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
        result = cls.list({'items_per_page': 500})
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['id']

        return paas_hosts.get(hostname)

    @classmethod
    def list_names(cls):
        """Retrieve paas id and names."""
        ret = dict([(item['id'], item['name'])
                    for item in cls.list({'items_per_page': 500})])
        return ret
