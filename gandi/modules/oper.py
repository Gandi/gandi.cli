
from gandi.conf import GandiModule


class Oper(GandiModule):

    @classmethod
    def list(cls, options):
        """list operation"""

        return cls.call('operation.list', options)

    @classmethod
    def info(cls, id):
        """display information about an operation"""

        return cls.call('operation.info', id)
