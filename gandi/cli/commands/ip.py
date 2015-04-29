""" Ip namespace commands. """

import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_ip
from gandi.cli.core.params import (pass_gandi, DATACENTER,
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
@click.option('--vlan', default=None, help='Filter by vlan.')
@pass_gandi
def list(gandi, datacenter, type, id, attached, detached, version, reverse,
         vm, vlan):
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
    opt_dc = {}
    if datacenter:
        datacenter_id = int(gandi.datacenter.usable_id(datacenter))
        options['datacenter_id'] = datacenter_id
        opt_dc = {'datacenter_id': datacenter_id}

    iface_options = {}
    if type:
        iface_options['type'] = type
    if vlan:
        iface_options['vlan'] = vlan
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
                   for iface in gandi.iface.list(opt_dc)])
    vms = dict([(vm['id'], vm)
                for vm in gandi.iaas.list(opt_dc)])

    for num, ip_ in enumerate(ips):
        if num:
            gandi.separator_line()
        output_ip(gandi, ip_, datacenters, vms, ifaces, output_keys)

    return ips


@cli.command()
@click.argument('resources', nargs=-1)
@pass_gandi
def info(gandi, resources):
    """Display information about one or more IPs

    Resource can be one or more IPs or IDs.
    """
    output_keys = ['ip', 'state', 'dc', 'type', 'vm', 'reverse']
    justify = 14

    resources = sorted(tuple(set(resources)))
    datacenters = gandi.datacenter.list()

    ret = []
    for num, item in enumerate(resources):
        if num:
            gandi.separator_line()
        try:
            ip = gandi.ip.info(item)
            ret.append(ip)
            iface = gandi.iface.info(ip['iface_id'])
            vms = None
            if iface.get('vm_id'):
                vm = gandi.iaas.info(iface['vm_id'])
                vms = {vm['id']: vm}
            output_ip(gandi, ip, datacenters, vms, {iface['id']: iface},
                      output_keys)
        except:
            gandi.echo("Error looking up ip %s, skipping" % item)
            # TODO: should be more verbose here (possible reasons: "unknown identifier"...)

    return ret


@cli.command()
@click.argument('ip')
@click.option('--reverse', help='Update reverse (PTR record) for this IP')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def update(gandi, ip, reverse, background):
    """Update an ip."""
    if not reverse:
        return
    return gandi.ip.update(ip, {'reverse': reverse}, background)


@cli.command()
@click.argument('resources', nargs=-1)
@click.argument('vm')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def attach(gandi, resources, vm, background, force):
    """Attach one or more IPs to a vm.

    ip can be an ip id or ip.
    vm can be a vm id or name.
    """

    resources = sorted(tuple(set(resources)))
    ret = []

    for num, item in enumerate(resources):
        try:
            ip_ = gandi.ip.info(item)
            vm_ = gandi.iaas.info(vm)
        except UsageError:
            gandi.error("Can't find this ip %s" % item)
            break

        iface = gandi.iface.info(ip_['iface_id'])
        if iface.get('vm_id'):
            if vm_ and iface['vm_id'] == vm_.get('id'):
                gandi.echo('IP %s is already attached to vm %s.' %
                           (ip_['ip'], iface['vm_id']))
                continue

            if not force:
                proceed = click.confirm('Are you sure you want to detach'
                                        ' %s from vm %s?' %
                                        (ip_['ip'], iface['vm_id']))
                if not proceed:
                    continue

        gandi.echo('Attaching IP %s to VM %s...' %
                    (ip_['ip'], iface['vm_id']))

        ret.append(gandi.ip.attach(item, vm, background, force))

    return ret 


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
        gandi.echo('You must have an --ip-version to 4 when having a vlan.')
        return

    if ip and not vlan:
        gandi.echo('You must have a --vlan when giving an --ip.')
        return

    vm_ = gandi.iaas.info(attach) if attach else None

    if datacenter and vm_:
        dc_id = gandi.datacenter.usable_id(datacenter)
        if dc_id != vm_['datacenter_id']:
            gandi.echo('The datacenter you give is not the same the vm you'
                       ' want to attach.')
            return

    if not datacenter:
        if vm_:
            datacenter = vm_['datacenter_id']
        else:
            gandi.echo('The vm you want to attach this IP to is not in %s datacenter.'
                       % datacenter)
            return

    return gandi.ip.create(ip_version, datacenter, bandwidth, attach,
                           vlan, ip, background)


@cli.command()
@click.argument('resources', nargs=-1)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def detach(gandi, resources, background, force):
    """Detach one or more IPs from the vm they are attached to.

    resource can be an ip id or ip.
    """
    resources = sorted(tuple(set(resources)))
    ret = []

    for num, item in enumerate(resources):
        if not force:
            proceed = click.confirm('Are you sure you want to detach ip %s?' % item)
            if not proceed:
                continue
        ret.append(gandi.ip.detach(item, background, force))
    return ret


@cli.command()
@click.argument('resources', nargs=-1)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def delete(gandi, resources, background, force):
    """Delete one or more IPs (after detaching them from VMs if necessary).

    resource can be an ip id or ip.
    """

    resources = sorted(tuple(set(resources)))
    possible_resources = gandi.ip.resource_list()

    # check that each IP can be deleted
    for item in resources:
        if item not in possible_resources:
            gandi.echo('Sorry interface %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' %
                        possible_resources)
            return

    if not force:
        gandi.echo("The following IPs will be deleted:")
        [ gandi.echo(ip) for ip in resources ]
        proceed = click.confirm('Do you want to proceed?')
        if not proceed:
            return

    gandi.echo("Deleting: %s" % resources)
    return gandi.ip.delete(resources, background, force)
