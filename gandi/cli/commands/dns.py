""" DNS namespace commands. """

import sys
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_dns_records, output_generic
from gandi.cli.core.params import pass_gandi, DNS_RECORDS


@cli.group(name='dns')
@pass_gandi
def dns(gandi):
    """Commands related to LiveDNS."""


@dns.command('domain.list')
@pass_gandi
def domain_list(gandi):
    """List domains manageable by REST API."""
    domains = gandi.dns.list()
    for domain in domains:
        gandi.echo(domain['fqdn'])

    return domains


@dns.command()
@click.argument('fqdn')
@click.argument('name', default=None, required=False)
@click.argument('rrset_type', default=None, required=False, type=DNS_RECORDS)
@click.option('--sort', default='name',
              type=click.Choice(['name', 'ttl', 'type', 'values']),
              help='Sort results (does not work with text option).')
@click.option('--type', default=None, type=DNS_RECORDS,
              help='Filter results by type (does not work with text option).')
@click.option('--text', default=False, is_flag=True,
              help='Output result as text.')
@pass_gandi
def list(gandi, fqdn, name, sort, type, rrset_type, text):
    """Display records for a domain."""
    domains = gandi.dns.list()
    domains = [domain['fqdn'] for domain in domains]
    if fqdn not in domains:
        gandi.echo('Sorry domain %s does not exist' % fqdn)
        gandi.echo('Please use one of the following: %s' % ', '.join(domains))
        return

    output_keys = ['name', 'ttl', 'type', 'values']

    result = gandi.dns.records(fqdn, sort_by=sort, text=text)
    if text:
        gandi.echo(result)
        return result

    for num, rec in enumerate(result):
        if type and rec['rrset_type'] != type:
            continue
        if rrset_type and rec['rrset_type'] != rrset_type:
            continue
        if name and rec['rrset_name'] != name:
            continue
        if num:
            gandi.separator_line()
        output_dns_records(gandi, rec, output_keys)

    return result


@dns.command()
@click.argument('fqdn')
@click.argument('name')
@click.argument('type', type=DNS_RECORDS)
@click.argument('value', nargs=-1, required=True)
@click.option('--ttl', default=None, type=click.INT, required=False,
              help='Time to live, in seconds')
@pass_gandi
def create(gandi, fqdn, name, type, value, ttl):
    """Create new record entry for a domain.

    multiple value parameters can be provided.
    """
    domains = gandi.dns.list()
    domains = [domain['fqdn'] for domain in domains]
    if fqdn not in domains:
        gandi.echo('Sorry domain %s does not exist' % fqdn)
        gandi.echo('Please use one of the following: %s' % ', '.join(domains))
        return

    result = gandi.dns.add_record(fqdn, name, type, value, ttl)
    gandi.echo(result['message'])


@dns.command()
@click.argument('fqdn')
@click.argument('name', required=False)
@click.argument('type', type=DNS_RECORDS, required=False)
@click.argument('value', nargs=-1, required=False)
@click.option('--ttl', default=None, type=click.INT, required=False,
              help='Time to live, in seconds')
@click.option('-f', '--file', type=click.File('rb'),
              help='Zone content in a plain text file. If provided this will '
                   'ignore all other parameters and overwrite current zone '
                   'content')
@pass_gandi
def update(gandi, fqdn, name, type, value, ttl, file):
    """Update record entry for a domain.

    --file option will ignore other parameters and overwrite current zone
    content with provided file content.
    """
    domains = gandi.dns.list()
    domains = [domain['fqdn'] for domain in domains]
    if fqdn not in domains:
        gandi.echo('Sorry domain %s does not exist' % fqdn)
        gandi.echo('Please use one of the following: %s' % ', '.join(domains))
        return

    content = ''
    if file:
        content = file.read()
    elif not sys.stdin.isatty():
        content = click.get_text_stream('stdin').read()

    content = content.strip()
    if not content and not name and not type and not value:
        click.echo('Cannot find parameters for zone content to update.')
        return

    if name and type and not value:
        click.echo('You must provide one or more value parameter.')
        return

    result = gandi.dns.update_record(fqdn, name, type, value, ttl, content)
    gandi.echo(result['message'])


@dns.command()
@click.argument('fqdn')
@click.argument('name', required=False)
@click.argument('type', type=DNS_RECORDS, required=False)
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def delete(gandi, fqdn, name, type, force):
    """Delete record entry for a domain."""
    domains = gandi.dns.list()
    domains = [domain['fqdn'] for domain in domains]
    if fqdn not in domains:
        gandi.echo('Sorry domain %s does not exist' % fqdn)
        gandi.echo('Please use one of the following: %s' % ', '.join(domains))
        return

    if not force:
        if not name and not type:
            prompt = ("Are you sure to delete all records for domain %s ?" %
                      fqdn)
        elif name and not type:
            prompt = ("Are you sure to delete all '%s' name records for "
                      "domain %s ?" % (name, fqdn))
        else:
            prompt = ("Are you sure to delete all '%s' records of type %s "
                      "for domain %s ?" % (name, type, fqdn))

        proceed = click.confirm(prompt)

        if not proceed:
            return

    result = gandi.dns.del_record(fqdn, name, type)
    gandi.echo('Delete successful.')
    return result


@dns.group(name='keys')
@pass_gandi
def keys(gandi):
    """Commands related to LiveDNS DNSSEC keys."""


@keys.command(name='list')
@click.argument('fqdn')
@pass_gandi
def keys_list(gandi, fqdn):
    """List domain keys."""
    keys = gandi.dns.keys(fqdn)
    output_keys = ['uuid', 'algorithm', 'algorithm_name', 'ds', 'flags',
                   'status']
    for num, key in enumerate(keys):
        if num:
            gandi.separator_line()
        output_generic(gandi, key, output_keys, justify=15)
    return keys


@keys.command(name='info')
@click.argument('fqdn')
@click.argument('key')
@pass_gandi
def keys_info(gandi, fqdn, key):
    """Display information about a domain key."""
    key_info = gandi.dns.keys_info(fqdn, key)
    output_keys = ['uuid', 'algorithm', 'algorithm_name', 'ds', 'fingerprint',
                   'public_key', 'flags', 'tag', 'status']
    output_generic(gandi, key_info, output_keys, justify=15)
    return key_info


@keys.command(name='create')
@click.argument('fqdn')
@click.argument('flag', type=click.Choice(['256', '257']))
@pass_gandi
def keys_create(gandi, fqdn, flag):
    """Create key for a domain."""
    key_info = gandi.dns.keys_create(fqdn, int(flag))

    output_keys = ['uuid', 'algorithm', 'algorithm_name', 'ds', 'fingerprint',
                   'public_key', 'flags', 'tag', 'status']
    output_generic(gandi, key_info, output_keys, justify=15)
    return key_info


@keys.command(name='delete')
@click.argument('fqdn')
@click.argument('key')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def keys_delete(gandi, fqdn, key, force):
    """Delete a key for a domain."""
    if not force:
        proceed = click.confirm('Are you sure you want to delete key %s on '
                                'domain %s?' % (key, fqdn))

        if not proceed:
            return

    result = gandi.dns.keys_delete(fqdn, key)
    gandi.echo('Delete successful.')
    return result


@keys.command(name='recover')
@click.argument('fqdn')
@click.argument('key')
@pass_gandi
def keys_recover(gandi, fqdn, key):
    """Recover deleted key for a domain."""
    result = gandi.dns.keys_recover(fqdn, key)
    gandi.echo('Recover successful.')
    return result
