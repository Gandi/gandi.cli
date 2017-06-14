""" Vlan namespace commands. """

import click
from IPy import IP

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_vlan, output_generic, output_iface, output_ip, output_line,
    DatacenterLimited
)
from gandi.cli.core.params import option, pass_gandi, DATACENTER


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--subnet', help='Display subnets.', is_flag=True)
@click.option('--gateway', help='Display gateway.', is_flag=True)
@pass_gandi
def list(gandi, datacenter, id, subnet, gateway):
    """List vlans."""
    output_keys = ['name', 'state', 'dc']
    if id:
        output_keys.append('id')
    if subnet:
        output_keys.append('subnet')
    if gateway:
        output_keys.append('gateway')

    datacenters = gandi.datacenter.list()

    vlans = gandi.vlan.list(datacenter)
    for num, vlan in enumerate(vlans):
        if num:
            gandi.separator_line()
        output_vlan(gandi, vlan, datacenters, output_keys)

    return vlans


@cli.command()
@click.option('--ip', help='Display ips.', is_flag=True)
@click.argument('resource')
@pass_gandi
def info(gandi, resource, ip):
    """Display information about a vlan."""
    output_keys = ['name', 'state', 'dc', 'subnet', 'gateway']

    datacenters = gandi.datacenter.list()

    vlan = gandi.vlan.info(resource)

    gateway = vlan['gateway']
    if not ip:
        output_vlan(gandi, vlan, datacenters, output_keys, justify=11)
        return vlan

    gateway_exists = False

    vms = dict([(vm_['id'], vm_) for vm_ in gandi.iaas.list()])
    ifaces = gandi.vlan.ifaces(resource)

    for iface in ifaces:
        for ip in iface['ips']:
            if gateway == ip['ip']:
                gateway_exists = True

    if gateway_exists:
        vlan.pop('gateway')
    else:
        vlan['gateway'] = ("%s don't exists" % gateway if gateway
                           else 'none')

    output_vlan(gandi, vlan, datacenters, output_keys, justify=11)

    output_keys = ['vm', 'bandwidth']
    for iface in ifaces:
        gandi.separator_line()
        output_iface(gandi, iface, datacenters, vms, output_keys,
                     justify=11)
        for ip in iface['ips']:
            output_ip(gandi, ip, None, None, None, ['ip'])
            if gateway == ip['ip']:
                output_line(gandi, 'gateway', 'true', justify=11)

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
@option('--datacenter', type=DATACENTER, default='FR-SD3',
        help='Datacenter where the vlan will be spawned.')
@click.option('--subnet', help='The vlan subnet.')
@click.option('--gateway', help='The vlan gateway.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
def create(gandi, name, datacenter, subnet, gateway, background):
    """ Create a new vlan """
    try:
        gandi.datacenter.is_opened(datacenter, 'iaas')
    except DatacenterLimited as exc:
        gandi.echo('/!\ Datacenter %s will be closed on %s, '
                   'please consider using another datacenter.' %
                   (datacenter, exc.date))

    result = gandi.vlan.create(name, datacenter, subnet, gateway, background)

    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--name', help='Name of the vlan.')
@click.option('--gateway', help='Gateway of the vlan.')
@click.option('--create', default=False, is_flag=True,
              help='If gateway is a vm and does not have any ip in the good '
                   'vlan, we will start by putting an ip in the vlan.')
@option('--bandwidth', type=click.INT, default=102400,
        help="Network bandwidth in kbit/s used to create the VM's ip in this "
             'vlan.')
@click.argument('resource')
@pass_gandi
def update(gandi, resource, name, gateway, create, bandwidth):
    """ Update a vlan

    ``gateway`` can be a vm name or id, or an ip.
    """
    params = {}
    if name:
        params['name'] = name

    vlan_id = gandi.vlan.usable_id(resource)

    try:
        if gateway:
            IP(gateway)
            params['gateway'] = gateway
    except ValueError:
        vm = gandi.iaas.info(gateway)
        ips = [ip for sublist in
               [[ip['ip'] for ip in iface['ips'] if ip['version'] == 4]
                for iface in vm['ifaces']
                if iface['vlan'] and iface['vlan'].get('id') == vlan_id]
               for ip in sublist]

        if len(ips) > 1:
            gandi.echo("This vm has two ips in the vlan, don't know which one"
                       ' to choose (%s)' % (', '.join(ips)))
            return

        if not ips and not create:
            gandi.echo("Can't find '%s' in '%s' vlan" % (gateway, resource))
            return

        if not ips and create:
            gandi.echo('Will create a new ip in this vlan for vm %s' % gateway)
            oper = gandi.ip.create('4', vm['datacenter_id'], bandwidth,
                                   vm['hostname'], resource)

            iface_id = oper['iface_id']
            iface = gandi.iface.info(iface_id)
            ips = [ip['ip'] for ip in iface['ips'] if ip['version'] == 4]

        params['gateway'] = ips[0]

    result = gandi.vlan.update(resource, params)

    return result
