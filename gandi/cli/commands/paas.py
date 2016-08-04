""" PaaS instances namespace commands. """

import os

import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_paas, output_generic, randomstring,
    DatacenterLimited
)
from gandi.cli.core.params import (
    pass_gandi, DATACENTER, SNAPSHOTPROFILE_PAAS, PAAS_TYPE, option,
)


@cli.command()
@click.option('--state', default=None, help='Filter results by state.')
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--vhosts', help='Display vhosts.', default=True, is_flag=True)
@click.option('--type', help='Display types.', is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, state, id, vhosts, type, limit):
    """List PaaS instances."""
    options = {
        'items_per_page': limit,
    }
    if state:
        options['state'] = state

    output_keys = ['name', 'state']
    if id:
        output_keys.append('id')
    if vhosts:
        output_keys.append('vhost')
    if type:
        output_keys.append('type')

    paas_hosts = {}
    result = gandi.paas.list(options)
    for num, paas in enumerate(result):
        paas_hosts[paas['id']] = []
        if vhosts:
            list_vhost = gandi.vhost.list({'paas_id': paas['id']})
            for host in list_vhost:
                paas_hosts[paas['id']].append(host['name'])

        if num:
            gandi.separator_line()
        output_paas(gandi, paas, [], paas_hosts[paas['id']],
                    output_keys)

    return result


@cli.command()
@click.argument('resource')
@click.option('--stat', default=False, is_flag=True,
              help='Display cached page statistic based on the last 24 hours.')
@pass_gandi
def info(gandi, resource, stat):
    """Display information about a PaaS instance.

    Resource can be a vhost, a hostname, or an ID
    Cache statistics are based on 24 hours data.
    """
    output_keys = ['name', 'type', 'size', 'memory', 'console', 'vhost',
                   'dc', 'sftp_server', 'git_server', 'snapshot']

    paas = gandi.paas.info(resource)
    paas_hosts = []
    list_vhost = gandi.vhost.list({'paas_id': paas['id']})

    df = gandi.paas.quota(paas['id'])
    paas.update({'df': df})

    if stat:
        cache = gandi.paas.cache(paas['id'])
        paas.update({'cache': cache})

    for host in list_vhost:
        paas_hosts.append(host['name'])

    output_paas(gandi, paas, [], paas_hosts, output_keys)

    return paas


@cli.command()
@click.option('--origin', default='gandi', help="Set the origin remote's name")
@click.option('--directory', help='Specify the destination directory')
@click.option('--vhost', required=False, default='default')
@click.argument('name', required=True)
@pass_gandi
def clone(gandi, name, vhost, directory, origin):
    """Clone a remote vhost in a local git repository."""
    if vhost != 'default':
        directory = vhost
    else:
        directory = name if not directory else directory

    return gandi.paas.clone(name, vhost, directory, origin)


@cli.command()
@click.option('--vhost', default='default',
              help="Add a remote for a given instance's vhost to the local "
              "git repository")
@click.option('--remote', default='gandi', help="Specify the remote's name")
@click.argument('name', required=True)
@pass_gandi
def attach(gandi, name, vhost, remote):
    """Add remote for an instance's default vhost to the local git repository.
    """
    return gandi.paas.attach(name, vhost, remote)


@cli.command(root=True)
@click.option('--remote', default='gandi', help="Specify the remote's name")
@click.option('--branch', default='master', help="Specify the branch to deploy")
@pass_gandi
def deploy(gandi, remote, branch):
    """Deploy code on the instance's remote vhost corresponding to current
    directory.
    """
    return gandi.paas.deploy(remote, branch)


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, background, force, resource):
    """Delete a PaaS instance.

    Resource can be a vhost, a hostname, or an ID
    """
    output_keys = ['id', 'type', 'step']

    possible_resources = gandi.paas.resource_list()
    for item in resource:
        if item not in possible_resources:
            gandi.echo('Sorry PaaS instance %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' %
                       possible_resources)
            return

    if not force:
        instance_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm("Are you sure to delete PaaS instance %s?" %
                                instance_info)

        if not proceed:
            return

    opers = gandi.paas.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@click.option('--name', default=None,
              help='Name of the PaaS instance, will be generated if not '
                   'provided.')
@option('--size', default='s',
        type=click.Choice(['s', 'm', 'l', 'xl', 'xxl']),
        help='Size of the PaaS instance.')
@option('--type', default='pythonpgsql',
        type=PAAS_TYPE,
        help='Type of the PaaS instance.')
@option('--quantity', default=0,
        help='Additional disk amount (in GB).')
@option('--duration', default='1m',
        help='Number of month, suffixed with m.')
@option('--datacenter', type=DATACENTER, default='LU-BI1',
        help='Datacenter where the PaaS will be spawned.')
@click.option('--vhosts', default=None,
              help='Virtual host(s) to be linked to the instance.')
@click.option('--ssl', help='Get ssl on that vhost.', is_flag=True)
@click.option('--pk', '--private-key',
              help='Private key used to generate the ssl Certificate.')
@click.option('--poll-cert', help='Will wait for the certificate creation.',
              is_flag=True)
@click.option('--password', help='Use command-line supplied password.')
@click.option('--snapshotprofile', default=None, type=SNAPSHOTPROFILE_PAAS,
              help='Set a snapshot profile associated to this paas disk.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@option('--sshkey', multiple=True,
        help='Authorize ssh authentication for the given ssh key.')
@pass_gandi
def create(gandi, name, size, type, quantity, duration, datacenter, vhosts,
           password, snapshotprofile, background, sshkey, ssl, private_key,
           poll_cert):
    """Create a new PaaS instance and initialize associated git repository.

    you can specify a configuration entry named 'sshkey' containing
    path to your sshkey file

    $ gandi config set [-g] sshkey ~/.ssh/id_rsa.pub

    or getting the sshkey "my_key" from your gandi ssh keyring

    $ gandi config set [-g] sshkey my_key

    to know which PaaS instance type to use as type

    $ gandi paas types

    """
    try:
        gandi.datacenter.is_opened(datacenter, 'paas')
    except DatacenterLimited as exc:
        gandi.echo('/!\ Datacenter %s will be closed on %s, '
                   'please consider using another datacenter.' %
                   (datacenter, exc.date))

    if not password:
        password = click.prompt('password', hide_input=True,
                                confirmation_prompt=True)

    if not name:
        name = randomstring('paas')

    if vhosts and not gandi.hostedcert.activate_ssl(vhosts,
                                                    ssl,
                                                    private_key,
                                                    poll_cert):
        return

    result = gandi.paas.create(name, size, type, quantity, duration,
                               datacenter, vhosts, password,
                               snapshotprofile, background, sshkey)
    return result


@cli.command()
@click.option('--name', type=click.STRING, default=None,
              help='Name of the PaaS instance.')
@click.option('--size', default=None,
              type=click.Choice(['s', 'm', 'x', 'xl', 'xxl']),
              help='Size of the PaaS instance.')
@click.option('--quantity', type=click.INT, default=0,
              help='Additional disk amount (in GB).')
@click.option('--password', default=False, is_flag=True,
              help='Password of the PaaS instance.')
@click.option('--sshkey', multiple=True,
              help='Authorize ssh authentication for the given ssh key.')
@click.option('--upgrade', default=False, is_flag=True,
              help='Upgrade the instance to the last system image if needed.')
@click.option('--console', default=None,
              help='Activate or deactivate the Console.')
@click.option('--snapshotprofile', default=None, type=click.INT,
              help='Set a snapshot profile associated to this paas disk.')
@click.option('--reset-mysql-password', default=None,
              help='Reset mysql password for root.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--delete-snapshotprofile', default=False, is_flag=True,
              help='Remove a snapshot profile associated to this paas disk.')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, name, size, quantity, password, sshkey,
           upgrade, console, snapshotprofile, reset_mysql_password,
           background, delete_snapshotprofile):
    """Update a PaaS instance.

    Resource can be a Hostname or an ID
    """

    if snapshotprofile and delete_snapshotprofile:
        raise UsageError('You must not set snapshotprofile and '
                         'delete-snapshotprofile.')

    pwd = None
    if password:
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

    if delete_snapshotprofile:
        snapshotprofile = ''

    result = gandi.paas.update(resource, name, size, quantity, pwd,
                               sshkey, upgrade, console, snapshotprofile,
                               reset_mysql_password, background)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@pass_gandi
def restart(gandi, resource, background, force):
    """Restart a PaaS instance.

    Resource can be a vhost, a hostname, or an ID
    """
    output_keys = ['id', 'type', 'step']

    possible_resources = gandi.paas.resource_list()
    for item in resource:
        if item not in possible_resources:
            gandi.echo('Sorry PaaS instance %s does not exist' % item)
            gandi.echo('Please use one of the following: %s' %
                       possible_resources)
            return

    if not force:
        instance_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm("Are you sure to restart PaaS instance %s?" %
                                instance_info)

        if not proceed:
            return

    opers = gandi.paas.restart(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers


@cli.command()
@pass_gandi
def types(gandi):
    """List types PaaS instances."""
    options = {}
    types = gandi.paas.type_list(options)
    for type_ in types:
        gandi.echo(type_['name'])

    return types


@cli.command()
@click.argument('resource')
@pass_gandi
def console(gandi, resource):
    """Open a console on a PaaS.

    Resource can be a hostname or an ID
    """
    gandi.echo('/!\ Use ~. ssh escape key to exit.')

    gandi.paas.console(resource)
