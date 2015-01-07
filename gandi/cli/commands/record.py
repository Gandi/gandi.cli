""" Record namespace commands. """

import os
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_generic,
)
from gandi.cli.core.params import pass_gandi, StringConstraint


@cli.command()
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID to use, if not set default zone will be used.')
@click.option('--output', '-o', is_flag=True,
              help='Write the records into a file.')
@click.argument('domain', required=True)
@pass_gandi
def list(gandi, domain, zone_id, output):
    """List DNS zone records for a domain."""
    output_keys = ['name', 'type', 'value', 'ttl']

    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be '
                   'managed at Gandi.' % domain)
        return

    records = gandi.record.list(zone_id)
    if not output:
        for num, rec in enumerate(records):
            if num:
                gandi.separator_line()
            output_generic(gandi, rec, output_keys, justify=12)
    else:
        zone_filename = domain + "_" + str(zone_id)
        if os.path.exists(zone_filename):
            open(zone_filename, 'w').close()
        for record in records:
            with open(zone_filename, 'ab') as zone_file:
                zone_file.write('%s %s IN %s %s\n' %
                                (record['name'], record['ttl'],
                                 record['type'], record['value']))

        gandi.echo('Your zone file have been writen in %s' % zone_filename)

    return records


@cli.command()
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

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be '
                   'managed at Gandi.' % domain)
        return

    record = {'type': type, 'name': name, 'value': value}
    if ttl:
        record['ttl'] = ttl

    result = gandi.record.create(zone_id, record)
    return result


@cli.command()
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID tu use, if not set, default zone will be used.')
@click.option('--name', default=None,
              help='Relative name of the record to delete.')
@click.option('--type', default=None,
              type=click.Choice(['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT',
                                 'WKS', 'SRV', 'LOC', 'SPF']),
              help='DNS record type')
@click.option('--value', default=None,
              type=StringConstraint(minlen=1, maxlen=1024))
@click.argument('domain', required=True)
@pass_gandi
def delete(gandi, domain, zone_id, name, type, value):
    """Delete a record entry for a domain"""
    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be '
                   'managed at Gandi.' % domain)
        return

    record = {'name': name, 'type': type, 'value': value}
    result = gandi.record.delete(zone_id, record)
    return result


@cli.command()
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID tu use, if not set, default zone will be used.')
@click.option('--file', '-f', type=click.File('r'),
              required=True, help='Filename of the zone file.')
@click.argument('domain', required=True)
@pass_gandi
def update(gandi, domain, zone_id, file):
    """Update all records entries for a domain from a file"""
    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be '
                   'managed at Gandi.' % domain)

    records = file.read()
    result = gandi.record.update(zone_id, records)
    return result
