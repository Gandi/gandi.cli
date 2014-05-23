
import click

from gandi.cli.__main__ import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import output_vm, read_ssh_key


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@pass_gandi
def list(gandi, state):
    """List virtual machines."""

    options = {}
    if state:
        options['state'] = state

    datacenters = gandi.datacenter.list()
    result = gandi.iaas.list(options)
    for vm in result:
        gandi.echo('-' * 10)
        output_vm(gandi, vm, datacenters)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """Display information about a virtual machine."""

    datacenters = gandi.datacenter.list()
    vm = gandi.iaas.info(id)
    output_vm(gandi, vm, datacenters)

    return vm


@cli.command()
@click.argument('id')
@pass_gandi
def stop(gandi, id):
    """Stop a virtual machine."""

    result = gandi.iaas.stop(id)
    gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def start(gandi, id):
    """Start a virtual machine."""

    result = gandi.iaas.start(id)
    gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def reboot(gandi, id):
    """Reboot a virtual machine."""

    result = gandi.iaas.reboot(id)
    gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def delete(gandi, id):
    """Delete a virtual machine."""

    result = gandi.iaas.delete(id)
    gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--datacenter_id', type=click.INT, default=None,
              help='id of the datacenter where the VM will be spawned')
@click.option('--memory', type=click.INT, default=None,
              help='quantity of RAM in Megabytes to allocate')
@click.option('--cores', type=click.INT, default=None,
              help='number of cpu')
@click.option('--ip_version', type=click.INT, default=None,
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
@click.option('--sys_disk_id', type=click.INT, default=None,
              help='id of disk image used to boot the vm')
@click.option('--run', default=None,
              help='shell command that will run at the first startup of a VM.'
                   'This command will run with root privileges in the ``/`` '
                   'directory at the end of its boot: network interfaces and '
                   'disks are mounted')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.argument('ssh_key', default=None, type=click.File('rb'), required=False,
                callback=read_ssh_key)
@pass_gandi
def create(gandi, datacenter_id, memory, cores, ip_version, bandwidth, login,
           password, hostname, sys_disk_id, run, interactive, ssh_key):
    """Create a new virtual machine.

    you can provide a ssh_key on command line calling this command as:

    >>> cat ~/.ssh/id_rsa.pub | gandi create -

    or specify a configuration entry named 'ssh_key_path' containing
    path to your ssh_key file

    >>> gandi config ssh_key_path ~/.ssh/id_rsa.pub

    to know which disk image id to use as sys_disk_id

    >>> gandi image.list

    """

    result = gandi.iaas.create(datacenter_id, memory, cores, ip_version,
                               bandwidth, login, password, hostname,
                               sys_disk_id, run,
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


@cli.command(name='image.list')
@click.option('--datacenter_id', type=click.INT, default=None,
              help='filter by id of datacenter')
@pass_gandi
def image_list(gandi, datacenter_id):
    """List available sys_disk_id of images."""

    result = gandi.image.list(datacenter_id)
    for source in result:
        msg = '%s (%s) - kernel:%s - dc:%d - # %d' % (source['label'],
                                                      source['os_arch'],
                                                      source['kernel_version'],
                                                      source['datacenter_id'],
                                                      source['disk_id'])
        gandi.echo(msg)

    return result
