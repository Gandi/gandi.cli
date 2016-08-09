""" Hosted certificate namespace commands. """

import os
import click

# define basestring for python3
try:
    basestring
except NameError:
    basestring = (str, bytes)

type_list = list

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_hostedcert
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--vhosts', help='Display related vhosts.', is_flag=True)
@click.option('--dates', help='Display dates.', is_flag=True)
@click.option('--fqdns', help='Display fqdns.', is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, id, vhosts, dates, fqdns, limit):
    """ List hosted certificates. """
    justify = 10
    options = {'items_per_page': limit, 'state': 'created'}

    output_keys = []

    if id:
        output_keys.append('id')

    output_keys.append('subject')

    if dates:
        output_keys.extend(['date_created', 'date_expire'])
        justify = 12

    if fqdns:
        output_keys.append('fqdns')

    if vhosts:
        output_keys.append('vhosts')

    result = gandi.hostedcert.list(options)

    for num, hcert in enumerate(result):
        if num:
            gandi.separator_line()

        if fqdns or vhosts:
            hcert = gandi.hostedcert.info(hcert['id'])

        output_hostedcert(gandi, hcert, output_keys, justify)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def info(gandi, resource):
    """ Display information about a hosted certificate.

    Resource can be a FQDN or an ID
    """
    output_keys = ['id', 'subject', 'date_created', 'date_expire',
                   'fqdns', 'vhosts']

    result = gandi.hostedcert.infos(resource)
    for num, hcert in enumerate(result):
        if num:
            gandi.separator_line()
        output_hostedcert(gandi, hcert, output_keys)

    return result


@cli.command()
@click.option('--pk', '--private-key', required=True,
              help='Private key used to generate this CRT.')
@click.option('--crt', '--certificate', required=False,
              help='The certificate.')
@click.option('--crt-id', '--certificate-id', type=click.INT, required=False,
              help='The certificate.')
@pass_gandi
def create(gandi, private_key, certificate, certificate_id):
    """ Create a new hosted certificate. """
    if not certificate and not certificate_id:
        gandi.echo('One of --certificate or --certificate-id is needed.')
        return
    if certificate and certificate_id:
        gandi.echo('Only one of --certificate or --certificate-id is needed.')

    if os.path.isfile(private_key):
        with open(private_key) as fhandle:
            private_key = fhandle.read()

    if certificate:
        if os.path.isfile(certificate):
            with open(certificate) as fhandle:
                certificate = fhandle.read()
    else:
        cert = gandi.certificate.info(certificate_id)
        certificate = gandi.certificate.pretty_format_cert(cert)

    result = gandi.hostedcert.create(private_key, certificate)

    output_keys = ['id', 'subject', 'date_created', 'date_expire',
                   'fqdns', 'vhosts']

    output_hostedcert(gandi, result, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def delete(gandi, resource, force):
    """ Delete a hosted certificate.

    Resource can be a FQDN or an ID
    """
    infos = gandi.hostedcert.infos(resource)
    if not infos:
        return

    if not force:
        proceed = click.confirm('Are you sure to delete the following hosted '
                                'certificates ?\n' +
                                '\n'.join(['%s: %s' % (res['id'],
                                                       res['subject'])
                                           for res in infos]) + '\n')
        if not proceed:
            return

    for res in infos:
        gandi.hostedcert.delete(res['id'])
