import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_cert
from gandi.cli.core.params import pass_gandi, CERTIFICATE_PACKAGE


@cli.command(options_metavar='')
@pass_gandi
def packages(gandi):
    """ List certificate packages. """
    packages = gandi.certificate.package_list()

    for package in sorted(packages,
                          lambda a, b: cmp("%02d%03d%s" % (a['category']['id'],
                                                           a['max_domains'],
                                                           a['name']),
                                           "%02d%03d%s" % (b['category']['id'],
                                                           b['max_domains'],
                                                           b['name']))):
        gandi.echo(package['name'])

    return packages


@cli.command()
@click.option('--id', help='display ids', is_flag=True)
@click.option('--altnames', help='display altnames', is_flag=True)
@click.option('--csr', help='display CSR', is_flag=True)
@click.option('--cert', help='display CRT', is_flag=True)
@click.option('--all-status', help='show all certificates', is_flag=True)
@click.option('--status', help='display status', is_flag=True)
@click.option('--dates', help='display dates', is_flag=True)
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, id, altnames, csr, cert, all_status, status, dates, limit):
    """ List certificates. """
    options = {'items_per_page': limit}

    if not all_status:
        options['status'] = ['valid', 'pending']

    output_keys = ['cn', 'package']

    if id:
        output_keys.append('id')

    if status:
        output_keys.append('status')

    if dates:
        output_keys.extend(['date_created', 'date_end'])

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
