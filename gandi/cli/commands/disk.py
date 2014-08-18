import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_disk, output_generic, randomstring
from gandi.cli.core.params import pass_gandi, DATACENTER, option


@cli.command()
@click.option('--only-data', help='only display data disks', is_flag=True)
@click.option('--only-snapshot', help='only display snapshots', is_flag=True)
@click.option('--type', help='display types', is_flag=True)
@click.option('--id', help='display ids', is_flag=True)
@click.option('--vm', help='display vms', is_flag=True)
@click.option('--snapshot-profile', help='display snapshot profile',
              is_flag=True)
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, only_data, only_snapshot, type, id, vm, snapshot_profile,
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
    if snapshot_profile:
        output_keys.append('profile')
        profiles = gandi.snapshotprofile.list()

    result = gandi.disk.list(options)
    vms = dict([(vm['id'], vm) for vm in gandi.iaas.list()])

    for disk in result:
        gandi.separator_line()
        output_disk(gandi, disk, [], vms, profiles, output_keys)

    return result


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """ Display information about a disk.

    Resource can be a disk name, or it's ID
    """
    output_keys = ['name', 'state', 'size', 'type', 'id', 'dc', 'vm', 'profile']

    disk = gandi.disk.info(resource)
    vms = dict([(vm['id'], vm) for vm in gandi.iaas.list()])
    output_disk(gandi, disk, [], vms, [], output_keys)

    return disk


@cli.command()
@click.option('--name', type=click.STRING, default=None,
              help='Name of the PaaS instance')
@click.option('--size', default=None, type=click.INT,
              help='Size of the PaaS instance')
@click.option('--snapshot-profile', help='Selected napshot profile',
              default=None)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, name, size, snapshot_profile, background):
    """ Update a disk.

    Resource can be a disk name, or it's ID
    """
    try:
        snapshot_profile = int(snapshot_profile)
    except ValueError:
        gandi.echo('--snapshot-profile must be an existing profile.')
        gandi.echo('get all existing profiles with :')
        gandi.echo('  gandi snapshotprofile list')
        return

    result = gandi.disk.update(resource, name, size, snapshot_profile,
                               background)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
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
