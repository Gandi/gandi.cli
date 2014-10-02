""" Datacenter commands module. """

from gandi.cli.core.base import GandiModule


class Datacenter(GandiModule):

    """ Module to handle CLI commands.

    $ gandi datacenters
    """

    @classmethod
    def list(cls, options=None):
        """List available datacenters."""
        return cls.safe_call('hosting.datacenter.list', options or {})

    @classmethod
    def filtered_list(cls, name=None, obj=None):
        """List datacenters matching name and compatible
        with obj"""
        options = {}
        if name:
            options['id'] = cls.usable_id(name)

        def obj_ok(dc, obj):
            if not obj or obj['datacenter_id'] == dc['id']:
                return True
            return False

        return [x for x in cls.list(options) if obj_ok(x, obj)]

    @classmethod
    def from_iso(cls, iso):
        """Retrieve datacenter id associated to an ISO."""
        result = cls.list()
        dc_isos = {}
        for dc in result:
            dc_isos[dc['iso']] = dc['id']

        return dc_isos.get(iso)

    @classmethod
    def from_name(cls, name):
        """Retrieve datacenter id associated to a name."""
        result = cls.list()
        dc_names = {}
        for dc in result:
            dc_names[dc['name']] = dc['id']

        return dc_names.get(name)

    @classmethod
    def from_country(cls, country):
        """Retrieve datacenter id associated to a country."""
        result = cls.list()
        dc_countries = {}
        for dc in result:
            dc_countries[dc['country']] = dc['id']

        return dc_countries.get(country)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be ISO, name, country."""
        try:
            # id is maybe a ISO
            qry_id = cls.from_iso(id)
            if not qry_id:
                # id is maybe a name
                qry_id = cls.from_name(id)
            if not qry_id:
                # id is maybe a country
                qry_id = cls.from_country(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
