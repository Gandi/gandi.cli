
import click
from gandi.cli.__main__ import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import read_ssh_key


@cli.command(name='paas.list')
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@click.option('--vhosts', help='display vhosts', is_flag=True)
@pass_gandi
def list(gandi, state, id, vhosts):
    """List Paas instances."""

    options = {}
    if state:
        options['state'] = state

    paas_hosts = {}
    result = gandi.paas.list(options)
    for paas in result:
        paas_hosts[paas['id']] = []
        if vhosts:
            list_vhost = gandi.vhost.list({'paas_id': paas['id']})
            for host in list_vhost:
                paas_hosts[paas['id']].append(host['name'])

        msg = '%s - %s' % (paas['name'], paas['state'])
        if id:
            msg += ' - # %d' % paas['id']

        if vhosts:
            msg += ' - %s' % (' / '.join(paas_hosts[paas['id']]))

        gandi.echo(msg)


@cli.command(name='paas.info')
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """Display information about a Paas instance."""

    result = gandi.paas.info(id)
    gandi.pretty_echo(result)

    return result


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

    result = gandi.paas.delete(id)
    gandi.pretty_echo(result)

    return result


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
@click.option('--datacenter_id', type=click.INT, default=None,
              help='id of the datacenter where the PaaS will be spawned')
@click.option('--vhosts', default=0,
              help='List of virtual hosts to be linked to the instance')
@click.option('--password', default=None,
              help='Password of the PaaS instance')
@click.option('--snapshot_profile', default=None,
              help='Set a snapshot profile associated to this paas disk')
@click.option('--interactive', default=False, is_flag=True,
              help='run creation in interactive mode (default=False)')
@click.argument('ssh_key', default=None, type=click.File('rb'), required=False,
                callback=read_ssh_key)
@pass_gandi
def create(gandi, name, size, type, quantity, duration, datacenter_id, vhosts,
           password, snapshot_profile, interactive, ssh_key):
    """Create a new PaaS instance.

    you can provide a ssh_key on command line calling this command as:

    >>> cat ~/.ssh/id_rsa.pub | gandi paas -

    or specify a configuration entry named 'ssh_key_path' containing
    path to your ssh_key file

    >>> gandi config ssh_key_path ~/.ssh/id_rsa.pub

    """

    result = gandi.paas.create(name, size, type, quantity, duration,
                               datacenter_id, vhosts, password,
                               snapshot_profile, interactive, ssh_key)
    gandi.pretty_echo(result)
