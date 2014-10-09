""" Iface commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.datacenter import Datacenter
from gandi.cli.modules.vlan import Vlan
from gandi.cli.modules.iaas import Iaas


class Iface(GandiModule):

    """ Module to handle CLI commands.

    $ gandi iface list
    $ gandi iface info
    $ gandi iface create
    $ gandi iface delete
    $ gandi iface update

    """

    @classmethod
    def list(cls, options=None):
        """ List all ifaces."""
        options = options or {}
        return cls.call('hosting.iface.list', options)

    @classmethod
    def _info(cls, iface_id):
        """ Get information about an iface."""
        return cls.call('hosting.iface.info', iface_id)

    @classmethod
    def info(cls, num):
        """ Get information about an iface."""
        return cls._info(cls.usable_id(num))

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be num or id."""
        try:
            qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def _attach(cls, iface_id, vm_id):
        """ Attach an iface to a vm. """
        oper = cls.call('hosting.vm.iface_attach', vm_id, iface_id)
        return oper

    @classmethod
    def create(cls, ip_version, datacenter, bandwidth, vlan, vm, background):
        """ Create a new iface """
        if not background and not cls.intty():
            background = True

        datacenter_id_ = int(Datacenter.usable_id(datacenter))

        iface_params = {
            'ip_version': ip_version,
            'datacenter_id': datacenter_id_,
            'bandwidth': bandwidth,
        }
        if vlan:
            iface_params['vlan'] = Vlan.usable_id(vlan)

        result = cls.call('hosting.iface.create', iface_params)

        if background and not vm:
            return result

        # interactive mode, run a progress bar
        cls.echo('Creating your iface.')
        cls.display_progress(result)
        cls.echo('Your iface has been created.')

        if not vm:
            return

        vm_id = Iaas.usable_id(vm)
        result = cls._attach(result['iface_id'], vm_id)

        if background:
            return result

        cls.echo('Attaching your iface.')
        cls.display_progress(result)

    @classmethod
    def _detach(cls, iface_id):
        """ Detach an iface from a vm. """
        iface = cls._info(iface_id)
        opers = []
        vm_id = iface.get('vm_id')
        if vm_id:
            cls.echo('The iface is still attached to the vm %s.' % vm_id)
            cls.echo('Will detach it.')
            opers.append(cls.call('hosting.vm.iface_detach', vm_id, iface_id))
        return opers

    @classmethod
    def delete(cls, resources, background=False):
        """ Delete this iface."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        resources = [cls.usable_id(item) for item in resources]

        opers = []
        for iface_id in resources:
            opers.extend(cls._detach(iface_id))

        if opers:
            cls.echo('Detaching your iface(s).')
            cls.display_progress(opers)

        opers = []
        for iface_id in resources:
            oper = cls.call('hosting.iface.delete', iface_id)
            opers.append(oper)

        if background:
            return opers

        cls.echo('Deleting your iface.')
        cls.display_progress(opers)

    @classmethod
    def update(cls, id, bandwidth, vm, background):
        """ Update this iface. """
        if not background and not cls.intty():
            background = True

        iface_params = {}
        iface_id = cls.usable_id(id)

        if bandwidth:
            iface_params['bandwidth'] = bandwidth

        if iface_params:
            result = cls.call('hosting.iface.update', iface_id, iface_params)
            if background:
                return result

            # interactive mode, run a progress bar
            cls.echo('Updating your iface %s.' % id)
            cls.display_progress(result)

        if not vm:
            return

        vm_id = Iaas.usable_id(vm)

        opers = cls._detach(iface_id)
        if opers:
            cls.echo('Detaching iface.')
            cls.display_progress(opers)

        result = cls._attach(iface_id, vm_id)

        if background:
            return result

        cls.echo('Attaching your iface.')
        cls.display_progress(result)
