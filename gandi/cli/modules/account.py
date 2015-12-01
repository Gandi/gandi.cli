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
        usage = [sum(resource.values())
                 for resource in rating.values()
                 if isinstance(resource, dict)]
        return sum(usage)

    @classmethod
    def all(cls):
        """ Get all informations about this account """
        account = cls.info()
        creditusage = cls.creditusage()

        if not creditusage:
            return account

        left = account['credits'] / creditusage
        years, hours = divmod(left, 365 * 24)
        months, hours = divmod(hours, 31 * 24)
        days, hours = divmod(hours, 24)

        account.update({'credit_usage': creditusage,
                        'left': (years, months, days, hours)})

        return account
