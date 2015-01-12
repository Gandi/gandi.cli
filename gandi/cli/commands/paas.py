""" PaaS instances namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_paas, output_generic, randomstring
from gandi.cli.core.params import pass_gandi, DATACENTER, PAAS_TYPE, option


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
@pass_gandi
def info(gandi, resource):
    """Display information about a PaaS instance.

    Resource can be a vhost, a hostname, or an ID
    """
    output_keys = ['name', 'type', 'size', 'memory', 'console', 'vhost',
                   'dc', 'sftp_server', 'git_server']

    paas = gandi.paas.info(resource)
    paas_hosts = []
    list_vhost = gandi.vhost.list({'paas_id': paas['id']})

    df = gandi.paas.quota(paas['id'])
    paas.update({'df': df})

    for host in list_vhost:
        paas_hosts.append(host['name'])

    output_paas(gandi, paas, [], paas_hosts, output_keys)

    return paas


@cli.command()
@click.argument('vhost', required=False)
@pass_gandi
def clone(gandi, vhost):
    """Clone a remote vhost in a local git repository."""
    paas_access = gandi.get('paas.access')
    if not vhost and not paas_access:
        gandi.error('missing VHOST parameter')

    if vhost and not paas_access:
        paas_info = gandi.paas.info(vhost)
        gandi.vhost.init_vhost(vhost, paas=paas_info)
    else:
        paas_access = gandi.get('paas.access')
        gandi.execute('git clone ssh+git://%s/%s.git' % (paas_access, vhost))


@cli.command(root=True)
@click.argument('vhost', required=False)
@pass_gandi
def deploy(gandi, vhost):
    """Deploy code on a remote vhost."""
    paas_access = gandi.get('paas.access')
    if not vhost and not paas_access:
        gandi.error('missing VHOST parameter')

    if vhost and not paas_access:
        gandi.paas.init_conf(vhost, vhost=vhost)

    paas_access = gandi.get('paas.access')
    deploy_git_host = gandi.get('paas.deploy_git_host')

    gandi.execute("ssh %s 'deploy %s'" % (paas_access, deploy_git_host))


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
        type=click.Choice(['s', 'm', 'x', 'xl', 'xxl']),
        help='Size of the PaaS instance.')
@option('--type', default='pythonpgsql',
        type=PAAS_TYPE,
        help='Type of the PaaS instance.')
@option('--quantity', default=0,
        help='Additional disk amount (in GB).')
@option('--duration', default='1m',
        help='Number of month, suffixed with m.')
@option('--datacenter', type=DATACENTER, default='LU',
        help='Datacenter where the PaaS will be spawned.')
@click.option('--vhosts', default=None, multiple=True,
              help='List of virtual hosts to be linked to the instance.')
@click.option('--password', help='Use command-line supplied password.')
@click.option('--snapshotprofile', default=None,
              help='Set a snapshot profile associated to this paas disk.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@option('--sshkey', multiple=True,
        help='Authorize ssh authentication for the given ssh key.')
@pass_gandi
def create(gandi, name, size, type, quantity, duration, datacenter, vhosts,
           password, snapshotprofile, background, sshkey):
    """Create a new PaaS instance and initialize associated git repository.

    you can specify a configuration entry named 'sshkey' containing
    path to your sshkey file

    $ gandi config -g sshkey ~/.ssh/id_rsa.pub

    or getting the sshkey "my_key" from your gandi ssh keyring

    $ gandi config -g sshkey my_key

    to know which PaaS instance type to use as type

    $ gandi paas types

    """
    if not password:
        password = click.prompt('password', hide_input=True,
            confirmation_prompt=True)

    if not name:
        name = randomstring('vm')

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
@click.option('--upgrade', default=None,
              help='Upgrade the instance to the last system image if needed.')
@click.option('--console', default=None,
              help='Activate or deactivate the Console.')
@click.option('--snapshotprofile', default=None,
              help='Set a snapshot profile associated to this paas disk.')
@click.option('--reset-mysql-password', default=None,
              help='Reset mysql password for root.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@pass_gandi
@click.argument('resource')
def update(gandi, resource, name, size, quantity, password, sshkey,
           upgrade, console, snapshotprofile, reset_mysql_password,
           background):
    """Update a PaaS instance.

    Resource can be a Hostname or an ID
    """
    pwd = None
    if password:
        pwd = click.prompt('password', hide_input=True,
                           confirmation_prompt=True)

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
