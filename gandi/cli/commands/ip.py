""" Ip namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_ip
from gandi.cli.core.params import (option, pass_gandi, DATACENTER,
                                   IP_TYPE, option, IntChoice)


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.option('--type', default=None, type=IP_TYPE,
              help='Filter by type.')
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--attached', help='Only display attached ip.', is_flag=True)
@click.option('--detached', help='Only display detached ip.', is_flag=True)
@click.option('--version', help='Display ip version.', is_flag=True)
@click.option('--reverse', help='Display ip reverse.', is_flag=True)
@click.option('--vm', help='Display ip vm.', is_flag=True)
@pass_gandi
def list(gandi, datacenter, type, id, attached, detached, version, reverse,
         vm):
    """List ips."""
    if attached and detached:
        gandi.echo("You can't set --attached and --detached at the same time.")
        return

    output_keys = ['ip', 'state', 'dc', 'type']
    if id:
        output_keys.append('id')
    if version:
        output_keys.append('version')
    if vm:
        output_keys.append('vm')
    if reverse:
        output_keys.append('reverse')

    options = {}
    if datacenter:
        datacenter_id = int(Datacenter.usable_id(datacenter))
        options['datacenter_id'] = datacenter_id

    iface_options = {}
    if type:
        iface_options['type'] = type
    if attached:
        iface_options['state'] = 'used'
    elif detached:
        iface_options['state'] = 'free'

    if iface_options:
        ifaces = gandi.iface.list(iface_options)
        options['iface_id'] = [iface['id'] for iface in ifaces]

    datacenters = gandi.datacenter.list()

    ips = gandi.ip.list(options)
    ifaces = dict([(iface['id'], iface)
                   for iface in gandi.iface.list(datacenter)])
    vms = dict([(vm['id'], vm)
                for vm in gandi.iaas.list(datacenter)])

    for num, ip_ in enumerate(ips):
        if num:
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


@cli.command()
@click.argument('ip')
@click.argument('vm')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def attach(gandi, ip, vm, background, force):
    """Attach an ip to a vm.

    ip can be an ip id or ip
    vm can be a vm id or name.
    """
    return gandi.ip.attach(ip, vm, background, force)


@cli.command()
@option('--datacenter', type=DATACENTER, default='LU',
        help='Datacenter where the ip will be created.')
@option('--bandwidth', type=click.INT, default=102400,
        help="Network bandwidth in bit/s used to create the VM's first "
             "network interface.")
@option('--ip-version', type=IntChoice(['4', '6']), default=4,
        help='Version of created IP.')
@click.option('--vlan', help='The vlan to which attach this ip if any.')
@click.option('--ip', help='The ip if you try to create a private ip.')
@click.option('--attach', help='The vm you want to attach if any.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, datacenter, bandwidth, ip_version, vlan, ip, attach,
           background):
    """Create a public or private ip
    """
    if ip_version != 4 and vlan:
        click.echo('You must have an --ip-version to 4 when having a vlan.')
        return

    if ip and not vlan:
        click.echo('You must have a --vlan when giving an --ip.')
        return

    vm_ = gandi.iaas.info(attach) if attach else None

    if datacenter and vm_:
        dc_id = gandi.datacenter.usable_id(datacenter)
        if dc_id != vm_['datacenter_id']:
            click.echo('The datacenter you give is not the same the vm you'
                       ' want to attach.')
            return

    if not datacenter:
        if vm_:
            datacenter = vm_['datacenter_id']
        else:
            click.echo('The vm you want to attach is not in %s datacenter.'
                       % datacenter)
            return

    return gandi.ip.create(ip_version, datacenter, bandwidth, attach,
                           vlan, ip, background)


@cli.command()
@click.argument('resource')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def detach(gandi, resource, background, force):
    """Detach an ip from it's currently attached vm.

    resource can be an ip id or ip.
    """
    if not force:
        proceed = click.confirm('Are you sure to detach ip %s?' % resource)
        if not proceed:
            return

    return gandi.ip.detach(resource, background, force)


@cli.command()
@click.argument('resource')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def delete(gandi, resource, background, force):
    """Delete an ip (and detach it from it's currently attached vm).

    resource can be an ip id or ip.
    """
    if not force:
        proceed = click.confirm('Are you sure to delete ip %s?' % resource)
        if not proceed:
            return

    return gandi.ip.delete(resource, background, force)
