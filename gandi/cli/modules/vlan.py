""" vlan commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Vlan(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vlan list

    """

    @classmethod
    def list(cls, datacenter=None):
        """List vm vlan (in the future it should handle paas vlans)."""
        options = {}
        if datacenter:
            datacenter_id = int(Datacenter.usable_id(datacenter))
            options['datacenter_id'] = datacenter_id

        return cls.call('hosting.vlan.list', options)

