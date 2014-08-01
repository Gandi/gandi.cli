import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, limit):
    """ List vhosts. """
    options = {
        'items_per_page': limit,
    }

    output_keys = ['name', 'paas_id', 'state']

    result = gandi.vhost.list(options)
    for vhost in result:
        gandi.separator_line()
        output_generic(gandi, vhost, output_keys)

    return result

@cli.command()
@click.argument('resource', nargs=-1)
@pass_gandi
def info(gandi, resource):
    """ Display information about a vhost.

    Ressource must be the vhost fqdn.
    """
    output_keys = ['name', 'paas_id', 'state', 'date_creation']

    ret = []
    for item in resource:
        vhost = gandi.vhost.info(item)
        ret.append(output_generic(gandi, vhost, output_keys))

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
        proceed = click.confirm("Are you sure to delete vhost %s?" %
                               instance_info)

        if not proceed:
            return

    opers = gandi.vhost.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
