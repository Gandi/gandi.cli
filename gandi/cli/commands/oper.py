""" Operation namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi, OPER_STEP


@cli.command()
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@click.option('--step', '-s', type=OPER_STEP, help='Filter the result by step',
              default=['BILL', 'WAIT', 'RUN'], multiple=True,
              show_default=True)
@pass_gandi
def list(gandi, limit, step):
    """List operations."""
    output_keys = ['id', 'type', 'step']

    options = {
        'step': step,
        'items_per_page': limit,
        'sort_by': 'date_created DESC'
    }

    result = gandi.oper.list(options)
    for num, oper in enumerate(reversed(result)):
        if num:
            gandi.separator_line()
        output_generic(gandi, oper, output_keys)

    return result


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """Display information about an operation."""
    output_keys = ['id', 'type', 'step', 'last_error']

    oper = gandi.oper.info(id)
    output_generic(gandi, oper, output_keys)

    return oper
