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



