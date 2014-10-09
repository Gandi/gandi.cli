""" Disk namespace commands. """

import click

from gandi.cli.core.cli import cli, compatcallback
from gandi.cli.core.utils import output_disk, output_generic, randomstring
from gandi.cli.core.params import (pass_gandi, DATACENTER, SNAPSHOTPROFILE,
                                   KERNEL, option)


@cli.command()
@click.option('--only-data', help='Only display data disks.', is_flag=True)
@click.option('--only-snapshot', help='Only display snapshots.', is_flag=True)
@click.option('--type', help='Display types.', is_flag=True)
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--vm', help='Display vms.', is_flag=True)
@click.option('--snapshotprofile', help='Display snapshot profile.',
              is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, only_data, only_snapshot, type, id, vm, snapshotprofile,
         limit):
    """ List disks. """
    options = {
        'items_per_page': limit,
    }

    if only_data:
        options.setdefault('type', []).append('data')
    if only_snapshot:
        options.setdefault('type', []).append('snapshot')

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

    for disk in result:
        gandi.separator_line()
        output_disk(gandi, disk, [], vms, profiles, output_keys)

    return result


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """ Display information about a disk.

    Resource can be a disk name or ID
    """
    output_keys = ['name', 'state', 'size', 'type', 'id', 'dc', 'vm',
                   'profile']

    disk = gandi.disk.info(resource)
    vms = dict([(vm['id'], vm) for vm in gandi.iaas.list()])
    output_disk(gandi, disk, [], vms, [], output_keys)

    return disk


@compatcallback
def check_size(ctx, param, value):
    """ Validation callback for size parameter."""
    if value and value % 1024:
        raise click.ClickException('Size must be a multiple of 1024.')
    return value


@cli.command()
@click.option('--cmdline', type=click.STRING, default=None,
              help='Kernel cmdline.')
@click.option('--kernel', type=KERNEL, default=None, help='Kernel for disk.')
@click.option('--name', type=click.STRING, default=None, help='Disk name.')
@click.option('--size', default=None, type=click.INT, help='Disk size.',
              callback=check_size)
@click.option('--snapshotprofile', help='Selected snapshot profile.',
              default=None, type=SNAPSHOTPROFILE)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, cmdline, kernel, name, size,
           snapshotprofile, background):
    """ Update a disk.

    Resource can be a disk name, or ID
    """
    try:
        snapshotprofile = int(snapshotprofile) if snapshotprofile else None
    except ValueError:
        gandi.echo('--snapshotprofile must be an existing profile.')
        gandi.echo('get all existing profiles with :')
        gandi.echo('  gandi snapshotprofile list')
        return

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
@click.argument('resource', required=True)
@pass_gandi
def delete(gandi, resource, force, background):
    """ Delete a disk. """
    output_keys = ['name', 'disk_id', 'state', 'date_creation']
    if not force:
        proceed = click.confirm('Are you sure to delete disk %s?' % resource)

        if not proceed:
            return

    opers = gandi.disk.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--name', type=click.STRING, default=None, help='Disk name.')
@click.option('--vm', default=None, type=click.STRING,
              help='Attach the newly created disk to the vm.')
@click.option('--size', default=3072, type=click.INT, help='Disk size.',
              callback=check_size)
@click.option('--snapshotprofile', help='Selected snapshot profile.',
              default=None, type=SNAPSHOTPROFILE)
@option('--datacenter', type=DATACENTER, default='LU',
        help='Datacenter where the VM will be spawned.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, name, vm, size, snapshotprofile, datacenter, background):
    """ Create a new disk. """
    try:
        snapshotprofile = int(snapshotprofile) if snapshotprofile else None
    except ValueError:
        gandi.echo('--snapshotprofile must be an existing profile.')
        gandi.echo('get all existing profiles with :')
        gandi.echo('  gandi snapshotprofile list')
        return

    name = name or randomstring()

    result = gandi.disk.create(name, vm, size, snapshotprofile, datacenter,
                               background)

    if background:
        gandi.pretty_echo(result)

    return result
