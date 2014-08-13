import os
import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_cert
from gandi.cli.core.params import (pass_gandi, CERTIFICATE_PACKAGE, IntChoice,
                                   option)


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


@cli.command()
@click.argument('resource', nargs=-1)
@click.option('-o', '--output', help='the file to write the cert')
@pass_gandi
def export(gandi, resource, output):
    """ Write the certificate to <output> or <fqdn>.crt

    Ressource can be a CN or an ID
    """
    ids = []
    for res in resource:
        ids.extend(gandi.certificate.usable_ids(res))

    if output and len(ids) > 1:
        gandi.echo('Do not know which cert you want to export.')
        return

    for id_ in set(ids):
        cert = gandi.certificate.info(id_)
        if not 'cert' in cert:
            continue

        crt_filename = output or cert['cn'] + '.crt'
        if os.path.exists(crt_filename):
            gandi.echo('The file %s already exists.' % crt_filename)
            continue

        crt = gandi.certificate.pretty_format_cert(cert)
        if crt:
            with open(crt_filename, 'w') as crt_file:
                crt_file.write(crt)
                gandi.echo('wrote %s' % crt_filename)

        return crt


@cli.command()
@click.option('--csr', help='Csr of the new certificate', required=False)
@click.option('--pk', '--private-key', required=False,
              help='Private key to use to generate the CSR')
@click.option('--cn', '--common-name', required=False,
              help='Common name to use when generating the CSR')
@click.option('--c', '--country', required=False,
              help='The generated CSR country (C)')
@click.option('--st', '--state', required=False,
              help='The generated CSR state (ST)')
@click.option('--l', '--city', required=False,
              help='The generated CSR location (L)')
@click.option('--o', '--organisation', required=False,
              help='The generated CSR organisation (O)')
@click.option('--ou', '--branch', required=False,
              help='The generated CSR branch (OU)')
@click.option('-d', '--duration', default=1,
              type=IntChoice(['1', '2', '3', '4', '5']),
              help='The certificate duration in year')
@option('--package', default='cert_std_1_0_0', type=CERTIFICATE_PACKAGE,
        help='Certificate package')
# dcv method (email, dns, file, auto)
# altnames
@pass_gandi
def create(gandi, csr, private_key, common_name, country, state, city,
           organisation, branch, duration, package):
    """Create a new certificate.
    """
    if not (csr or common_name):
        gandi.echo('You need a CSR or a CN to create a certificate.')
        return

    if csr:
        if branch or organisation or city or state or country:
            gandi.echo('Following options are only used to generate the CSR.')
    else:
        params = (('CN', common_name),
                  ('OU', branch),
                  ('O', organisation),
                  ('L', city),
                  ('ST', state),
                  ('C', country))
        params = [(key, val) for key, val in params if val]
        subj = '/'.join(['='.join(value) for value in params])
        csr = gandi.certificate.create_csr(common_name, private_key, params)
        if not csr:
            return

    if os.path.exists(csr):
        csr = open(csr).read()

    result = gandi.certificate.create(csr, duration, package)

    return result


@cli.command()
@click.argument('resource', nargs=1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False)')
@pass_gandi
def delete(gandi, resource, background, force):
    """ Write the certificate to <output> or <fqdn>.crt

    Ressource can be a CN or an ID
    """
    ids = gandi.certificate.usable_ids(resource)

    if len(ids) > 1:
        gandi.echo('Will not delete, %s is not precise enough.' % resource)
        gandi.echo('  * cert : ' +
                   '\n  * cert : '.join([str(id_) for id_ in ids]))
        return

    if not force:
        proceed = click.confirm("Are you sure to delete the certificate %s?" %
                                resource)
        if not proceed:
            return

    result = gandi.certificate.delete(ids[0], background)
    return result
