""" Virtual hosts namespace commands. """

import click
import os

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_vhost
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--names', help='Display names.', is_flag=True)
@pass_gandi
def list(gandi, limit, id, names):
    """ List vhosts. """
    options = {
        'items_per_page': limit,
    }

    output_keys = ['name', 'state', 'date_creation']
    if id:
        # When we will have more than paas vhost, we will append rproxy_id
        output_keys.append('paas_id')

    paas_names = {}
    if names:
        output_keys.append('paas_name')
        paas_names = gandi.paas.list_names()

    result = gandi.vhost.list(options)
    for num, vhost in enumerate(result):
        paas = paas_names.get(vhost['paas_id'])
        if num:
            gandi.separator_line()
        output_vhost(gandi, vhost, paas, output_keys)

    return result


@cli.command()
@click.option('--id', help='Display ids.', is_flag=True)
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def info(gandi, resource, id):
    """ Display information about a vhost.

    Resource must be the vhost fqdn.
    """
    output_keys = ['name', 'state', 'date_creation', 'paas_name', 'ssl']

    if id:
        # When we will have more than paas vhost, we will append rproxy_id
        output_keys.append('paas_id')

    paas_names = gandi.paas.list_names()

    ret = []
    paas = None
    for num, item in enumerate(resource):
        vhost = gandi.vhost.info(item)
        try:
            hostedcert = gandi.hostedcert.infos(vhost['name'])
            vhost['ssl'] = 'activated' if hostedcert else 'disabled'
        except ValueError:
            vhost['ssl'] = 'disabled'
        paas = paas_names.get(vhost['paas_id'])
        if num:
            gandi.separator_line()
        ret.append(output_vhost(gandi, vhost, paas, output_keys))

    return ret


def activate_ssl(gandi, vhost, ssl, private_key, poll_cert):
    if ssl:
        try:
            hostedcert = gandi.hostedcert.infos(vhost)
        except ValueError:
            cert = gandi.certificate.get_latest_valid(vhost)
            if cert:
                if not private_key:
                    gandi.echo('Please give the private key for certificate '
                               + 'id %s (CN: %s)' % (cert['id'], cert['cn']))
                    return False

                if os.path.isfile(private_key):
                    with open(private_key) as fhandle:
                        private_key = fhandle.read()

                crt = gandi.certificate.pretty_format_cert(cert)
                gandi.hostedcert.create(private_key, crt)
            elif poll_cert:
                gandi.echo('This operation will take a long time waiting '
                           'for the certificate to be generated.')

                # create the certificate
                csr = gandi.certificate.process_csr(common_name,
                                                    private_key=private_key)
                package = gandi.certificate.get_package(vhost)
                oper = gandi.certificate.create(csr, 1, package)

                gandi.echo('If the term close, you can check the create '
                           'operation with :')
                gandi.echo('$ gandi certificate follow %s' % oper['id'])
                gandi.echo("And when it's DONE you can continue doing :")
                gandi.echo('$ gandi vhost update %s --ssl --private-key %s' %
                           (vhost, vhost.replace('*.', 'wildcard.') + '.key'))
            else:
                gandi.echo('There is no certificate for %s.' % vhost)
                gandi.echo('Create the certificate with (for exemple) :')
                gandi.echo('$ gandi certificate create --cn %s --type std' %
                           vhost)
                gandi.echo('Then update the vhost to activate ssl with :')
                gandi.echo('$ gandi vhost udpate %s --ssl' % vhost)
                ssl = False
    return True


@cli.command()
@click.option('--vhost', help='Vhost fqdn.', required=True)
@click.option('--paas', required=True,
              help='PaaS instance on which to create it.')
@click.option('--ssl', help='Get ssl on that vhost.', is_flag=True)
@click.option('--pk', '--private-key',
              help='Private key used to generate the ssl Certificate.')
@click.option('--alter-zone', help='Will update the domain zone.',
              is_flag=True)
@click.option('--poll-cert', help='Will wait for the certificate creation.',
              is_flag=True)
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='Continue the process whatever append.')
@pass_gandi
def create(gandi, vhost, paas, ssl, private_key, alter_zone, poll_cert,
           background, force):
    """ Create a new vhost. """
    if not activate_ssl(gandi, vhost, ssl, private_key, poll_cert):
        return

    paas_info = gandi.paas.info(paas)
    result = gandi.vhost.create(paas_info, vhost, alter_zone, background)

    if not result:
        return

    if background:
        gandi.pretty_echo(result)

    return result


@cli.command()
@click.option('--ssl', help='Get ssl on that vhost.', is_flag=True)
@click.option('--pk', '--private-key',
              help='Private key used to generate the ssl Certificate.')
@click.option('--poll-cert', help='Will wait for the certificate creation.',
              is_flag=True)
@click.argument('resource', nargs=1, required=True)
@pass_gandi
def update(gandi, resource, ssl, private_key, poll_cert):
    """ Update a vhost.

    Right now you can only activate ssl on the vhost.
    """
    activate_ssl(gandi, resource, ssl, private_key, poll_cert)


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.argument('resource', required=True)
@pass_gandi
def delete(gandi, resource, force, background):
    """ Delete a vhost. """
    output_keys = ['name', 'paas_id', 'state', 'date_creation']
    if not force:
        proceed = click.confirm('Are you sure to delete vhost %s?' %
                                resource)

        if not proceed:
            return

    opers = gandi.vhost.delete(resource, background)
    if background:
        for oper in opers:
            output_generic(gandi, oper, output_keys)

    return opers
