""" Disk commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults
from .iaas import Iaas, Datacenter


class Disk(GandiModule):

    """ Module to handle CLI commands.

    $ gandi disk create
    $ gandi disk delete
    $ gandi disk info
    $ gandi disk list
    $ gandi disk update

    """

    @classmethod
    def from_name(cls, name):
        """ Retrieve a disk id accsociated to a name. """
        disks = cls.list({'name': name})
        if len(disks) == 1:
            return disks[0]['id']
        elif not disks:
            return

        raise DuplicateResults('disk name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be name or id."""
        try:
            qry_id = cls.from_name(id)
            if not qry_id:
                qry_id = int(id)
        except DuplicateResults as exc:
            cls.error(exc.errors)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def list(cls, options=None):
        """ List all disks."""
        options = options or {}
        return cls.call('hosting.disk.list', options)

    @classmethod
    def list_create(cls, datacenter=None, label=None):
        """List available disks for vm creation."""
        options = {}
        if datacenter:
            datacenter_id = int(Datacenter.usable_id(datacenter))
            options['datacenter_id'] = datacenter_id

        # implement a filter by label as API doesn't handle it
        images = cls.safe_call('hosting.disk.list', options)
        if not label:
            return images
        return [img for img in images
                if label.lower() in img['name'].lower()]

    @classmethod
    def _info(cls, disk_id):
        """ Get information about a disk."""
        return cls.call('hosting.disk.info', disk_id)

    @classmethod
    def info(cls, name):
        """ Get information about a disk."""
        return cls._info(cls.usable_id(name))

    @staticmethod
    def disk_param(name, size, snapshot_profile, cmdline=None, kernel=None):
        """ Return disk parameter structure. """
        disk_params = {}

        if cmdline:
            disk_params['cmdline'] = cmdline

        if kernel:
            disk_params['kernel'] = kernel

        if name:
            disk_params['name'] = name

        if snapshot_profile:
            disk_params['snapshot_profile'] = snapshot_profile

        if size:
            disk_params['size'] = size

        return disk_params

    @classmethod
    def update(cls, resource, name, size, snapshot_profile,
               background, cmdline=None, kernel=None):
        """ Update this disk. """
        disk_params = cls.disk_param(name, size, snapshot_profile,
                                     cmdline, kernel)

        result = cls.call('hosting.disk.update',
                          cls.usable_id(resource),
                          disk_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Updating your disk.')
        cls.display_progress(result)

    @classmethod
    def _detach(cls, disk_id):
        """ Detach a disk from a vm. """
        disk = cls._info(disk_id)
        opers = []
        if disk.get('vms_id'):
            for vm_id in disk['vms_id']:
                cls.echo('The disk is still attached to the vm %s.' % vm_id)
                cls.echo('Will detach it.')
                opers.append(cls.call('hosting.vm.disk_detach',
                                      vm_id, disk_id))
        return opers

    @classmethod
    def delete(cls, resources, background=False):
        """ Delete this disk."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        resources = [cls.usable_id(item) for item in resources]

        opers = []
        for disk_id in resources:
            opers.extend(cls._detach(disk_id))

        if opers:
            cls.echo('Detaching your disk(s).')
            cls.display_progress(opers)

        opers = []
        for disk_id in resources:
            oper = cls.call('hosting.disk.delete', disk_id)
            opers.append(oper)

        if background:
            return opers

        cls.echo('Deleting your disk.')
        cls.display_progress(opers)

    @classmethod
    def _attach(cls, disk_id, vm_id):
        """ Attach a disk to a vm. """
        oper = cls.call('hosting.vm.disk_attach', vm_id, disk_id)
        return oper

    @classmethod
    def create(cls, name, vm, size, snapshotprofile, datacenter,
               background=False):
        """ Create a disk and attach it to a vm. """
        disk_params = cls.disk_param(name, size, snapshotprofile)
        disk_params['datacenter_id'] = int(Datacenter.usable_id(datacenter))

        result = cls.call('hosting.disk.create', disk_params)

        if background and not vm:
            return result

        # interactive mode, run a progress bar
        cls.echo('Creating your disk.')
        cls.display_progress(result)

        if not vm:
            return

        vm_id = Iaas.usable_id(vm)
        result = cls._attach(result['disk_id'], vm_id)

        if background:
            return result

        cls.echo('Attaching your disk.')
        cls.display_progress(result)
