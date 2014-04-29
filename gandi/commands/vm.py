
import click
from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@pass_gandi
def list(gandi, state):
    """list user vm."""

    options = {}
    if state:
        options['state'] = state

    result = gandi.call('vm.list', options)

    for vm in result:
        print '#%d - %s - %s' % (vm['id'], vm['hostname'], vm['state'])


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """info for a user vm."""

    result = gandi.call('vm.info', (id, ))
    from pprint import pprint
    pprint(result)
