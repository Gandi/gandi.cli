
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import (
    output_vm, output_image, output_oper, output_datacenter,
)


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@pass_gandi
def list(gandi, state, id):
    """List virtual machines."""

    options = {}
    if state:
        options['state'] = state

    output_keys = ['hostname', 'state']
    if id:
        output_keys.append('id')

    datacenters = gandi.datacenter.list()
    result = gandi.iaas.list(options)
    for vm in result:
        gandi.echo('-' * 10)
        output_vm(gandi, vm, datacenters, output_keys)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """Display information about a virtual machine."""

    output_keys = ['hostname', 'state', 'cores', 'memory', 'console',
                   'datacenter']

    datacenters = gandi.datacenter.list()
    vm = gandi.iaas.info(id)
    output_vm(gandi, vm, datacenters, output_keys)

    return vm


@cli.command()
@click.argument('id')
@pass_gandi
def stop(gandi, id):
    """Stop a virtual machine."""

    output_keys = ['id', 'type', 'step']

    oper = gandi.iaas.stop(id)
    output_oper(gandi, oper, output_keys)

    return oper


@cli.command()
@click.argument('id')
@pass_gandi
def start(gandi, id):
    """Start a virtual machine."""

    output_keys = ['id', 'type', 'step']

    oper = gandi.iaas.start(id)
    output_oper(gandi, oper, output_keys)

    return oper


@cli.command()
@click.argument('id')
@pass_gandi
def reboot(gandi, id):
    """Reboot a virtual machine."""

    output_keys = ['id', 'type', 'step']

    oper = gandi.iaas.reboot(id)
    output_oper(gandi, oper, output_keys)

    return oper


@cli.command()
@click.option('--force', '-f', multiple=True, is_flag=True,
              help='force the vm to stop')
@click.argument('id')
@pass_gandi
def delete(gandi, id, force):
    """Delete a virtual machine."""

    output_keys = ['id', 'type', 'step']

    vm = gandi.iaas.info(id)
    if vm['state'] == 'running':
        if not force:
            force_stop = click.confirm('VM %s is running, stop it ?' % id)

        if force or force_stop:
            interactive = True
            gandi.iaas.stop(id, interactive=interactive)

    oper = gandi.iaas.delete(id)
    output_oper(gandi, oper, output_keys)

    return oper


@cli.command()
@click.option('--datacenter', default=None,
              help='name|iso|country|id of the datacenter where the VM will be spawned')
@click.option('--memory', type=click.INT, default=None,
              help='quantity of RAM in Megabytes to allocate')
@click.option('--cores', type=click.INT, default=None,
              help='number of cpu')
@click.option('--ip-version', type=click.INT, default=None,
              help='version of the created IP, can be 4 or 6')
@click.option('--bandwidth', type=click.INT, default=None,
              help="network bandwidth in bit/s used to create the VM's first "
                   "network interface")
@click.option('--login', default=None,
              help='login to create on the VM')
@click.option('--password', default=None,
              help='password to set to the root account and the created login')
@click.option('--hostname', default='tempo',
              help='hostname of the VM')
@click.option('--image', default=None,
              help='label (or id) of disk image used to boot the vm')
@click.option('--run', default=None,
              help='shell command that will run at the first startup of a VM.'
                   'This command will run with root privileges in the ``/`` '
                   'directory at the end of its boot: network interfaces and '
                   'disks are mounted')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.option('--ssh-key', default=None,
              help='Authorize ssh authentication for the given ssh key')
@pass_gandi
def create(gandi, datacenter, memory, cores, ip_version, bandwidth, login,
           password, hostname, image, run, interactive, ssh_key):
    """Create a new virtual machine.

    you can specify a configuration entry named 'ssh_key' containing
    path to your ssh_key file

    >>> gandi config ssh_key ~/.ssh/id_rsa.pub

    to know which disk image label (or id) to use as image

    >>> gandi images

    to know which datacenter name|iso|country|id to use as datacenter

    >>> gandi datacenters

    """

    result = gandi.iaas.create(datacenter, memory, cores, ip_version,
                               bandwidth, login, password, hostname,
                               image, run,
                               interactive, ssh_key)
    if not interactive:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--memory', type=click.INT, default=None,
              help='quantity of RAM in Megabytes to allocate')
@click.option('--cores', type=click.INT, default=None,
              help='number of cpu')
@click.option('--console', default=None, is_flag=True,
              help='activate the emergency console')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.argument('id')
@pass_gandi
def update(gandi, id, memory, cores, console, interactive):
    """Update a virtual machine."""

    result = gandi.iaas.update(id, memory, cores, console, interactive)
    if not interactive:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def console(gandi, id):
    """Open a console to virtual machine."""

    gandi.iaas.console(id)


@cli.command()
@click.option('--datacenter_id', type=click.INT, default=None,
              help='filter by id of datacenter')
@pass_gandi
def images(gandi, datacenter_id):
    """List available images."""

    output_keys = ['label', 'os_arch', 'kernel_version', 'disk_id',
                   'datacenter_id']

    result = gandi.image.list(datacenter_id)
    for image in result:
        gandi.echo('-' * 10)
        output_image(gandi, image, output_keys)

    return result


@cli.command()
@click.option('--id', help='display ids', is_flag=True)
@pass_gandi
def datacenters(gandi, id):
    """List available datacenters."""

    output_keys = ['iso', 'name', 'country']
    if id:
        output_keys.append('id')

    result = gandi.datacenter.list()
    for dc in result:
        gandi.echo('-' * 10)
        output_datacenter(gandi, dc, output_keys)

    return result
