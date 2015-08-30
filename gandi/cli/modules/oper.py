""" Operation commands module. """

from gandi.cli.core.base import GandiModule


class Oper(GandiModule):

    """ Module to handle CLI commands.

    $ gandi oper info
    $ gandi oper list

    """

    @classmethod
    def list(cls, options):
        """List operation."""
        return cls.call('operation.list', options)

    @classmethod
    def count(cls, options):
        """Count operation."""
        return cls.call('operation.count', options)

    @classmethod
    def info(cls, id):
        """Display information about an operation."""
        return cls.call('operation.info', id)
