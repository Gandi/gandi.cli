import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_vm, output_image, output_generic,
)
from gandi.cli.core.params import (
    pass_gandi, option, IntChoice, DATACENTER, DISK_IMAGE,
)


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, state, id, limit):
    """List virtual machines."""

    options = {
        'items_per_page': limit,
    }
    if state:
        options['state'] = state

    output_keys = ['hostname', 'state']
    if id:
        output_keys.append('id')

    datacenters = gandi.datacenter.list()
    result = gandi.iaas.list(options)
    for vm in result:
        gandi.separator_line()
        output_vm(gandi, vm, datacenters, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def info(gandi, resource):
    """Display information about a virtual machine.

    Resource can be a Hostname or an ID
    """

    output_keys = ['hostname', 'state', 'cores', 'memory', 'console',
                   'datacenter', 'ip']

    datacenters = gandi.datacenter.list()
    ret = []
    for item in resource:
        vm = gandi.iaas.info(item)
        output_vm(gandi, vm, datacenters, output_keys, 14)
        ret.append(vm)
        for disk in vm['disks']:
            disk_out_keys = ['label', 'kernel_version', 'name', 'size']
            output_image(gandi, disk, datacenters, disk_out_keys, 14)

    return ret


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run in background mode (default=False)')
@pass_gandi
def stop(gandi, background, resource):
    """Stop a virtual machine.

    Resource can be a Hostname or an ID
    """

    output_keys = ['id', 'type', 'step']

    opers = gandi.iaas.stop(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run in background mode (default=False)')
@pass_gandi
def start(gandi, background, resource):
    """Start a virtual machine.

    Resource can be a Hostname or an ID
    """

    output_keys = ['id', 'type', 'step']

    opers = gandi.iaas.start(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run in background mode (default=False)')
@pass_gandi
def reboot(gandi, background, resource):
    """Reboot a virtual machine.

    Resource can be a Hostname or an ID
    """

    output_keys = ['id', 'type', 'step']

    opers = gandi.iaas.reboot(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run in background mode (default=False)')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, background, force, resource):
    """Delete a virtual machine.

    Resource can be a Hostname or an ID
    """

    output_keys = ['id', 'type', 'step']

    iaas_list = gandi.iaas.list()
    iaas_namelist = [vm['hostname'] for vm in iaas_list]
    for item in resource:
        if item not in iaas_namelist:
            gandi.echo('Sorry virtual machine %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' % iaas_namelist)
            return

    if not force:
        instance_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm("Are you sure to delete Virtual Machine %s?" %
                                instance_info)

        if not proceed:
            return

    stop_opers = []
    for item in resource:
        vm = next((vm for (index, vm) in enumerate(iaas_list)
                  if vm['hostname'] == item), None)
        if vm['state'] == 'running':
            if background:
                gandi.echo('Virtual machine not stopped, background option '
                           'disabled')
                background = False
            oper = gandi.iaas.stop(item, background)
            if not background:
                stop_opers.append(oper)

    opers = gandi.iaas.delete(resource, background)
    if background:
        for oper in stop_opers + opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@option('--datacenter', type=DATACENTER, default='FR',
        help='datacenter where the VM will be spawned')
@option('--memory', type=click.INT, default=256,
        help='quantity of RAM in Megabytes to allocate')
@option('--cores', type=click.INT, default=1,
        help='number of cpu')
@option('--ip-version', type=IntChoice(['4', '6']), default='4',
        help='version of the created IP')
@option('--bandwidth', type=click.INT, default=102400,
        help="network bandwidth in bit/s used to create the VM's first "
             "network interface")
@option('--login', default='admin',
        help='login to create on the VM')
@click.option('--password', default=False, is_flag=True,
              help='will ask for a password to be set for the root account '
                   'and the created login')
@click.option('--hostname', default=None,
              help='hostname of the VM, will be generated if not provided')
@option('--image', type=DISK_IMAGE, default='Debian 7',
        help='disk image used to boot the vm')
@click.option('--run', default=None,
              help='shell command that will run at the first startup of a VM.'
                   'This command will run with root privileges in the ``/`` '
                   'directory at the end of its boot: network interfaces and '
                   'disks are mounted')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run creation in background mode (default=False)')
@option('--ssh-key',
        help='Authorize ssh authentication for the given ssh key')
@option('--ssh-key-id', help='Add an ssh key id OR name from the portfolio.',
        multiple=True)
@pass_gandi
def create(gandi, datacenter, memory, cores, ip_version, bandwidth, login,
           password, hostname, image, run, background, ssh_key, ssh_key_id):
    """Create a new virtual machine.

    you can specify a configuration entry named 'ssh_key' containing
    path to your ssh_key file

    >>> gandi config -g ssh_key ~/.ssh/id_rsa.pub

    to know which disk image label (or id) to use as image

    >>> gandi images

    """
    pwd = None
    if password or not (ssh_key or ssh_key_id):
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

    if not password:
        gandi.echo('/!\ Please be aware that you did not provide a password, '
                   'some services like console will not be able to work.')

    result = gandi.iaas.create(datacenter, memory, cores, ip_version,
                               bandwidth, login, pwd, hostname,
                               image, run,
                               background,
                               ssh_key, ssh_key_id)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--memory', type=click.INT, default=None,
              help='quantity of RAM in Megabytes to allocate')
@click.option('--cores', type=click.INT, default=None,
              help='number of cpu')
@click.option('--console', default=None, is_flag=True,
              help='activate the emergency console')
@click.option('--password', default=False, is_flag=True,
              help='will ask for a password to be set for the root account '
                   'and the created login')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run creation in background mode (default=False)')
@click.argument('resource')
@pass_gandi
def update(gandi, resource, memory, cores, console, password, background):
    """Update a virtual machine.

    Resource can be a Hostname or an ID
    """
    pwd = None
    if password:
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

    result = gandi.iaas.update(resource, memory, cores, console, pwd,
                               background)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('resource')
@pass_gandi
def console(gandi, resource):
    """Open a console to virtual machine.

    Resource can be a Hostname or an ID
    """
    gandi.echo('/!\ Please be aware that if you didn\'t provide a password '
               'during creation, console service will be unavailable.')
    gandi.echo('/!\ You can use "gandi vm update" command to set a password.')

    gandi.iaas.console(resource)


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='filter by datacenter')
@click.argument('label', required=False)
@pass_gandi
def images(gandi, label, datacenter):
    """List available system images for virtual machines.

    You can also filter results using label, by example:

    >>> gandi vm images Ubuntu --datacenter FR

    or

    >>> gandi vm images 'Ubuntu 10.04' --datacenter FR

    """

    output_keys = ['label', 'os_arch', 'kernel_version', 'disk_id',
                   'dc']

    datacenters = gandi.datacenter.list()
    result = gandi.image.list(datacenter, label)
    for image in result:
        gandi.separator_line()
        output_image(gandi, image, datacenters, output_keys)

    return result


@cli.command(root=True)
@click.option('--id', help='display ids', is_flag=True)
@pass_gandi
def datacenters(gandi, id):
    """List available datacenters."""

    output_keys = ['iso', 'name', 'country']
    if id:
        output_keys.append('id')

    result = gandi.datacenter.list()
    for dc in result:
        gandi.separator_line()
        output_generic(gandi, dc, output_keys)

    return result
