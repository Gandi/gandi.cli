
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.conf import pass_gandi
from gandi.cli.core.utils import output_image, check_domain_available


@cli.command()
@pass_gandi
def list(gandi):
    """List domains."""

    options = {}
    domains = gandi.domain.list(options)
    for domain in domains:
        gandi.echo(domain['fqdn'])

    return domains


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about a domain."""

    output_keys = ['fqdn', 'nameservers', 'services', 'zone_id', 'tags']

    result = gandi.domain.info(resource)
    output_image(gandi, result, output_keys)

    return result


@cli.command()
@click.option('--domain', default=None, prompt=True,
              callback=check_domain_available,
              help='Name of the domain')
@click.option('--duration', default=1, prompt=True,
              type=click.IntRange(min=1, max=10),
              help='Registration period in years, between 1 and 10')
@click.option('--owner', default=None,
              help='Registrant handle')
@click.option('--admin', default=None,
              help='Administrative contact handle')
@click.option('--tech', default=None,
              help='Technical contact handle')
@click.option('--bill', default=None,
              help='Billing contact handle')
@click.option('--background', default=False, is_flag=True,
              help='run creation in background mode (default=False)')
@pass_gandi
def create(gandi, domain, duration, owner, admin, tech, bill, background):
    """Buy a domain."""

    result = gandi.domain.create(domain, duration, owner, admin, tech, bill,
                                 background)
    if background:
        gandi.pretty_echo(result)

    return result
