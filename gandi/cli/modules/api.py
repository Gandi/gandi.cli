
from gandi.cli.core.conf import GandiModule


class Api(GandiModule):

    @classmethod
    def info(cls):
        """display information about API"""

        return cls.call('version.info')
