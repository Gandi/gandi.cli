""" Contact commands module. """

from gandi.cli.core.base import GandiModule


class Contact(GandiModule):

    """ Module to handle CLI commands."""

    @classmethod
    def info(cls):
        """Display information about a Contact."""
        return cls.call('contact.info')

    @classmethod
    def create(cls, params):
        """Create a new contact."""
        return cls.call('contact.create', params, empty_key=True)
