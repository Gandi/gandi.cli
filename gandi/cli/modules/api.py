
from gandi.cli.core.base import GandiModule


class Api(GandiModule):

    @classmethod
    def info(cls):
        """display information about API"""

        return cls.call('version.info')
