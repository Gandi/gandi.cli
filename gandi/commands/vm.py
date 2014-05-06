
import time
from subprocess import call

import click
from click.exceptions import UsageError

from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@pass_gandi
def list(gandi, state, id):
    """list virtual machines"""

    options = {}
    if state:
        options['state'] = state

    result = gandi.call('vm.list', options)
    for vm in result:
        print '%s - %s' % (vm['hostname'], vm['state']),
        if id:
            print '- #%d' % vm['id'],
        print

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """display information about a virtual machine"""

    result = gandi.call('vm.info', id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def stop(gandi, id):
    """stop a virtual machine"""

    result = gandi.call('vm.stop', id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def start(gandi, id):
    """start a virtual machine"""

    result = gandi.call('vm.start', id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def reboot(gandi, id):
    """reboot a virtual machine"""

    result = gandi.call('vm.reboot', id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def delete(gandi, id):
    """delete a virtual machine"""

    result = gandi.call('vm.delete', id)
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
@click.option('--run', default=None,
              help='shell command that will run at the first startup of a VM.\
This command will run with root privileges in the ``/`` directory at the end \
of its boot: network interfaces and disks are mounted')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.argument('ssh_key', default=None, type=click.File('rb'), required=False,
                callback=read_ssh_key,
                help='ssh public key to authorize to connect to the root \
account and the created login')
@pass_gandi
def create(gandi, datacenter_id, memory, cores, ip_version, bandwidth, login,
           password, run, interactive, ssh_key):
    """create a new virtual machine.

    you can provide a ssh_key on command line calling this command as:

    >>> cat ~/.ssh/id_rsa.pub | gandi vm -

    """

    # priority to command line parameters
    # then env var
    # then local configuration
    # then global configuration
    datacenter_id_ = datacenter_id if datacenter_id else int(gandi.get('datacenter_id'))
    memory_ = memory if memory else int(gandi.get('memory'))
    cores_ = cores if cores else int(gandi.get('cores'))
    ip_version_ = ip_version if ip_version else int(gandi.get('ip_version'))
    bandwidth_ = bandwidth if bandwidth else int(gandi.get('bandwidth'))

    login_ = login if login else gandi.get('login')
    password_ = password if password else gandi.get('password')

    vm_params = {
        'hostname': 'tempo',
        'datacenter_id': datacenter_id_,
        'memory': memory_,
        'cores': cores_,
        'ip_version': ip_version_,
        'bandwidth': bandwidth_,
        'login': login_,
        'password': password_,
    }
    run_ = run if run else gandi.get('run')
    if run_ is not None:
        vm_params['run'] = run_

    ssh_key_ = ssh_key if ssh_key else gandi.get('ssh_key')
    if ssh_key_ is not None:
        vm_params['ssh_key'] = ssh_key_

    disk_params = {'datacenter_id': int(gandi.get('datacenter_id')),
                   'name': 'sysdisktempo'}
    sys_disk_id = int(gandi.get('sys_disk_id'))

    result = gandi.call('vm.create_from', vm_params, disk_params, sys_disk_id)
    if not interactive:
        from pprint import pprint
        pprint(result)
    else:
        # interactive mode, run a progress bar
        from datetime import datetime
        start_crea = datetime.utcnow()

        print "We're creating your first Virtual Machine with default settings."
        # count number of operations, 3 steps per operation
        count_operations = len(result) * 3
        crea_done = False
        vm_id = None
        while not crea_done:
            op_score = 0
            for oper in result:
                op_step = gandi.call('operation.info', oper['id'])['step']
                if op_step == 'WAIT':
                    op_score += 1
                elif op_step == 'RUN':
                    op_score += 2
                elif op_step == 'DONE':
                    op_score += 3
                else:
                    msg = 'step %s unknown, exiting creation' % op_step
                    raise UsageError(msg)

                if 'vm_id' in oper and oper['vm_id'] is not None:
                    vm_id = oper['vm_id']

            gandi.update_progress(float(op_score) / count_operations, start_crea)

            if op_score == count_operations:
                crea_done = True

            time.sleep(.5)

        print
        vm_info = gandi.call('vm.info', vm_id)
        for iface in vm_info['ifaces']:
            for ip in iface['ips']:
                if ip['version'] == 4:
                    access = 'ssh %s@%s' % (login_, ip['ip'])
                else:
                    access = 'ssh -6 %s@%s' % (login_, ip['ip'])
                # stop on first access found
                break

        print 'Your VM have been created, requesting access...'
        time.sleep(5)
        gandi.shell(access)
