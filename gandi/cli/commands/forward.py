""" Forward namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_forward
from gandi.cli.core.params import pass_gandi, EMAIL_TYPE


@cli.command()
@click.option('--limit', help='Limit number of results.',
              default=100, show_default=True)
@click.argument('domain', metavar='domain.tld')
@pass_gandi
def list(gandi, domain, limit):
    """List mail forwards for a domain."""
    options = {'items_per_page': limit}
    result = gandi.forward.list(domain, options)
    for forward in result:
        output_forward(gandi, domain, forward)
    return result


@cli.command()
@click.option('--destination', '-d', help='Add forward destination.',
              multiple=True, required=True)
@click.argument('address', type=EMAIL_TYPE, metavar='address@domain.tld')
@pass_gandi
def create(gandi, address, destination):
    """Create a domain mail forward."""
    source, domain = address

    result = gandi.forward.create(domain, source, destination)

    return result


@cli.command()
@click.option('--dest-add', '-a', help='Add forward destination.',
              multiple=True, required=False)
@click.option('--dest-del', '-d', help='Delete forward destination.',
              multiple=True, required=False)
@click.argument('address', type=EMAIL_TYPE, metavar='address@domain.tld')
@pass_gandi
def update(gandi, address, dest_add, dest_del):
    """Update a domain mail forward."""
    source, domain = address

    if not dest_add and not dest_del:
        gandi.echo('Nothing to update: you must provide destinations to '
                   'update, use --dest-add/-a or -dest-del/-d parameters.')
        return

    result = gandi.forward.update(domain, source, dest_add, dest_del)

    return result


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('address', type=EMAIL_TYPE, metavar='address@domain.tld')
@pass_gandi
def delete(gandi, address, force):
    """Delete a domain mail forward."""
    source, domain = address

    if not force:
        proceed = click.confirm('Are you sure to delete the domain '
                                'mail forward %s@%s ?' % (source, domain))

        if not proceed:
            return

    result = gandi.forward.delete(domain, source)

    return result
