
from gandi.conf import GandiPlugin


class Paas(GandiPlugin):

    def list(self, options):
        """list Paas instances"""

        return self.call('paas.list', options)

    def info(self, id):
        """display information about a Paas instance"""

        return self.call('paas.info', id)


class Vhost(GandiPlugin):

    def list(self, options=None):
        """list virtual hosts"""

        if not options:
            options = {}

        return self.call('paas.vhost.list', options)
