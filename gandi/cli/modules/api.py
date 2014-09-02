""" API commands module. """

from gandi.cli.core.base import GandiModule


class Api(GandiModule):

    """ Module to handle CLI commands.

    $ gandi api
    """

    @classmethod
    def info(cls):
        """Display information about API."""
        return cls.call('version.info')
