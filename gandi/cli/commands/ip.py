""" Ip namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_ip, output_generic
from gandi.cli.core.params import option, pass_gandi, DATACENTER, IP_TYPE


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.option('--type', default=None, type=IP_TYPE,
              help='Filter by type.')
@click.option('--version', help='Display ip version.', is_flag=True)
@click.option('--reverse', help='Display ip reverse.', is_flag=True)
@click.option('--vm', help='Display ip vm.', is_flag=True)
@pass_gandi
def list(gandi, datacenter, type, version, reverse, vm):
    """List ips."""
    output_keys = ['ip', 'state', 'dc', 'type']
    if version:
        output_keys.append('version')
    if vm:
        output_keys.append('vm')
    if reverse:
        output_keys.append('reverse')

    datacenters = gandi.datacenter.list()

    ips = gandi.ip.list(datacenter, type)
    ifaces = dict([(iface['id'], iface)
                   for iface in gandi.iface.list(datacenter)])
    vms = dict([(vm['id'], vm)
                for vm in gandi.iaas.list(datacenter)])

    for ip_ in ips:
        gandi.separator_line()
        output_ip(gandi, ip_, datacenters, vms, ifaces, output_keys)

    return ips


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about an ip.

    Resource can be an ip or id.
    """
    output_keys = ['ip', 'state', 'dc', 'type', 'vm']

    datacenters = gandi.datacenter.list()

    ip = gandi.ip.info(resource)
    iface = gandi.iface.info(ip['iface_id'])
    vms = None
    if iface.get('vm_id'):
        vm = gandi.iaas.info(iface['vm_id'])
        vms = {vm['id']: vm}

    output_ip(gandi, ip, datacenters, vms, {iface['id']: iface},
              output_keys)

    return ip
