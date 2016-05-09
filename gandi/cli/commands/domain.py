""" Domain namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_contact_info, output_domain
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, limit):
    """List domains."""
    options = {'items_per_page': limit}
    domains = gandi.domain.list(options)
    for domain in domains:
        gandi.echo(domain['fqdn'])

    return domains


@cli.command()
@click.argument('resource')
@pass_gandi
def info(gandi, resource):
    """Display information about a domain."""
    output_keys = ['fqdn', 'nameservers', 'services', 'zone_id', 'tags',
                   'created', 'expires', 'updated']
    contact_field = ['owner', 'admin', 'bill', 'tech', 'reseller']

    result = gandi.domain.info(resource)
    output_contact_info(gandi, result['contacts'], contact_field, justify=12)
    output_domain(gandi, result, output_keys, justify=12)

    return result


@cli.command()
@click.option('--domain', default=None, help='Name of the domain.')
@click.option('--duration', default=1, prompt=True,
              type=click.IntRange(min=1, max=10),
              help='Registration period in years, between 1 and 10.')
@click.option('--owner', default=None,
              help='Registrant handle.')
@click.option('--admin', default=None,
              help='Administrative contact handle.')
@click.option('--tech', default=None,
              help='Technical contact handle.')
@click.option('--bill', default=None,
              help='Billing contact handle.')
@click.option('--nameserver', default=None,
              help='Nameserver', multiple=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', metavar='DOMAIN', required=False)
@pass_gandi
def create(gandi, resource, domain, duration, owner, admin, tech, bill,
           nameserver, background):
    """Buy a domain."""
    if domain:
        gandi.echo('/!\ --domain option is deprecated and will be removed '
                   'upon next release.')
        gandi.echo("You should use 'gandi domain create %s' instead." % domain)

    if (domain and resource) and (domain != resource):
        gandi.echo('/!\ You specified both an option and an argument which '
                   'are different, please choose only one between: %s and %s.'
                   % (domain, resource))
        return

    _domain = domain or resource
    if not _domain:
        _domain = click.prompt('Name of the domain')

    result = gandi.domain.create(_domain, duration, owner, admin, tech, bill,
                                 nameserver, background)
    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--duration', default=1, prompt=True,
              type=click.IntRange(min=1, max=10),
              help='Registration period in years, between 1 and 10.')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('domain')
@pass_gandi
def renew(gandi, domain, duration, background):
    """Renew a domain."""
    result = gandi.domain.renew(domain, duration, background)
    if background:
        gandi.pretty_echo(result)

    return result
