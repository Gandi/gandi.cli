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

    @classmethod
    def creditusage(cls):
        """Get credit usage per hour"""
        rating = cls.call('hosting.rating.list')
        if not rating:
            return 0

        rating = rating.pop()
        usage = [sum(resource.values()) for (_, resource) in rating.iteritems()
                 if type(resource) is dict]
        return sum(usage)
