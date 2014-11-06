""" Snapshot profiles namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_snapshot_profile
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--only-paas', help='Only display PaaS profiles.', is_flag=True)
@click.option('--only-vm', help='Only display vm profile.s', is_flag=True)
@pass_gandi
def list(gandi, only_paas, only_vm):
    """ List snapshot profiles. """
    target = None
    if only_paas and not only_vm:
        target = 'paas'
    if only_vm and not only_paas:
        target = 'vm'

    output_keys = ['id', 'name', 'kept_total', 'target']
    result = gandi.snapshotprofile.list({}, target=target)

    for num, profile in enumerate(result):
        if num:
            gandi.separator_line()
        output_snapshot_profile(gandi, profile, output_keys)

    return result


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """ Display information about a snapshot profile.

    Resource can be a profile name or ID
    """
    output_keys = ['id', 'name', 'kept_total', 'target', 'quota_factor',
                   'schedules']

    result = gandi.snapshotprofile.info(resource)
    output_snapshot_profile(gandi, result, output_keys)
    return result
