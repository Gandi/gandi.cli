""" Certificate namespace commands. """

import os
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_cert
from gandi.cli.core.params import (pass_gandi, IntChoice,
                                   CERTIFICATE_PACKAGE, CERTIFICATE_DCV_METHOD)


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
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--altnames', help='Display altnames.', is_flag=True)
@click.option('--csr', help='Display CSR.', is_flag=True)
@click.option('--cert', help='Display CRT.', is_flag=True)
@click.option('--all-status', is_flag=True,
              help='Filter the certificate without regard to its status.')
@click.option('--status', help='Display status.', is_flag=True)
@click.option('--dates', help='Display dates.', is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
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
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--altnames', help='Display altnames.', is_flag=True)
@click.option('--csr', help='Display CSR.', is_flag=True)
@click.option('--cert', help='Display CRT.', is_flag=True)
@click.option('--all-status', help='Show all certificates.', is_flag=True)
@pass_gandi
def info(gandi, resource, id, altnames, csr, cert, all_status):
    """ Display information about a certificate.

    Resource can be a CN or an ID
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
@click.option('-o', '--output', help='The file to write the cert.')
@click.option('--force', '-f', is_flag=True,
              help='Overwrite the crt file if it exists.')
@pass_gandi
def export(gandi, resource, output, force):
    """ Write the certificate to <output> or <fqdn>.crt.

    Resource can be a CN or an ID
    """
    ids = []
    for res in resource:
        ids.extend(gandi.certificate.usable_ids(res))

    if output and len(ids) > 1:
        gandi.echo('Too many certs found, you must specify which cert you '
                   'want to export')
        return

    for id_ in set(ids):
        cert = gandi.certificate.info(id_)
        if 'cert' not in cert:
            continue

        if cert['status'] != 'valid':
            gandi.echo('The certificate must be in valid status to be '
                       'exported (%s).' % id_)
            continue

        crt_filename = output or cert['cn'] + '.crt'
        if not force and os.path.exists(crt_filename):
            gandi.echo('The file %s already exists.' % crt_filename)
            continue

        crt = gandi.certificate.pretty_format_cert(cert)
        if crt:
            with open(crt_filename, 'w') as crt_file:
                crt_file.write(crt)
                gandi.echo('wrote %s' % crt_filename)

        return crt


@cli.command()
@click.option('--csr', required=False,
              help='Csr of the new certificate (filename or content).')
@click.option('--pk', '--private-key', required=False,
              help='Private key to use to generate the CSR (filename or '
              'content).')
@click.option('--cn', '--common-name', required=False,
              help='Common name to use when generating the CSR.')
@click.option('--country', required=False,
              help='The generated CSR country (C).')
@click.option('--state', required=False,
              help='The generated CSR state (ST).')
@click.option('--city', required=False,
              help='The generated CSR location (L).')
@click.option('--organisation', required=False,
              help='The generated CSR organisation (O).')
@click.option('--branch', required=False,
              help='The generated CSR branch (OU).')
@click.option('-d', '--duration', default=1,
              type=IntChoice(['1', '2', '3', '4', '5']),
              help='The certificate duration in year.')
@click.option('--package', default='cert_std_1_0_0', type=CERTIFICATE_PACKAGE,
              help='Certificate package (default=cert_std_1_0_0).')
@click.option('--altnames', required=False, multiple=True,
              help='The certificate altnames (comma separated text without '
                   'space).')
@click.option('--dcv-method', required=False, type=CERTIFICATE_DCV_METHOD,
              help='Give the DCV method to use to check domain ownership.')
@pass_gandi
def create(gandi, csr, private_key, common_name, country, state, city,
           organisation, branch, duration, package, altnames, dcv_method):
    """Create a new certificate."""
    if not (csr or common_name):
        gandi.echo('You need a CSR or a CN to create a certificate.')
        return

    csr = gandi.certificate.process_csr(common_name, csr, private_key, country,
                                        state, city, organisation, branch)
    if not csr:
        return

    result = gandi.certificate.create(csr, duration, package, altnames,
                                      dcv_method)

    return result


@cli.command()
@click.argument('resource', nargs=1, required=True)
@click.option('--csr', help='New csr for the certificate.', required=False)
@click.option('--pk', '--private-key', required=False,
              help='Private key to use to generate the CSR.')
@click.option('--c', '--country', required=False,
              help='The generated CSR country (C).')
@click.option('--st', '--state', required=False,
              help='The generated CSR state (ST).')
@click.option('--l', '--city', required=False,
              help='The generated CSR location (L).')
@click.option('--o', '--organisation', required=False,
              help='The generated CSR organisation (O).')
@click.option('--ou', '--branch', required=False,
              help='The generated CSR branch (OU).')
@click.option('--altnames', required=False, multiple=True,
              help='All the certificate altnames (comma separated text '
                   'without space).')
@click.option('--dcv-method', required=False, type=CERTIFICATE_DCV_METHOD,
              help='Give the DCV method to use to check domain ownership.')
@pass_gandi
def update(gandi, resource, csr, private_key, country, state, city,
           organisation, branch, altnames, dcv_method):
    """ Update a certificate CSR.

    Resource can be a CN or an ID
    """
    ids = gandi.certificate.usable_ids(resource)

    if len(ids) > 1:
        gandi.echo('Will not update, %s is not precise enough.' % resource)
        gandi.echo('  * cert : ' +
                   '\n  * cert : '.join([str(id_) for id_ in ids]))
        return

    id_ = ids[0]

    result = gandi.certificate.update(id_, csr, private_key, country, state,
                                      city, organisation, branch, altnames,
                                      dcv_method)

    return result


@cli.command('change-dcv')
@click.argument('resource', nargs=1, required=True)
@click.option('--dcv-method', required=True, type=CERTIFICATE_DCV_METHOD,
              help='Give the updated DCV method to use.')
@pass_gandi
def change_dcv(gandi, resource, dcv_method):
    """ Change the DCV for a running certificate operation.

    Resource can be a CN or an ID
    """
    ids = gandi.certificate.usable_ids(resource)

    if len(ids) > 1:
        gandi.echo('Will not update, %s is not precise enough.' % resource)
        gandi.echo('  * cert : ' +
                   '\n  * cert : '.join([str(id_) for id_ in ids]))
        return

    id_ = ids[0]

    opers = gandi.oper.list({'cert_id': id_})
    if not opers:
        gandi.echo('Can not find any operation for this certificate.')
        return

    oper = opers[0]
    if (oper['step'] != 'RUN'
            and oper['params']['inner_step'] != 'comodo_oper_updated'):
        gandi.echo('This certificate operation is not in the good step to '
                   'update the DCV method.')
        return

    gandi.certificate.change_dcv(oper['id'], dcv_method)
    cert = gandi.certificate.info(id_)

    csr = oper['params']['csr']
    package = cert['package']
    altnames = oper['params'].get('altnames')
    gandi.certificate.advice_dcv_method(csr, package, altnames, dcv_method)


@cli.command('resend-dcv')
@click.argument('resource', nargs=1, required=True)
@pass_gandi
def resend_dcv(gandi, resource):
    """ Resend the DCV mail.

    Resource can be a CN or an ID
    """
    ids = gandi.certificate.usable_ids(resource)

    if len(ids) > 1:
        gandi.echo('Will not update, %s is not precise enough.' % resource)
        gandi.echo('  * cert : ' +
                   '\n  * cert : '.join([str(id_) for id_ in ids]))
        return

    id_ = ids[0]

    opers = gandi.oper.list({'cert_id': id_})
    if not opers:
        gandi.echo('Can not find any operation for this certificate.')
        return

    oper = opers[0]
    if (oper['step'] != 'RUN'
            and oper['params']['inner_step'] != 'comodo_oper_updated'):
        gandi.echo('This certificate operation is not in the good step to '
                   'resend the DCV.')
        return

    if oper['params']['dcv_method'] != 'email':
        gandi.echo('This certificate operation is not in email DCV.')
        return

    gandi.certificate.resend_dcv(oper['id'])


@cli.command()
@click.argument('resource', nargs=1, required=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@pass_gandi
def delete(gandi, resource, background, force):
    """ Revoke the certificate.

    Resource can be a CN or an ID
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
