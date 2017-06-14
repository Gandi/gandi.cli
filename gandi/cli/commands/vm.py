""" Virtual machines namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_vm, output_image, output_generic, output_datacenter,
    output_kernels, output_metric,
    DatacenterLimited
)
from gandi.cli.core.utils.size import disk_check_size
from gandi.cli.core.params import (
    pass_gandi, option, IntChoice, DATACENTER, DISK_IMAGE, SIZE
)


@cli.command()
@click.option('--state', default=None, help='Filter results by state.')
@click.option('--datacenter', default=None, type=DATACENTER,
              help='Filter results by datacenter.')
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, state, id, limit, datacenter):
    """List virtual machines."""
    options = {
        'items_per_page': limit,
    }
    if state:
        options['state'] = state
    if datacenter:
        options['datacenter_id'] = gandi.datacenter.usable_id(datacenter)

    output_keys = ['hostname', 'state']
    if id:
        output_keys.append('id')

    result = gandi.iaas.list(options)
    for num, vm in enumerate(result):
        if num:
            gandi.separator_line()
        output_vm(gandi, vm, [], output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--stat', default=False, is_flag=True,
              help='Display general vm statistic')
@pass_gandi
def info(gandi, resource, stat):
    """Display information about a virtual machine.

    Resource can be a Hostname or an ID
    """
    output_keys = ['hostname', 'state', 'cores', 'memory', 'console',
                   'datacenter', 'ip']
    justify = 14
    if stat is True:
        sampler = {'unit': 'hours', 'value': 1, 'function': 'max'}
        time_range = 3600 * 24
        query_vif = 'vif.bytes.all'
        query_vbd = 'vbd.bytes.all'

    resource = sorted(tuple(set(resource)))
    datacenters = gandi.datacenter.list()
    ret = []
    for num, item in enumerate(resource):
        if num:
            gandi.separator_line()
        vm = gandi.iaas.info(item)
        output_vm(gandi, vm, datacenters, output_keys, justify)
        ret.append(vm)
        for num, disk in enumerate(vm['disks']):
            gandi.echo('')
            disk_out_keys = ['label', 'kernel_version', 'name', 'size']
            output_image(gandi, disk, datacenters, disk_out_keys, justify)
        if stat is True:
            metrics_vif = gandi.metric.query(vm['id'], time_range, query_vif,
                                             'vm', sampler)
            metrics_vbd = gandi.metric.query(vm['id'], time_range, query_vbd,
                                             'vm', sampler)
            gandi.echo('')
            gandi.echo('vm network stats')
            output_metric(gandi, metrics_vif, 'direction', justify)
            gandi.echo('disk network stats')
            output_metric(gandi, metrics_vbd, 'direction', justify)

    return ret


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def stop(gandi, background, resource):
    """Stop a virtual machine.

    Resource can be a Hostname or an ID
    """
    output_keys = ['id', 'type', 'step']

    resource = sorted(tuple(set(resource)))
    opers = gandi.iaas.stop(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def start(gandi, background, resource):
    """Start a virtual machine.

    Resource can be a Hostname or an ID
    """
    output_keys = ['id', 'type', 'step']

    resource = sorted(tuple(set(resource)))
    opers = gandi.iaas.start(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def reboot(gandi, background, resource):
    """Reboot a virtual machine.

    Resource can be a Hostname or an ID
    """
    output_keys = ['id', 'type', 'step']

    resource = sorted(tuple(set(resource)))
    opers = gandi.iaas.reboot(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, background, force, resource):
    """Delete a virtual machine.

    Resource can be a Hostname or an ID
    """
    output_keys = ['id', 'type', 'step']

    resource = sorted(tuple(set(resource)))
    possible_resources = gandi.iaas.resource_list()
    for item in resource:
        if item not in possible_resources:
            gandi.echo('Sorry virtual machine %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' %
                       possible_resources)
            return

    if not force:
        instance_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm("Are you sure to delete Virtual Machine %s?" %
                                instance_info)

        if not proceed:
            return

    iaas_list = gandi.iaas.list()
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
@option('--datacenter', type=DATACENTER, default='FR-SD3',
        help='Datacenter where the VM will be spawned.')
@option('--memory', type=click.INT, default=256,
        help='Quantity of RAM in Megabytes to allocate.')
@option('--cores', type=click.INT, default=1,
        help='Number of cpu.')
@click.option('--ip-version', type=IntChoice(['4', '6']), default=None,
              help='Version of created IP.')
@option('--bandwidth', type=click.INT, default=102400,
        help="Network bandwidth in kbit/s used to create the VM's first "
             "network interface.")
@click.option('--login', default=None,
              help='Login to create on the VM.')
@click.option('--password', default=False, is_flag=True,
              help='Will ask for a password to be set for the root account '
                   'and the created login.')
@click.option('--hostname', default=None,
              help='Hostname of the VM, will be generated if not provided.')
@option('--image', type=DISK_IMAGE, default='Debian 8',
        help='Disk image used to boot the VM.')
@click.option('--run', default=None,
              help='Shell command that will run at the first startup of a VM.'
                   'This command will run with root privileges in the ``/`` '
                   'directory at the end of its boot: network interfaces and '
                   'disks are mounted.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@option('--sshkey', multiple=True,
        help='Authorize ssh authentication for the given ssh key.')
@click.option('--size', default=None, metavar='SIZE[M|G|T]', type=SIZE,
              help=('Disk size. A size suffix (M for megabytes up to T for '
                    'terabytes) is optional, megabytes is the default if no '
                    'suffix is present.'),
              callback=disk_check_size)
@click.option('--vlan', default=None, help='A vlan to use with this vm.')
@click.option('--ip', default=None, help='An ip in the vlan for this vm.')
@click.option('--script', default=None,
              help='Local script to upload and run on the VM after creation.')
@click.option('--script-args', default=None,
              help='Local script argument line.')
@click.option('--ssh', default=False, is_flag=True,
              help='Open a SSH session to the machine after creation '
                   '(default=False).')
@pass_gandi
def create(gandi, datacenter, memory, cores, ip_version, bandwidth, login,
           password, hostname, image, run, background, sshkey, size, vlan, ip,
           script, script_args, ssh):
    """Create a new virtual machine.

    you can specify a configuration entry named 'sshkey' containing
    path to your sshkey file

    $ gandi config set [-g] sshkey ~/.ssh/id_rsa.pub

    or getting the sshkey "my_key" from your gandi ssh keyring

    $ gandi config set [-g] sshkey my_key

    to know which disk image label (or id) to use as image

    $ gandi vm images

    """
    try:
        gandi.datacenter.is_opened(datacenter, 'iaas')
    except DatacenterLimited as exc:
        gandi.echo('/!\ Datacenter %s will be closed on %s, '
                   'please consider using another datacenter.' %
                   (datacenter, exc.date))

    pwd = None
    if password or not sshkey:
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

    if ip and not vlan:
        gandi.echo("--ip can't be used without --vlan.")
        return

    if not vlan and not ip_version:
        ip_version = 6

    if not ip_version:
        gandi.echo("* Private only ip vm (can't enable emergency web console "
                   'access).')

    # Display a short summary for creation
    if login:
        user_summary = 'root and %s users' % login
    else:
        user_summary = 'root user'

    gandi.echo('* %s will be created.' % user_summary)
    if sshkey:
        gandi.echo('* SSH key authorization will be used.')
    if not pwd:
        gandi.echo('* No password supplied for vm (required to enable '
                   'emergency web console access).')
    result = gandi.iaas.create(datacenter, memory, cores, ip_version,
                               bandwidth, login, pwd, hostname,
                               image, run,
                               background,
                               sshkey, size, vlan, ip, script, script_args, ssh)
    if background:
        gandi.echo('* IAAS backend is now creating your VM and its '
                   'associated resources in the background.')

    return result


@cli.command()
@click.option('--memory', type=click.INT, default=None,
              help='Quantity of RAM in Megabytes to allocate.')
@click.option('--cores', type=click.INT, default=None,
              help='Number of cpu.')
@click.option('--console', default=None, is_flag=True,
              help='Activate the emergency console.')
@click.option('--password', default=False, is_flag=True,
              help='Will ask for a password to be set for the root account '
                   'and the created login.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--reboot', default=False, is_flag=True,
              help='Accept a VM reboot for non-live updates')
@click.argument('resource')
@pass_gandi
def update(gandi, resource, memory, cores, console, password, background,
           reboot):
    """Update a virtual machine.

    Resource can be a Hostname or an ID
    """
    pwd = None
    if password:
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

    max_memory = None
    if memory:
        max_memory = gandi.iaas.required_max_memory(resource, memory)

    if max_memory and not reboot:
        gandi.echo('memory update must be done offline.')
        if not click.confirm("reboot machine %s?" % resource):
            return

    result = gandi.iaas.update(resource, memory, cores, console, pwd,
                               background, max_memory)
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
    gandi.echo('/!\ Use ~. ssh escape key to exit.')

    gandi.iaas.console(resource)


@cli.command()
@click.option('--wait', default=False, is_flag=True,
              help='Wait for virtual machine sshd to come up (timeout 2min).')
@click.option('--wipe-key', default=False, is_flag=True,
              help='Wipe SSH known host entry first.')
@click.option('--login', '-l', default='root',
              help='Use given login for ssh call')
@click.option('--identity', '-i', default=None,
              help='Use specified path for ssh key')
@click.argument('resource')
@click.argument('args', nargs=-1)
@pass_gandi
def ssh(gandi, resource, login, identity, wipe_key, wait, args):
    """Spawn an SSH session to virtual machine.

    Resource can be a Hostname or an ID
    """
    if '@' in resource:
        (login, resource) = resource.split('@', 1)
    if wipe_key:
        gandi.iaas.ssh_keyscan(resource)
    if wait:
        gandi.iaas.wait_for_sshd(resource)
    gandi.iaas.ssh(resource, login, identity, args)


@cli.command()
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.argument('label', required=False)
@pass_gandi
def images(gandi, label, datacenter):
    """List available system images for virtual machines.

    You can also filter results using label, by example:

    $ gandi vm images Ubuntu --datacenter LU

    or

    $ gandi vm images 'Ubuntu 10.04' --datacenter LU

    """
    output_keys = ['label', 'os_arch', 'kernel_version', 'disk_id',
                   'dc', 'name']

    datacenters = gandi.datacenter.list()
    result = gandi.image.list(datacenter, label)
    for num, image in enumerate(result):
        if num:
            gandi.separator_line()
        output_image(gandi, image, datacenters, output_keys)

    # also display usable disks
    result = gandi.disk.list_create(datacenter, label)
    for disk in result:
        gandi.separator_line()
        output_image(gandi, disk, datacenters, output_keys)

    return result


@cli.command()
@click.option('--vm', default=None,
              help='Output available kernels for given vm.')
@click.option('--datacenter', type=DATACENTER, default=None,
              help='Filter by datacenter.')
@click.option('--flavor', default=None,
              help='Filter by kernel flavor.')
@click.argument('match', default='', required=False, metavar='pattern')
@pass_gandi
def kernels(gandi, vm, datacenter, flavor, match):
    """List available kernels."""

    if vm:
        vm = gandi.iaas.info(vm)

    dc_list = gandi.datacenter.filtered_list(datacenter, vm)

    for num, dc in enumerate(dc_list):
        if num:
            gandi.echo('\n')
        output_datacenter(gandi, dc, ['dc_name'])
        kmap = gandi.kernel.list(dc['id'], flavor, match)
        for _flavor in kmap:
            gandi.separator_line()
            output_kernels(gandi, _flavor, kmap[_flavor])


@cli.command(root=True)
@click.option('--id', help='Display ids.', is_flag=True)
@pass_gandi
def datacenters(gandi, id):
    """List available datacenters."""
    output_keys = ['iso', 'name', 'country', 'dc_code', 'status']
    if id:
        output_keys.append('id')

    result = gandi.datacenter.list()
    for num, dc in enumerate(result):
        if num:
            gandi.separator_line()
        output_datacenter(gandi, dc, output_keys, justify=10)

    return result
