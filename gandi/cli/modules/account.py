""" Hosting account module. """

from gandi.cli.core.base import GandiModule


class Account(GandiModule):

    """ Module to handle CLI commands.

    $ gandi account info

    """

    @classmethod
    def info(cls):
        """Get information about the hosting account in use"""
        return cls.call('hosting.account.info')
