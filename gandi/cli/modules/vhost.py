""" Vhost commands module. """

from click import UsageError

from gandi.cli.modules.paas import Paas
from gandi.cli.core.base import GandiModule


class Vhost(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vhost create
    $ gandi vhost delete
    $ gandi vhost info
    $ gandi vhost list

    """

    @classmethod
    def list(cls, options=None):
        """ List paas vhosts (in the future it should handle iaas vhosts)."""
        options = options or {}
        return cls.call('paas.vhost.list', options)

    @classmethod
    def info(cls, name):
        """ Display information about a vhost. """
        return cls.call('paas.vhost.info', name)

    @classmethod
    def create(cls, paas, vhost, alter_zone, background):
        """ Create a new vhost. """
        if not background and not cls.intty():
            background = True

        paas_id = Paas.usable_id(paas)
        params = {'paas_id': paas_id,
                  'vhost': vhost,
                  'zone_alter': alter_zone}
        result = cls.call('paas.vhost.create', params, dry_run=True)

        if background:
            return result

        cls.echo('Creating a new vhost.')
        cls.display_progress(result)
        cls.echo('Your vhost %s has been created.' % vhost)

        return result

    @classmethod
    def delete(cls, resources, background=False):
        """ Delete this vhost. """
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('paas.vhost.delete', item)
            opers.append(oper)

        if background:
            return opers

        cls.echo('Deleting your vhost.')
        cls.display_progress(opers)

    @classmethod
    def git_remote(cls, vhost):
        """Return remote for given vhost"""
        paas = Paas.info(vhost)
        git_server = paas['git_server']
        # hack for dev
        if 'dev' in paas['console']:
            git_server = 'git.hosting.dev.gandi.net'

        paas_access = '%s@%s' % (paas['user'], git_server)

        if 'php' not in paas['type']:
            remote = 'ssh+git://%s/default.git' % paas_access
        else:
            remote = 'ssh+git://%s/%s.git' % (paas_access, vhost)

        return remote

    @classmethod
    def attach(cls, vhost):
        """Attach a vhost to a remote from the local
        repository"""
        remote = cls.git_remote(vhost)

        return cls.execute('git remote add %s %s' % (vhost, remote,))

    @classmethod
    def clone(cls, vhost, directory=None):
        """Clone this vhost in a local git repository"""

        remote = cls.git_remote(vhost)

        if not directory:
            directory = vhost

        git_command = 'git clone %s %s' % (remote, directory)

        return cls.execute(git_command)
