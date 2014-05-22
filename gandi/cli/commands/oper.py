
import click
from gandi.cli.__main__ import cli
from gandi.cli.core.conf import pass_gandi


@cli.command(name='oper.list')
@pass_gandi
def list(gandi):
    """list operation"""

    options = {
        'step': ['WAIT', 'RUN'],
    }

    result = gandi.oper.list(options)
    gandi.pretty_echo(result)

    return result


@cli.command(name='oper.info')
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """display information about an operation"""

    result = gandi.oper.info(id)
    gandi.pretty_echo(result)

    return result
