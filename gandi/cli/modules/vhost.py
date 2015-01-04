""" Vhost commands module. """

import os

from gandi.cli.core.base import GandiModule


class Vhost(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vhost create
    $ gandi vhost delete
    $ gandi vhost info
    $ gandi vhost list

    """
    @classmethod
    def init_vhost(cls, vhost, created=True, id=None, paas=None):
        """Initialize vhost directory and create a local configuration file."""
        assert id or paas

        if 'php' not in paas['type']:
            vhost = 'default'

        git_server = paas['git_server']
        # hack for dev
        if 'dev' in paas['console']:
            git_server = 'git.hosting.dev.gandi.net'
        paas_access = '%s@%s' % (paas['user'], git_server)
        current_path = os.getcwd()
        repo_path = os.path.join(current_path, vhost)
        if created:
            if os.path.exists(repo_path):
                cls.echo('%s already exists, please remove it before cloning' %
                         repo_path)
                return

            init_git = cls.execute('git clone ssh+git://%s/%s.git' %
                                   (paas_access, vhost))
            if not init_git:
                cls.echo('An error has occurred during git clone of instance.')
                return
        else:
            cls.echo('You should init your git repo when the paas is created, '
                     'type:')
            cls.echo('gandi paas clone %s' % vhost)
            return

        # go into directory to save configuration file in this directory
        os.chdir(repo_path)
        cls.configure(False, 'paas.user', paas['user'])
        cls.configure(False, 'paas.name', paas['name'])
        cls.configure(False, 'paas.deploy_git_host', '%s.git' % vhost)
        cls.configure(False, 'paas.access', paas_access)
        os.chdir(current_path)

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
    def create(cls, paas_info, vhost, alter_zone, background):
        """ Create a new vhost. """
        if not background and not cls.intty():
            background = True

        params = {'paas_id': paas_info['id'],
                  'vhost': vhost,
                  'zone_alter': alter_zone}
        result = cls.call('paas.vhost.create', params, dry_run=True)

        if background:
            return result

        cls.echo('Creating a new vhost.')
        cls.display_progress(result)
        cls.echo('Your vhost %s has been created.' % vhost)

        cls.init_vhost(vhost, created=not background, paas=paas_info)
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
