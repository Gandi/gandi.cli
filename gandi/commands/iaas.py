
import click

from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@pass_gandi
def list(gandi, state):
    """list virtual machines"""

    options = {}
    if state:
        options['state'] = state

    result = gandi.iaas.list(options)
    for vm in result:
        print '%s - %s - #%d' % (vm['hostname'], vm['state'], vm['id'])

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """display information about a virtual machine"""

    result = gandi.iaas.info(id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def stop(gandi, id):
    """stop a virtual machine"""

    result = gandi.iaas.stop(id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def start(gandi, id):
    """start a virtual machine"""

    result = gandi.iaas.start(id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def reboot(gandi, id):
    """reboot a virtual machine"""

    result = gandi.iaas.reboot(id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id')
@pass_gandi
def delete(gandi, id):
    """delete a virtual machine"""

    result = gandi.iaas.delete(id)
    from pprint import pprint
    pprint(result)

    return result


def read_ssh_key(ctx, value):
    if not value:
        return

    key = value.read()
    return key


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
              help="network bandwidth in bit/s used to create the VM's first \
network interface")
@click.option('--login', default=None,
              help='login to create on the VM')
@click.option('--password', default=None,
              help='password to set to the root account and the created login')
@click.option('--hostname', default='tempo',
              help='hostname of the VM')
@click.option('--run', default=None,
              help='shell command that will run at the first startup of a VM.\
This command will run with root privileges in the ``/`` directory at the end \
of its boot: network interfaces and disks are mounted')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.argument('ssh_key', default=None, type=click.File('rb'), required=False,
                callback=read_ssh_key)
@pass_gandi
def create(gandi, datacenter_id, memory, cores, ip_version, bandwidth, login,
           password, hostname, run, interactive, ssh_key):
    """create a new virtual machine.

    you can provide a ssh_key on command line calling this command as:

    >>> cat ~/.ssh/id_rsa.pub | gandi vm -

    """

    result = gandi.iaas.create(datacenter_id, memory, cores, ip_version,
                               bandwidth, login, password, hostname, run,
                               interactive, ssh_key)
    from pprint import pprint
    pprint(result)

    return result
