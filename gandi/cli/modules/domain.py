
from gandi.cli.core.conf import GandiModule


class Domain(GandiModule):

    @classmethod
    def list(cls, options):
        """list operation"""

        return cls.call('domain.list', options)

    @classmethod
    def info(cls, fqdn):
        """display information about a domain"""

        return cls.call('domain.info', fqdn)

    @classmethod
    def from_fqdn(cls, fqdn):
        """retrieve domain id associated to a fqdn"""

        result = cls.list({})
        domains = {}
        for domain in result:
            domains[domain['fqdn']] = domain['id']

        return domains.get(fqdn)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a fqdn
            qry_id = cls.from_fqdn(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
