""" Vlan namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_vlan, output_generic
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


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, background, force, resource):
    """Delete a vlan.

    Resource can be a vlan name, or an ID
    """
    output_keys = ['id', 'type', 'step']

    vlan_list = gandi.vlan.list()
    vlan_namelist = [vlan['name'] for vlan in vlan_list]
    for item in resource:
        if item not in vlan_namelist:
            gandi.echo('Sorry vlan %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' % vlan_namelist)
            return

    if not force:
        vlan_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm('Are you sure to delete vlan %s?' %
                                vlan_info)

        if not proceed:
            return

    opers = gandi.vlan.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
