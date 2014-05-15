
from gandi.conf import GandiPlugin


class Paas(GandiPlugin):

    def list(self, options):
        """list Paas instances"""

        return self.call('paas.list', options)

    def list_vhost(self, options=None):
        """display information about a virtual machine"""

        if not options:
            options = {}

        return self.call('paas.vhost.list', options)

    def info(self, id):
        """display information about a Paas instance"""

        return self.call('paas.info', id)
