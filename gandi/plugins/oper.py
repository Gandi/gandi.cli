
from gandi.conf import GandiPlugin


class Oper(GandiPlugin):

    def list(self, options):
        """list operation"""

        return self.call('operation.list', options)

    def info(self, id):
        """display information about an operation"""

        return self.call('operation.info', id)
