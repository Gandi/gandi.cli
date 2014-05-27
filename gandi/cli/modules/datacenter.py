
from gandi.cli.core.conf import GandiModule


class Datacenter(GandiModule):

    @classmethod
    def list(cls):
        """list available datacenters"""

        options = {}

        return cls.call('hosting.datacenter.list', options)

    @classmethod
    def from_iso(cls, iso):
        """retrieve datacenter id associated to an ISO"""

        result = cls.list()
        dc_isos = {}
        for dc in result:
            dc_isos[dc['iso']] = dc['id']

        return dc_isos.get(iso)

    @classmethod
    def from_name(cls, name):
        """retrieve datacenter id associated to a name"""

        result = cls.list()
        dc_names = {}
        for dc in result:
            dc_names[dc['name']] = dc['id']

        return dc_names.get(name)

    @classmethod
    def from_country(cls, country):
        """retrieve datacenter id associated to a country"""

        result = cls.list()
        dc_countries = {}
        for dc in result:
            dc_countries[dc['country']] = dc['id']

        return dc_countries.get(country)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a ISO
            qry_id = cls.from_iso(id)
            if not qry_id:
                # id is maybe a name
                qry_id = cls.from_name(id)
            if not qry_id:
                # id is maybe a country
                qry_id = cls.from_country(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
