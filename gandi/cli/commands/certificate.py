""" Certificate namespace commands. """

import os
import click
import requests

# define basestring for python3
try:
    basestring
except NameError:
    basestring = (str, bytes)

type_list = list

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_cert, output_cert_oper, display_rows
from gandi.cli.core.params import (pass_gandi, IntChoice,
                                   CERTIFICATE_PACKAGE, CERTIFICATE_DCV_METHOD,
                                   CERTIFICATE_PACKAGE_TYPE,
                                   CERTIFICATE_PACKAGE_MAX,
                                   CERTIFICATE_PACKAGE_WARRANTY)


@cli.command()
@pass_gandi
def packages(gandi):
    """ List certificate packages.
    /!\\ deprecated call.
    """
    gandi.echo('/!\ "gandi certificate packages" is deprecated.')
    gandi.echo('Please use "gandi certificate plans".')
    return _plans(gandi, with_name=True)


@cli.command()
@pass_gandi
def plans(gandi):
    """ List certificate plans. """
    return _plans(gandi)


def package_desc(gandi, package):
    if isinstance(package, basestring):
        package = gandi.certificate.package_get(package)
        if not package:
            return ''

    type_ = package['category']['name']
    if package['wildcard']:
        desc = '%s wildcard' % type_
    elif package['max_domains'] > 1:
        desc = '%s multi domain' % type_
    else:
        desc = '%s single domain' % type_
    return ' '.join([word.capitalize() for word in desc.split(' ')])


def _plans(gandi, with_name=False):
    packages = gandi.certificate.package_list()

    def keyfunc(item):
        return (item['category']['id'],
                item['max_domains'],
                item['warranty'],
                item['name'])

    packages.sort(key=keyfunc)
    labels = ['Description', 'Max altnames', 'Type']
    if with_name:
        labels.insert(1, 'Name')
    else:
        labels.append('Warranty')
    ret = [labels]

    for package in packages:
        params = package['name'].split('_')
        cat = package['name'].split('_')[1]
        warranty = str(int(package['name'].split('_')[3]) * 1000)
        if len(warranty) > 3:
            warranty = type_list(warranty)
            warranty.insert(len(warranty) - 3, ',')
            warranty = ''.join(warranty)

        desc = package_desc(gandi, package)
        line = [desc, str(package['max_domains']), cat]
        if with_name:
            line.insert(1, package['name'])
        else:
            line.append(warranty)
        ret.append(line)

    display_rows(gandi, ret)

    return ret


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

    output_keys = ['cn', 'plan']

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
    for num, cert in enumerate(result):
        if num:
            gandi.separator_line()
        cert['plan'] = package_desc(gandi, cert['package'])
        output_cert(gandi, cert, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
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
    output_keys = ['cn', 'date_created', 'date_end', 'plan', 'status']

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
    for num, id_ in enumerate(set(ids)):
        cert = gandi.certificate.info(id_)
        if not all_status and cert['status'] not in ['valid', 'pending']:
            continue
        if num:
            gandi.separator_line()
        cert['plan'] = package_desc(gandi, cert['package'])
        output_cert(gandi, cert, output_keys)
        result.append(cert)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('-o', '--output', help='The file to write the cert.')
@click.option('--force', '-f', is_flag=True,
              help='Overwrite the crt file if it exists.')
@click.option('-i', '--intermediate', is_flag=True,
              help='Retrieve gandi intermediate certs.')
@pass_gandi
def export(gandi, resource, output, force, intermediate):
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

        cert_filename = cert['cn'].replace('*.', 'wildcard.', 1)
        crt_filename = output or cert_filename + '.crt'
        if not force and os.path.isfile(crt_filename):
            gandi.echo('The file %s already exists.' % crt_filename)
            continue

        crt = gandi.certificate.pretty_format_cert(cert)
        if crt:
            with open(crt_filename, 'w') as crt_file:
                crt_file.write(crt)
                gandi.echo('wrote %s' % crt_filename)

        package = cert['package']
        if 'bus' in package and intermediate:
            gandi.echo('Business certs do not need intermediates.')
        elif intermediate:
            crtf = 'pem'
            sha_version = cert['sha_version']
            type_ = package.split('_')[1]
            extra = ('sgc' if 'SGC' in package
                     and 'pro' in package
                     and sha_version == 1 else 'default')

            if extra == 'sgc':
                crtf = 'pem'

            inters = gandi.certificate.urls[sha_version][type_][extra][crtf]
            if isinstance(inters, basestring):
                inters = [inters]

            fhandle = open(cert_filename + '.inter.crt', 'w+b')
            for inter in inters:
                if inter.startswith('http'):
                    data = requests.get(inter).text
                else:
                    data = inter
                fhandle.write(data.encode('latin1'))

            gandi.echo('wrote %s' % cert_filename + '.inter.crt')
            fhandle.close()

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
              type=IntChoice(['1', '2']),
              help='The certificate duration in year.')
@click.option('--package', type=CERTIFICATE_PACKAGE,
              help='Certificate package.')
@click.option('--type', type=CERTIFICATE_PACKAGE_TYPE,
              help='Certificate package type (default=std).')
@click.option('--max-altname', type=CERTIFICATE_PACKAGE_MAX,
              help='Certificate package max altname number.')
@click.option('--warranty', type=CERTIFICATE_PACKAGE_WARRANTY,
              help='Certificate warranty, only good for pro certificates.')
@click.option('--altnames', required=False, multiple=True,
              help='The certificate altnames (comma separated text without '
                   'space).')
@click.option('--dcv-method', required=False, type=CERTIFICATE_DCV_METHOD,
              help='Give the DCV method to use to check domain ownership.')
@pass_gandi
def create(gandi, csr, private_key, common_name, country, state, city,
           organisation, branch, duration, package, type, max_altname,
           warranty, altnames, dcv_method):
    """Create a new certificate."""
    if not (csr or common_name):
        gandi.echo('You need a CSR or a CN to create a certificate.')
        return

    if package and (type or max_altname or warranty):
        gandi.echo('Please do not use --package at the same time you use '
                   '--type, --max-altname or --warranty.')
        return

    if type and warranty and type != 'pro':
        gandi.echo('The warranty can only be specified for pro certificates.')
        return

    csr = gandi.certificate.process_csr(common_name, csr, private_key, country,
                                        state, city, organisation, branch)
    if not csr:
        return

    if not common_name:
        common_name = gandi.certificate.get_common_name(csr)
        if not common_name:
            gandi.echo('Unable to parse provided csr: %s' % csr)
            return

    if '*' in common_name and altnames and len(altnames) > 1:
        gandi.echo("You can't have a wildcard with multidomain certificate.")
        return

    if package:
        gandi.echo('/!\ Using --package is deprecated, please replace it by '
                   '--type (in std, pro or bus) and --max-altname to set '
                   'the max number of altnames.')
    elif type or max_altname or warranty:
        package = gandi.certificate.get_package(common_name,
                                                type,
                                                max_altname,
                                                altnames,
                                                warranty)
        if not package:
            gandi.echo("Can't find any plan with your params.")
            gandi.echo('Please call : "gandi certificate plans".')
            return

    result = gandi.certificate.create(csr, duration, package, altnames,
                                      dcv_method)

    gandi.echo('The certificate create operation is %s' % result['id'])
    gandi.echo('You can follow it with:')
    gandi.echo('$ gandi certificate follow %s' % result['id'])
    if common_name:
        gandi.echo('When the operation is DONE, you can retrieve the .crt'
                   ' with:')
        gandi.echo('$ gandi certificate export "%s"' % common_name)

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

    gandi.echo('The certificate update operation is %s' % result['id'])
    gandi.echo('You can follow it with:')
    gandi.echo('$ gandi certificate follow %s' % result['id'])
    gandi.echo('When the operation is DONE, you can retrieve the .crt'
               ' with:')
    gandi.echo('$ gandi certificate export "%s"' % resource)

    return result


@cli.command()
@click.argument('resource', nargs=1, required=True)
@pass_gandi
def follow(gandi, resource):
    """ Get the operation status

    Resource is an operation ID
    """
    oper = gandi.oper.info(int(resource))
    assert(oper['type'].startswith('certificate_'))
    output_cert_oper(gandi, oper)
    return oper


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
