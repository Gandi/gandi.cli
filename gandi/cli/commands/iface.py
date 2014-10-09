""" Iface namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_iface
from gandi.cli.core.params import option, pass_gandi, IntChoice, DATACENTER


@cli.command()
@click.option('--vm', help='Display vms.', is_flag=True)
@click.option('--vlan', help='Display vlans.', is_flag=True)
@pass_gandi
def list(gandi, vm, vlan):
    """List ifaces."""
    output_keys = ['id', 'num', 'type', 'state', 'dc', 'bandwidth']
    if vm:
        output_keys.append('vm')
    if vlan:
        output_keys.append('vlan_')

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

    Resource can be an iface ID
    """
    output_keys = ['num', 'type', 'state', 'dc', 'bandwidth', 'vm', 'vlan_']

    datacenters = gandi.datacenter.list()
    vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])

    iface = gandi.iface.info(resource)
    output_iface(gandi, iface, datacenters, vms, output_keys)

    output_ips = ['ip', 'reverse', 'version']
    for ip in iface['ips']:
        gandi.separator_line()
        output_generic(gandi, ip, output_ips)

    return iface


@cli.command()
@option('--datacenter', type=DATACENTER, default='LU',
        help='Datacenter where the iface will be spawned.')
@option('--ip-version', type=IntChoice(['4', '6']), default='4',
        help='Version of created IP.')
@option('--bandwidth', type=click.INT, default=102400,
        help='Network bandwidth in bit/s to be used for this iface.')
@click.option('--vlan', default=None, type=click.STRING,
              help='Attach the newly created iface to the vlan.')
@click.option('--vm', default=None, type=click.STRING,
              help='Attach the newly created iface to the vm.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, ip_version, datacenter, bandwidth, vlan, vm, background):
    """ Create a new iface """
    result = gandi.iface.create(ip_version, datacenter, bandwidth, vlan, vm,
                                background)

    if not result:
        return

    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, background, force, resource):
    """Delete an iface.

    Resource can be an iface ID
    """
    output_keys = ['id', 'type', 'step']

    iface_list = gandi.iface.list()
    iface_idlist = [iface['id'] for iface in iface_list]
    for item in resource:
        item_ = int(item)
        if item_ not in iface_idlist:
            gandi.echo('Sorry iface %d does not exist' % item_)
            gandi.echo('Please use one of the following: %s' % iface_idlist)
            return

    if not force:
        iface_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm('Are you sure to delete iface %s?' %
                                iface_info)

        if not proceed:
            return

    opers = gandi.iface.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
