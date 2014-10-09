""" vlan commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Vlan(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vlan list
    $ gandi vlan info
    $ gandi vlan create
    $ gandi vlan update
    $ gandi vlan delete

    """

    @classmethod
    def list(cls, datacenter=None):
        """List virtual machine vlan

        (in the future it should also handle PaaS vlan)."""
        options = {}
        if datacenter:
            datacenter_id = int(Datacenter.usable_id(datacenter))
            options['datacenter_id'] = datacenter_id

        return cls.call('hosting.vlan.list', options)

    @classmethod
    def resource_list(cls):
        """ Get the possible list of resources (name, id). """
        items = cls.list()
        ret = [vlan['name'] for vlan in items]
        ret.extend([str(vlan['id']) for paas in items])
        return ret

    @classmethod
    def _info(cls, vlan_id):
        """ Get information about a vlan."""
        return cls.call('hosting.vlan.info', vlan_id)

    @classmethod
    def info(cls, name):
        """ Get information about a vlan."""
        return cls._info(cls.usable_id(name))

    @classmethod
    def delete(cls, resources, background=False):
        """Delete a vlan."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.vlan.delete', cls.usable_id(item))
            if not oper:
                continue

            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Deleting your vlan.')
        if opers:
            cls.display_progress(opers)

    @classmethod
    def create(cls, name, datacenter, background):
        """Create a new vlan."""
        if not background and not cls.intty():
            background = True

        datacenter_id_ = int(Datacenter.usable_id(datacenter))

        vlan_params = {
            'name': name,
            'datacenter_id': datacenter_id_,
        }
        result = cls.call('hosting.vlan.create', vlan_params)

        if not background:
            # interactive mode, run a progress bar
            cls.echo('Creating your vlan.')
            cls.display_progress(result)
            cls.echo('Your vlan %s has been created.' % name)

        return result

    @classmethod
    def update(cls, id, name):
        """Update an existing vlan."""
        vlan_params = {
            'name': name,
        }

        cls.echo('Updating your vlan.')
        result = cls.call('hosting.vlan.update', cls.usable_id(id),
                          vlan_params)
        return result

    @classmethod
    def from_name(cls, name):
        """Retrieve vlan id associated to a name."""
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
