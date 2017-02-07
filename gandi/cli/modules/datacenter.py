""" Datacenter commands module. """

from __future__ import print_function

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DatacenterClosed, DatacenterLimited


class Datacenter(GandiModule):

    """ Module to handle CLI commands.

    $ gandi datacenters
    """

    @classmethod
    def list(cls, options=None):
        """List available datacenters."""
        return cls.safe_call('hosting.datacenter.list', options or {})

    @classmethod
    def is_opened(cls, dc_code, type_):
        """List opened datacenters for given type."""
        options = {'dc_code': dc_code, '%s_opened' % type_: True}
        datacenters = cls.safe_call('hosting.datacenter.list', options)
        if not datacenters:
            # try with ISO code
            options = {'iso': dc_code, '%s_opened' % type_: True}
            datacenters = cls.safe_call('hosting.datacenter.list', options)
            if not datacenters:
                raise DatacenterClosed(r'/!\ Datacenter %s is closed, please '
                                       'choose another datacenter.' % dc_code)

        datacenter = datacenters[0]
        if datacenter.get('%s_closed_for' % type_) == 'NEW':
            dc_close_date = datacenter.get('deactivate_at', '')
            if dc_close_date:
                dc_close_date = dc_close_date.strftime('%d/%m/%Y')
            raise DatacenterLimited(dc_close_date)

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
        """Retrieve the first datacenter id associated to an ISO."""
        result = cls.list({'sort_by': 'id ASC'})
        dc_isos = {}
        for dc in result:
            if dc['iso'] not in dc_isos:
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
        """Retrieve the first datacenter id associated to a country."""
        result = cls.list({'sort_by': 'id ASC'})
        dc_countries = {}
        for dc in result:
            if dc['country'] not in dc_countries:
                dc_countries[dc['country']] = dc['id']

        return dc_countries.get(country)

    @classmethod
    def from_dc_code(cls, dc_code):
        """Retrieve the datacenter id associated to a dc_code"""
        result = cls.list()
        dc_codes = {}
        for dc in result:
            if dc.get('dc_code'):
                dc_codes[dc['dc_code']] = dc['id']

        return dc_codes.get(dc_code)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be ISO, name, country, dc_code."""
        try:
            # id is maybe a dc_code
            qry_id = cls.from_dc_code(id)
            if not qry_id:
                # id is maybe a ISO
                qry_id = cls.from_iso(id)
                if qry_id:
                    cls.deprecated('ISO code for datacenter filter use '
                                   'dc_code instead')
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
