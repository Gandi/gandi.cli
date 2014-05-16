
from gandi.conf import GandiModule


class Vhost(GandiModule):

    def list(self, options=None):
        """list virtual hosts"""

        if not options:
            options = {}

        return self.call('paas.vhost.list', options)


class Paas(GandiModule):

    def list(self, options):
        """list Paas instances"""

        return self.call('paas.list', options)

    def info(self, id):
        """display information about a Paas instance"""

        return self.call('paas.info', self.usable_id(id))

    def usable_id(self, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a hostname
            qry_id = self.from_hostname(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            self.error(msg)

        return qry_id

    def from_vhost(self, vhost):
        """retrieve paas instance id associated to a vhost"""

        result = Vhost().list()
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['paas_id']

        return paas_hosts.get(vhost)
