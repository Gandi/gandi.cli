import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_vhost
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@click.option('--ids', help='display ids', is_flag=True)
@click.option('--names', help='display namess', is_flag=True)
@pass_gandi
def list(gandi, limit, ids, names):
    """ List vhosts. """
    options = {
        'items_per_page': limit,
    }

    output_keys = ['name', 'state', 'date_creation']
    if ids:
        output_keys.append('paas_id')

    paas_names = {}
    if names:
        output_keys.append('paas_name')
        paas_names = gandi.paas.list_names()

    result = gandi.vhost.list(options)
    for vhost in result:
        paas = paas_names.get(vhost['paas_id'])
        gandi.separator_line()
        output_vhost(gandi, vhost, paas, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--ids', help='display ids', is_flag=True)
@pass_gandi
def info(gandi, resource, ids):
    """ Display information about a vhost.

    Ressource must be the vhost fqdn.
    """
    output_keys = ['name', 'state', 'date_creation', 'paas_name']

    if ids:
        # When we will have more than paas vhost, we will append rproxy_id
        output_keys.append('paas_id')

    paas_names = gandi.paas.list_names()

    ret = []
    paas = None
    for item in resource:
        vhost = gandi.vhost.info(item)
        paas = paas_names.get(vhost['paas_id'])
        gandi.separator_line()
        ret.append(output_vhost(gandi, vhost, paas, output_keys))

    return ret


@cli.command()
@click.option('--vhost', help='the vhost fqdn', required=True)
@click.option('--paas', help='the paas on which we create it', required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
@pass_gandi
def create(gandi, vhost, paas, background):
    """ Create a new vhost. """
    result = gandi.vhost.create(paas, vhost, background)

    if not result:
        return

    if background:
        gandi.pretty_echo(result)
    else:
        paas = gandi.paas.info(paas)
        gandi.paas.init_conf(paas['name'], vhost)

    return result


@cli.command()
@click.argument('resource', required=True)
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
@pass_gandi
def delete(gandi, resource, force, background):
    """ Delete a vhost. """
    output_keys = ['name', 'paas_id', 'state', 'date_creation']
    if not force:
        proceed = click.confirm('Are you sure to delete vhost %s?' %
                                resource)

        if not proceed:
            return

    opers = gandi.vhost.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
