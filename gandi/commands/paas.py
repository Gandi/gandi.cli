
import click
from click.exceptions import UsageError
from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command(name='paas.list')
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@click.option('--vhosts', help='display vhosts', is_flag=True)
@pass_gandi
def list(gandi, state, id, vhosts):
    """list Paas instances"""

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

        print '%s - %s' % (paas['name'], paas['state']),
        if id:
            print '- #%d' % paas['id'],

        if vhosts:
            print '-',
            print ' / '.join(paas_hosts[paas['id']]),
        print


@cli.command(name='paas.info')
@click.argument('id')
@pass_gandi
def info(gandi, id):
    """display information about a Paas instance"""

    result = gandi.paas.info(id)
    from pprint import pprint
    pprint(result)

    return result


@cli.command()
@click.argument('vhost')
@pass_gandi
def clone(gandi, vhost):
    """clone a remote vhost in a local git repository"""

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
    """deploy code on a remote vhost"""

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
