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
