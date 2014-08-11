import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_cert
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--id', help='display ids', is_flag=True)
@click.option('--altnames', help='display altnames', is_flag=True)
@click.option('--csr', help='display CSR', is_flag=True)
@click.option('--cert', help='display CRT', is_flag=True)
@click.option('--all-status', help='show all certificates', is_flag=True)
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, id, altnames, csr, cert, all_status, limit):
    """ List certificates. """
    options = {'items_per_page': limit}

    if not all_status:
        options['status'] = ['valid', 'pending']

    output_keys = ['cn', 'date_created', 'date_end', 'package', 'status']

    if id:
        output_keys.append('id')

    if altnames:
        output_keys.append('altnames')

    if csr:
        output_keys.append('csr')

    if cert:
        output_keys.append('cert')

    result = gandi.certificate.list(options)
    for cert in result:
        gandi.separator_line()
        output_cert(gandi, cert, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1)
@click.option('--id', help='display ids', is_flag=True)
@click.option('--altnames', help='display altnames', is_flag=True)
@click.option('--csr', help='display CSR', is_flag=True)
@click.option('--cert', help='display CRT', is_flag=True)
@click.option('--all-status', help='show all certificates', is_flag=True)
@pass_gandi
def info(gandi, resource, id, altnames, csr, cert, all_status):
    """ Display information about a certificate.

    Ressource can be a CN or an ID
    """
    output_keys = ['cn', 'date_created', 'date_end', 'package', 'status']

    if id:
        output_keys.append('id')

    if altnames:
        output_keys.append('altnames')

    if csr:
        output_keys.append('csr')

    if cert:
        output_keys.append('cert')

    ids = []
    for res in resource:
        ids.extend(gandi.certificate.usable_ids(res))

    result = []
    for id_ in set(ids):
        cert = gandi.certificate.info(id_)
        if not all_status and cert['status'] not in ['valid', 'pending']:
            continue
        gandi.separator_line()
        output_cert(gandi, cert, output_keys)
        result.append(cert)

    return result
