""" Record namespace commands. """

import os
import click
import json

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
@click.option('--format', '-f', type=click.Choice(['text', 'json']),
              help='Choose the output format', required=False)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@click.argument('domain', required=True)
@pass_gandi
def list(gandi, domain, zone_id, output, format, limit):
    """List DNS zone records for a domain."""
    options = {
        'items_per_page': limit,
    }
    output_keys = ['name', 'type', 'value', 'ttl']

    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be '
                   'managed at Gandi.' % domain)
        return

    records = gandi.record.list(zone_id, options)

    if not output and not format:
        for num, rec in enumerate(records):
            if num:
                gandi.separator_line()
            output_generic(gandi, rec, output_keys, justify=12)
    elif output:
        zone_filename = domain + "_" + str(zone_id)
        if os.path.isfile(zone_filename):
            open(zone_filename, 'w').close()
        for record in records:
            format_record = ('%s %s IN %s %s' %
                             (record['name'], record['ttl'],
                              record['type'], record['value']))
            with open(zone_filename, 'ab') as zone_file:
                zone_file.write(format_record + '\n')
        gandi.echo('Your zone file have been writen in %s' % zone_filename)
    elif format:
        if format == 'text':
            for record in records:
                format_record = ('%s %s IN %s %s' %
                                 (record['name'], record['ttl'],
                                  record['type'], record['value']))
                gandi.echo(format_record)
        if format == 'json':
            format_record = json.dumps(records, sort_keys=True,
                                       indent=4, separators=(',', ': '))
            gandi.echo(format_record)

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
              help='Zone ID to use, if not set, default zone will be used.')
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
    if not name and not type and not value:
        proceed = click.confirm('This command without parameters --type, '
                                '--name or --value will remove all records'
                                ' in this zone file. Are you sur to '
                                'perform this action ?')
        if not proceed:
            return
    record = {'name': name, 'type': type, 'value': value}
    result = gandi.record.delete(zone_id, record)
    return result


@cli.command()
@click.option('--zone-id', '-z', default=None, type=click.INT,
              help='Zone ID to use, if not set, default zone will be used.')
@click.option('--file', '-f', type=click.File('r'),
              required=False, help='Filename of the zone file.')
@click.option('--record', '-r', default=None, required=False,
              help="'name TTL IN TYPE [A, AAAA, MX, TXT, SPF] value'")
@click.option('--new-record', default=None, required=False,
              help="'name TTL IN TYPE [A, AAAA, MX, TXT, SPF] value'")
@click.argument('domain', required=True)
@pass_gandi
def update(gandi, domain, zone_id, file, record, new_record):
    """Update records entries for a domain from a file"""
    if not zone_id:
        result = gandi.domain.info(domain)
        zone_id = result['zone_id']

    if not zone_id:
        gandi.echo('No zone records found, domain %s doesn\'t seems to be'
                   ' managed at Gandi.' % domain)
        return
    if file:
        records = file.read()
        result = gandi.record.zone_update(zone_id, records)
        return result
    elif record and new_record:
        result = gandi.record.update(zone_id, record, new_record)
        return result
    else:
        gandi.echo('You must indicate a zone file or a record.'
                   ' Use `gandi record update --help` for more information')
