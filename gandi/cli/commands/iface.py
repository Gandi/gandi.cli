""" Iface namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_iface
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--vm', help='Display vms.', is_flag=True)
@click.option('--vlan', help='Display vlans.', is_flag=True)
@pass_gandi
def list(gandi, id, ip, vm, vlan):
    """List ifaces."""
    output_keys = ['num', 'type', 'state', 'dc', 'bandwidth']
    if id:
        output_keys.append('id')
    if vm:
        output_keys.append('vm')
    if vlan:
        output_keys.append('vlan')

    datacenters = gandi.datacenter.list()
    vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])

    ifaces = gandi.iface.list()
    for iface in ifaces:
        gandi.separator_line()
        output_iface(gandi, iface, datacenters, vms, output_keys)

    return ifaces


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about a iface.

    Resource can be an iface num or ID
    """
    output_keys = ['num', 'type', 'state', 'dc', 'bandwidth', 'vm']

    datacenters = gandi.datacenter.list()
    vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])

    iface = gandi.iface.info(resource)
    output_iface(gandi, iface, datacenters, vms, output_keys)

    output_ips = ['ip', 'reverse', 'version']
    for ip in iface['ips']:
        gandi.separator_line()
        output_generic(gandi, ip, output_ips)

    return iface
