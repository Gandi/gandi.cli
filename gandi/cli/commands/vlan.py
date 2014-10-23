""" Vlan namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_vlan, output_generic, output_iface
from gandi.cli.core.params import option, pass_gandi, DATACENTER


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
@click.option('--iface', help='Display ifaces.', is_flag=True)
@click.argument('resource')
@pass_gandi
def info(gandi, resource, iface):
    """Display information about a vlan."""
    output_keys = ['name', 'state', 'dc', 'subnet', 'gateway']

    datacenters = gandi.datacenter.list()

    vlan = gandi.vlan.info(resource)
    output_vlan(gandi, vlan, datacenters, output_keys)

    if iface:
        output_keys = ['id', 'bandwidth', 'type', 'state', 'vm']
        vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])
        ifaces = gandi.vlan.ifaces(resource)
        for iface in ifaces:
            gandi.separator_line()
            output_iface(gandi, iface, datacenters, vms, output_keys)

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

    Resource can be a vlan name or an ID
    """
    output_keys = ['id', 'type', 'step']

    possible_resources = gandi.vlan.resource_list()
    for item in resource:
        if item not in possible_resources:
            gandi.echo('Sorry vlan %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' %
                       possible_resources)
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


@cli.command()
@click.option('--name', required=True, help='Name of the vlan.')
@option('--datacenter', type=DATACENTER, default='LU',
        help='Datacenter where the vlan will be spawned.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, name, datacenter, background):
    """ Create a new vlan """
    result = gandi.vlan.create(name, datacenter, background)

    if not result:
        return

    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--name', required=True, help='Name of the vlan.')
@click.argument('resource')
@pass_gandi
def update(gandi, resource, name):
    """ Update a vlan """
    result = gandi.vlan.update(resource, name)

    if not result:
        return

    return result
