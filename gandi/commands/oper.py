
import click
from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command(name='oper.list')
@pass_gandi
def list(gandi):
    """list operation"""

    options = {
        'step': ['WAIT', 'RUN'],
    }

    result = gandi.oper.list(options)
    from pprint import pprint
    pprint(result)

    return result


@cli.command(name='oper.info')
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """display information about an operation"""

    result = gandi.oper.info(id)
    from pprint import pprint
    pprint(result)

    return result
