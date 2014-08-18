from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class Disk(GandiModule):

    @classmethod
    def from_name(cls, name):
        """ retrieve a disk id accsociated to a name """
        disks = cls.list({'name': name})
        if len(disks) == 1:
            return disks[0]['id']
        elif not disks:
            return

        raise DuplicateResults('disk name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
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
        """ list all disks """
        options = options or {}
        return cls.call('hosting.disk.list', options)

    @classmethod
    def info(cls, name):
        """ get information about a disk """
        return cls.call('hosting.disk.info', cls.usable_id(name))

    @classmethod
    def update(cls, resource, name, size, snapshot_profile, background):
        """ update this disk """
        disk_params = {}

        if name:
            disk_params['name'] = name

        if snapshot_profile:
            disk_params['snapshot_profile'] = snapshot_profile

        result = cls.call('hosting.disk.update',
                          cls.usable_id(resource),
                          disk_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo("Updating your disk.")
        cls.display_progress(result)

    @classmethod
    def delete(cls, resources, background=False):
        """ delete this disk """
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.disk.delete', cls.usable_id(item))
            opers.append(oper)

        if background:
            return opers

        cls.echo('Deleting your disk.')
        cls.display_progress(opers)
