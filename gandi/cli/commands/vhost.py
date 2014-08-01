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

    if names:
        output_keys.append('paas_name')

    retrieve_paas = names
    retrieved_paas = {}

    result = gandi.vhost.list(options)
    for vhost in result:
        if vhost['paas_id'] in retrieved_paas:
            paas = retrieved_paas[vhost['paas_id']]
        else:
            paas = {'id': vhost['paas_id']}
            if retrieve_paas:
                paas = gandi.paas.info(vhost['paas_id'])

        retrieved_paas[vhost['paas_id']] = paas
        gandi.separator_line()
        output_vhost(gandi, vhost, paas, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1)
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

    retrieved_paas = {}

    ret = []
    paas = None
    for item in resource:
        vhost = gandi.vhost.info(item)

        if vhost['paas_id'] in retrieved_paas:
            paas = retrieved_paas[vhost['paas_id']]
        else:
            paas = gandi.paas.info(vhost['paas_id'])

        gandi.separator_line()
        ret.append(output_vhost(gandi, vhost, paas, output_keys))

    return ret


@cli.command()
@click.option('--vhost', help='the vhost fqdn', required=True)
@click.option('--paas', help='the paas on which we create it', required=True)
@click.option('--background', default=False, is_flag=True,
              help='run creation in background mode (default=False)')
@pass_gandi
def create(gandi, vhost, paas, background):
    """ Create a new vhost. """
    result = gandi.vhost.create(paas, vhost, background)

    if not result:
        return

    if background:
        gandi.pretty_echo(result)

    paas = gandi.paas.info(paas)
    gandi.paas.init_conf(paas['name'], vhost)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@click.option('--background', default=False, is_flag=True,
              help='run in background mode (default=False)')
@pass_gandi
def delete(gandi, resource, force, background):
    """ Delete a vhost. """
    output_keys = ['name', 'paas_id', 'state', 'date_creation']
    if not force:
        instance_info = "'%s'" % ', '.join(resource)
        proceed = click.confirm('Are you sure to delete vhost %s?' %
                                instance_info)

        if not proceed:
            return

    opers = gandi.vhost.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
