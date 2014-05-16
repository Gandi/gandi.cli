
from gandi.conf import GandiModule


class Oper(GandiModule):

    def list(self, options):
        """list operation"""

        return self.call('operation.list', options)

    def info(self, id):
        """display information about an operation"""

        return self.call('operation.info', id)
