
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import output_image


@cli.command(name='domains')
@pass_gandi
def list(gandi):
    """List domains."""

    options = {}
    domains = gandi.domain.list(options)
    for domain in domains:
        gandi.echo(domain['fqdn'])

    return domains


@cli.command(name='domain')
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about a domain."""

    output_keys = ['fqdn', 'nameservers', 'services', 'zone_id', 'tags']

    result = gandi.domain.info(resource)
    output_image(gandi, result, output_keys)

    return result
