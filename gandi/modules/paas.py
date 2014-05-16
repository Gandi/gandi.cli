
from gandi.conf import GandiModule


class Vhost(GandiModule):

    @classmethod
    def list(cls, options=None):
        """list virtual hosts"""

        if not options:
            options = {}

        return cls.call('paas.vhost.list', options)


class Paas(GandiModule):

    @classmethod
    def list(cls, options):
        """list Paas instances"""

        return cls.call('paas.list', options)

    @classmethod
    def info(cls, id):
        """display information about a Paas instance"""

        return cls.call('paas.info', cls.usable_id(id))

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a vhost
            qry_id = cls.from_vhost(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def from_vhost(cls, vhost):
        """retrieve paas instance id associated to a vhost"""

        result = Vhost().list()
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['paas_id']

        return paas_hosts.get(vhost)
