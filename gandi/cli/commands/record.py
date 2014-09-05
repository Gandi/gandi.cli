""" Record namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_generic,
)
from gandi.cli.core.params import pass_gandi, StringConstraint


@cli.command(options_metavar='')
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID to use, if not set default zone will be used.')
@click.argument('domain', required=True)
@pass_gandi
def list(gandi, domain, zone_id):
    """List DNS zone records for a domain."""
    output_keys = ['name', 'type', 'value', 'ttl']

    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    records = gandi.record.list(zone_id)
    for rec in records:
        gandi.separator_line()
        output_generic(gandi, rec, output_keys, justify=12)

    return records


@cli.command(options_metavar='')
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID to use, if not set, default zone will be used.')
@click.option('--name', default=None, required=True,
              help='Relative name, may contain leading wildcard. '
                   '`@` for empty name')
@click.option('--type', default=None, required=True,
              type=click.Choice(['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT',
                                 'WKS', 'SRV', 'LOC', 'SPF']),
              help='DNS record type')
@click.option('--value', default=None, required=True,
              type=StringConstraint(minlen=1, maxlen=1024),
              help='Value for record. Semantics depends on the record type.'
                   'Currently limited to 1024 ASCII characters.'
                   'In case of TXT, each part between quotes is limited to 255'
                   ' characters')
@click.option('--ttl', default=None, required=False,
              type=click.IntRange(min=300, max=2592000),
              help='Time to live, in seconds, between 5 minutes and 30 days')
@click.argument('domain', required=True)
@pass_gandi
def create(gandi, domain, zone_id, name, type, value, ttl):
    """Create new DNS zone record entry for a domain."""

    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    record = {'type': type, 'name': name, 'value': value}
    if ttl:
        record['ttl'] = ttl

    result = gandi.record.create(zone_id, record)
    return result
