
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import output_paas, output_oper


@cli.command(name='paas.list')
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@click.option('--vhosts', help='display vhosts', default=True, is_flag=True)
@pass_gandi
def list(gandi, state, id, vhosts):
    """List Paas instances."""

    options = {}
    if state:
        options['state'] = state

    output_keys = ['name', 'state']
    if id:
        output_keys.append('id')
    if vhosts:
        output_keys.append('vhost')

    paas_hosts = {}
    result = gandi.paas.list(options)
    for paas in result:
        paas_hosts[paas['id']] = []
        if vhosts:
            list_vhost = gandi.vhost.list({'paas_id': paas['id']})
            for host in list_vhost:
                paas_hosts[paas['id']].append(host['name'])

        gandi.echo('-' * 10)
        output_paas(gandi, paas, [], paas_hosts[paas['id']],
                    output_keys)

    return result


@cli.command(name='paas.info')
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """Display information about a Paas instance."""

    output_keys = ['name', 'type', 'size', 'memory', 'console', 'vhost',
                   'dc', 'ftp_server', 'git_server']

    paas = gandi.paas.info(id)
    paas_hosts = []
    list_vhost = gandi.vhost.list({'paas_id': paas['id']})
    for host in list_vhost:
        paas_hosts.append(host['name'])

    output_paas(gandi, paas, [], paas_hosts, output_keys)

    return paas


@cli.command()
@click.argument('vhost')
@pass_gandi
def clone(gandi, vhost):
    """Clone a remote vhost in a local git repository."""

    paas = gandi.paas.info(vhost)

    git_server = paas['git_server']
    # dev hack
    git_server = '10.55.32.107'

    gandi.shell('git clone ssh+git://%s@%s/%s.git' % (paas['user'], git_server,
                                                      vhost))


@cli.command()
@click.argument('vhost')
@click.argument('git_url', required=False)
@pass_gandi
def deploy(gandi, vhost, git_url):
    """Deploy code on a remote vhost."""

    paas = gandi.paas.info(vhost)

    git_server = paas['git_server']
    # dev hack
    git_server = '10.55.32.107'

    if git_url:
        # clone locally
        gandi.shell('git clone %s .' % git_url)
        gandi.shell('git remote add gandi ssh+git://%s@%s/%s.git' %
                    (paas['user'], git_server, vhost))
        gandi.shell('git push gandi')
    else:
        gandi.shell('git push origin')

    gandi.shell("ssh %s@%s 'deploy %s.git'" % (paas['user'], git_server,
                                               vhost))


@cli.command(name='paas.delete')
@click.argument('id')
@pass_gandi
def delete(gandi, id):
    """Delete a PaaS instance."""

    output_keys = ['id', 'type', 'step']

    oper = gandi.paas.delete(id)
    output_oper(gandi, oper, output_keys)

    return oper


@cli.command(name='paas')
@click.option('--name', default=None,
              help='Name of the PaaS instance')
@click.option('--size', default=None,
              help='Size of the PaaS instance')
@click.option('--type', default=None,
              help='Type of the PaaS instance')
@click.option('--quantity', default=0,
              help='Additional disk amount (in GB)')
@click.option('--duration', default=None,
              help='number of month, suffixed with m (e.g.: `12m` means one year)')
@click.option('--datacenter', default=None,
              help='name|iso|country|id of the datacenter where the PaaS will be spawned')
@click.option('--vhosts', default=None,
              help='List of virtual hosts to be linked to the instance')
@click.option('--password', default=None,
              help='Password of the PaaS instance')
@click.option('--snapshot-profile', default=None,
              help='Set a snapshot profile associated to this paas disk')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@click.option('--ssh-key', default=None,
              help='Authorize ssh authentication for the given ssh key')
@pass_gandi
def create(gandi, name, size, type, quantity, duration, datacenter, vhosts,
           password, snapshot_profile, interactive, ssh_key):
    """Create a new PaaS instance.

    you can specify a configuration entry named 'ssh_key' containing
    path to your ssh_key file

    >>> gandi config ssh_key ~/.ssh/id_rsa.pub

    to know which datacenter name|iso|country|id to use as datacenter

    >>> gandi datacenters

    """

    result = gandi.paas.create(name, size, type, quantity, duration,
                               datacenter, vhosts, password,
                               snapshot_profile, interactive, ssh_key)
    if not interactive:
        gandi.pretty_echo(result)

    return result


@cli.command(name='paas.update')
@click.option('--name', type=click.STRING, default=None,
              help='Name of the PaaS instance')
@click.option('--size', default=None,
              help='Size of the PaaS instance')
@click.option('--quantity', type=click.INT, default=0,
              help='Additional disk amount (in GB)')
@click.option('--password', default=None,
              help='Password of the PaaS instance')
@click.option('--ssh-key', default=None,
              help='Authorize ssh authentication for the given ssh key')
@click.option('--upgrade', default=None,
              help='Upgrade the instance to the last system image if needed')
@click.option('--console', default=None,
              help='Activate or deactivate the Console')
@click.option('--snapshot-profile', default=None,
              help='Set a snapshot profile associated to this paas disk')
@click.option('--reset-mysql-password', default=None,
              help='Reset mysql password for root')
@click.option('--interactive', default=True, is_flag=True,
              help='run creation in interactive mode (default=True)')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, name, size, quantity, password, ssh_key,
           upgrade, console, snapshot_profile, reset_mysql_password,
           interactive):
    """Update a PaaS instance.

    Resource can be a Hostname or an ID
    """

    result = gandi.paas.update(resource, name, size, quantity, password,
                               ssh_key, upgrade, console, snapshot_profile,
                               reset_mysql_password, interactive)
    if not interactive:
        gandi.pretty_echo(result)

    return result
