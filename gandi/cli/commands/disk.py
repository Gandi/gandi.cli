""" Disk namespace commands. """

import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_disk, output_generic, randomstring,
    DatacenterLimited
)
from gandi.cli.core.utils.size import disk_check_size
from gandi.cli.core.params import (pass_gandi, DATACENTER, SNAPSHOTPROFILE_VM,
                                   KERNEL, SIZE, option, DISK_IMAGE)


@cli.command()
@click.option('--only-data', help='Only display data disks.', is_flag=True)
@click.option('--only-snapshot', help='Only display snapshots.', is_flag=True)
@click.option('--attached', help='Only display disks attached to a VM',
              is_flag=True)
@click.option('--detached', help='Only display detached disks', is_flag=True)
@click.option('--type', help='Display types.', is_flag=True)
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--vm', help='Display vms.', is_flag=True)
@click.option('--snapshotprofile', help='Display snapshot profile.',
              is_flag=True)
@click.option('--datacenter', default=None, type=DATACENTER,
              help='Filter results by datacenter.')
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, only_data, only_snapshot, attached, detached, type, id, vm,
         snapshotprofile, datacenter, limit):
    """ List disks. """
    options = {
        'items_per_page': limit,
    }

    if attached and detached:
        raise UsageError('You cannot use both --attached and --detached.')

    if only_data:
        options.setdefault('type', []).append('data')
    if only_snapshot:
        options.setdefault('type', []).append('snapshot')
    if datacenter:
        options['datacenter_id'] = gandi.datacenter.usable_id(datacenter)

    output_keys = ['name', 'state', 'size']
    if type:
        output_keys.append('type')
    if id:
        output_keys.append('id')
    if vm:
        output_keys.append('vm')

    profiles = []
    if snapshotprofile:
        output_keys.append('profile')
        profiles = gandi.snapshotprofile.list()

    result = gandi.disk.list(options)
    vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])

    # filter results per attached/detached
    disks = []
    for disk in result:
        if attached and not disk['vms_id']:
            continue
        if detached and disk['vms_id']:
            continue
        disks.append(disk)

    for num, disk in enumerate(disks):
        if num:
            gandi.separator_line()
        output_disk(gandi, disk, [], vms, profiles, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def info(gandi, resource):
    """ Display information about a disk.

    Resource can be a disk name or ID
    """
    output_keys = ['name', 'state', 'size', 'type', 'id', 'dc', 'vm',
                   'profile', 'kernel', 'cmdline']

    resource = sorted(tuple(set(resource)))
    vms = dict([(vm['id'], vm) for vm in gandi.iaas.list()])
    datacenters = gandi.datacenter.list()

    result = []
    for num, item in enumerate(resource):
        if num:
            gandi.separator_line()
        disk = gandi.disk.info(item)
        output_disk(gandi, disk, datacenters, vms, [], output_keys)
        result.append(disk)

    return result


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
@click.argument('resource', nargs=-1, required=True)
def detach(gandi, resource, background, force):
    """ Detach disks from currectly attached vm.

    Resource can be a disk name, or ID
    """
    resource = sorted(tuple(set(resource)))
    if not force:
        proceed = click.confirm('Are you sure you want to detach %s?' %
                                ', '.join(resource))
        if not proceed:
            return

    result = gandi.disk.detach(resource, background)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('-r', '--read-only', default=False, is_flag=True,
              help='Attach disk as read-only')
@click.option('--position', '-p', type=click.INT,
              help='Position where disk should be attached: 0 for system disk.'
                   ' If there is already a disk attached at the specified'
                   ' position, it will be swapped.')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
@click.argument('disk', nargs=1, required=True)
@click.argument('vm', nargs=1, required=True)
def attach(gandi, disk, vm, position, read_only, background, force):
    """ Attach disk to vm.

    disk can be a disk name, or ID
    vm can be a vm name, or ID
    """
    if not force:
        proceed = click.confirm("Are you sure you want to attach disk '%s'"
                                " to vm '%s'?" % (disk, vm))
        if not proceed:
            return

    disk_info = gandi.disk.info(disk)
    attached = disk_info.get('vms_id', False)
    if attached and not force:
        gandi.echo('This disk is still attached')
        proceed = click.confirm('Are you sure you want to detach %s?' % disk)

        if not proceed:
            return

    result = gandi.disk.attach(disk, vm, background, position, read_only)
    if background and result:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--cmdline', type=click.STRING, default=None,
              help='Kernel cmdline.')
@click.option('--kernel', type=KERNEL, default=None, help='Kernel for disk.')
@click.option('--name', type=click.STRING, default=None, help='Disk name.')
@click.option('--size', default=None, metavar='[+]SIZE[M|G|T]', type=SIZE,
              help=('Disk size. A size suffix (M for megabytes up to T for '
                    'terabytes) is optional, megabytes is the default if no '
                    'suffix is present. A prefix + is optionnal, if provided '
                    'size value will be added to current disk size, default '
                    'is to set directly new disk size.'),
              callback=disk_check_size)
@click.option('--snapshotprofile', help='Selected snapshot profile.',
              default=None, type=SNAPSHOTPROFILE_VM)
@click.option('--delete-snapshotprofile', default=False, is_flag=True,
              help='Remove snapshot profile associated to this disk.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, cmdline, kernel, name, size,
           snapshotprofile, delete_snapshotprofile, background):
    """ Update a disk.

    Resource can be a disk name, or ID
    """
    if snapshotprofile and delete_snapshotprofile:
        raise UsageError('You must not set snapshotprofile and '
                         'delete-snapshotprofile.')

    if delete_snapshotprofile:
        snapshotprofile = ''

    result = gandi.disk.update(resource, name, size, snapshotprofile,
                               background, cmdline, kernel)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, resource, force, background):
    """ Delete a disk. """
    output_keys = ['id', 'type', 'step']

    resource = sorted(tuple(set(resource)))
    if not force:
        disk_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm('Are you sure you want to delete disk %s?'
                                % disk_info)

        if not proceed:
            return

    opers = gandi.disk.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--name', type=click.STRING, default=None,
              help='Disk name, will be generated if not provided.')
@click.option('--vm', default=None, type=click.STRING,
              help='Attach the newly created disk to the vm.')
@click.option('--size', default='3072', metavar='SIZE[M|G|T]', type=SIZE,
              help=('Disk size. A size suffix (M for megabytes up to T for '
                    'terabytes) is optional, megabytes is the default if no '
                    'suffix is present.'),
              callback=disk_check_size)
@click.option('--snapshotprofile', help='Selected snapshot profile.',
              default=None, type=SNAPSHOTPROFILE_VM)
@click.option('--source', default=None, type=DISK_IMAGE,
              help='Create a disk from a disk or a snapshot.')
@option('--datacenter', type=DATACENTER, default='FR-SD3',
        help='Datacenter where the disk will be created.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, name, vm, size, snapshotprofile, datacenter, source,
           background):
    """ Create a new disk. """
    try:
        gandi.datacenter.is_opened(datacenter, 'iaas')
    except DatacenterLimited as exc:
        gandi.echo('/!\ Datacenter %s will be closed on %s, '
                   'please consider using another datacenter.' %
                   (datacenter, exc.date))

    if vm:
        vm_dc = gandi.iaas.info(vm)
        vm_dc_id = vm_dc['datacenter_id']
        dc_id = int(gandi.datacenter.usable_id(datacenter))
        if vm_dc_id != dc_id:
            gandi.echo('/!\ VM %s datacenter will be used instead of %s.'
                       % (vm, datacenter))
        datacenter = vm_dc_id

    output_keys = ['id', 'type', 'step']
    name = name or randomstring('vdi')

    disk_type = 'data'
    oper = gandi.disk.create(name, vm, size, snapshotprofile, datacenter,
                             source, disk_type, background)

    if background:
        output_generic(gandi, oper, output_keys)

    return oper


@cli.command()
@click.option('--name', type=click.STRING, default=None,
              help='Snapshot name, will be generated if not provided.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource')
@pass_gandi
def snapshot(gandi, name, resource, background):
    """ Create a snapshot on the fly. """
    name = name or randomstring('snp')

    source_info = gandi.disk.info(resource)
    datacenter = source_info['datacenter_id']
    result = gandi.disk.create(name, None, None, None, datacenter, resource,
                               'snapshot', background)

    if background:
        gandi.pretty_echo(result)
    return result


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', required=True)
@pass_gandi
def rollback(gandi, resource, background):
    """ Rollback a disk from a snapshot. """
    result = gandi.disk.rollback(resource, background)

    if background:
        gandi.pretty_echo(result)
    return result
