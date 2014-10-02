""" vlan commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Vlan(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vlan list

    """

    @classmethod
    def list(cls, datacenter=None):
        """List vm vlan (in the future it should also handle paas vlan)."""
        options = {}
        if datacenter:
            datacenter_id = int(Datacenter.usable_id(datacenter))
            options['datacenter_id'] = datacenter_id

        return cls.call('hosting.vlan.list', options)

    @classmethod
    def _info(cls, vlan_id):
        """ Get information about a vlan."""
        return cls.call('hosting.vlan.info', vlan_id)

    @classmethod
    def info(cls, name):
        """ Get information about a vlan."""
        return cls._info(cls.usable_id(name))

    @classmethod
    def from_name(cls, name):
        """Retrieve domain id associated to a FQDN."""
        result = cls.list()
        vlans = {}
        for vlan in result:
            vlans[vlan['name']] = vlan['id']

        return vlans.get(name)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be name or id."""
        try:
            # id is maybe a name
            qry_id = cls.from_name(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
