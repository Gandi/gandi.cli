""" Domain namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.params import pass_gandi, DNSSEC_FLAGS, DNSSEC_ALGORITHM


@cli.group(name='dnssec')
@pass_gandi
def dnssec(gandi):
    """Commands related to dnssec."""


@dnssec.command()
@click.option('--flags', default=None, type=DNSSEC_FLAGS,
              help='Flags (ZSK or KSK)')
@click.option('--algorithm', default=None, type=DNSSEC_ALGORITHM,
              help='Algorithm')
@click.option('--public_key', default=None, help='Public key (base64-encoded)')
@click.argument('resource')
@pass_gandi
def create(gandi, resource, flags, algorithm, public_key):
    """Create DNSSEC key."""

    result = gandi.dnssec.create(resource, flags, algorithm, public_key)

    return result


@dnssec.command()
@click.argument('resource')
@pass_gandi
def list(gandi, resource):
    """List DNSSEC keys."""
    keys = gandi.dnssec.list(resource)
    gandi.pretty_echo(keys)

    return keys


@dnssec.command()
@click.argument('resource', type=click.INT)
@pass_gandi
def delete(gandi, resource):
    """Delete DNSSEC key.
    """

    result = gandi.dnssec.delete(resource)
    gandi.echo('Delete successful.')

    return result
