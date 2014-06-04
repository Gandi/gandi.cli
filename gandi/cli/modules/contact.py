
from gandi.cli.core.conf import GandiModule


class Contact(GandiModule):

    @classmethod
    def info(cls):
        """display information about a Contact"""

        return cls.call('contact.info')
