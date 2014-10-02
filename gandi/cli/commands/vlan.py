""" Vlan namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_vlan
from gandi.cli.core.params import pass_gandi, DATACENTER


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.option('--id', help='Display ids.', is_flag=True)
@pass_gandi
def list(gandi, datacenter, id):
    """List vlans."""
    output_keys = ['name', 'state', 'dc']
    if id:
        output_keys.append('id')

    datacenters = gandi.datacenter.list()

    vlans = gandi.vlan.list(datacenter)
    for vlan in vlans:
        gandi.separator_line()
        output_vlan(gandi, vlan, datacenters, output_keys)

    return vlans


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about a vlan."""
    output_keys = ['name', 'state', 'dc']

    datacenters = gandi.datacenter.list()

    vlan = gandi.vlan.info(resource)
    output_vlan(gandi, vlan, datacenters, output_keys)

    return vlan
