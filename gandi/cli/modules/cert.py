""" Certificate commands module. """

import os
import re
from click import UsageError
from gandi.cli.core.base import GandiModule


class Certificate(GandiModule):

    """ Module to handle CLI commands.

    $ gandi certificate change-dcv
    $ gandi certificate create
    $ gandi certificate delete
    $ gandi certificate export
    $ gandi certificate info
    $ gandi certificate list
    $ gandi certificate packages
    $ gandi certificate resend-dcv
    $ gandi certificate update
    """

    @classmethod
    def from_cn(cls, common_name):
        """ Retrieve a certificate by its common name. """
        result = [(cert['id'], [cert['cn']] + cert['altnames'])
                  for cert in cls.list({'status': ['pending', 'valid']})]

        ret = {}
        for id_, fqdns in result:
            for fqdn in fqdns:
                ret.setdefault(fqdn, []).append(id_)

        cert_id = ret.get(common_name)
        if not cert_id:
            return

        return cert_id

    @classmethod
    def usable_ids(cls, id, accept_multi=True):
        """ Retrieve id from input which can be an id or a cn."""
        try:
            qry_id = cls.from_cn(id)
            if not qry_id:
                qry_id = [int(id)]
        except Exception:
            qry_id = None

        if not qry_id or not accept_multi and len(qry_id) != 1:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id if accept_multi else qry_id[0]

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from single input."""
        return cls.usable_ids(id, False)

    @classmethod
    def package_list(cls, options=None):
        """ List possible certificate packages."""
        options = options or {}
        try:
            return cls.safe_call('cert.package.list', options)
        except UsageError as err:
            if err.code == 150020:
                return []
            raise

    @classmethod
    def list(cls, options=None):
        """ List certificates."""
        options = options or {}
        return cls.call('cert.list', options)

    @classmethod
    def info(cls, id):
        """ Display information about a certificate."""
        return cls.call('cert.info', cls.usable_id(id))

    @classmethod
    def advice_dcv_method(cls, csr, package, altnames, dcv_method):
        """ Display dcv_method information. """
        params = {'csr': csr, 'package': package, 'dcv_method': dcv_method}
        result = cls.call('cert.get_dcv_params', params)
        if dcv_method == 'dns':
            cls.echo('You have to add these records in your domain zone :')
        cls.echo('\n'.join(result['message']))

    @classmethod
    def change_dcv(cls, oper_id, dcv_method):
        """ Change dcv method."""
        cls.call('cert.change_dcv', oper_id, dcv_method)

    @classmethod
    def resend_dcv(cls, oper_id):
        """ Resend dcv. """
        cls.call('cert.resend_dcv', oper_id)

    @classmethod
    def create(cls, csr, duration, package, altnames, dcv_method):
        """ Create a new certificate. """
        params = {'csr': csr, 'package': package, 'duration': duration}
        if altnames:
            params['altnames'] = altnames
        if dcv_method:
            params['dcv_method'] = dcv_method
            if dcv_method in ('dns', 'file'):
                cls.advice_dcv_method(csr, package, altnames, dcv_method)

        try:
            result = cls.call('cert.create', params)
        except UsageError:
            params['--dry-run'] = True
            msg = '\n'.join(['%s (%s)' % (err['reason'], err['attr'])
                             for err in cls.call('cert.create', params)])
            cls.error(msg)
            raise

        return result

    @classmethod
    def update(cls, cert_id, csr, private_key, country, state, city,
               organisation, branch, altnames, dcv_method):
        """ Update a certificate. """
        cert = cls.info(cert_id)
        if cert['status'] != 'valid':
            cls.error('The certificate must be in valid status to be updated.')
            return

        common_name = cert['cn']

        csr = cls.process_csr(common_name, csr, private_key, country, state,
                              city, organisation, branch)

        if not csr:
            return

        params = {'csr': csr}
        if altnames:
            params['altnames'] = []
            for altname in altnames:
                params['altnames'].extend(altname.split(','))
        if dcv_method:
            params['dcv_method'] = dcv_method

        try:
            result = cls.call('cert.update', cert_id, params)
        except UsageError:
            params['--dry-run'] = True
            msg = cls.call('cert.update', cert_id, params)
            if msg:
                cls.error(str(msg))
            raise

        return result

    @classmethod
    def create_csr(cls, common_name, private_key=None, params=None):
        """ Create CSR. """
        params = params or []

        params = [(key, val) for key, val in params if val]
        subj = '/' + '/'.join(['='.join(value) for value in params])

        if private_key and os.path.exists(private_key):
            cmd = 'openssl req -new -key %(key)s -out %(csr)s -subj "%(subj)s"'
        else:
            private_key = common_name.replace('*.', 'wildcard.') + '.key'
            # TODO check if it exists
            cmd = ('openssl req -new -newkey rsa:2048 -nodes -out %(csr)s '
                   '-keyout %(key)s -subj "%(subj)s"')

        if private_key.endswith('.crt') or private_key.endswith('.key'):
            csr_file = re.sub('\.(crt|key)$', '.csr', private_key)
        else:
            csr_file = private_key + '.csr'

        cmd = cmd % {'csr': csr_file, 'key': private_key, 'subj': subj}
        result = cls.execute(cmd)
        if not result:
            cls.echo('CSR creation failed')
            cls.echo(cmd)
            return

        return csr_file

    @classmethod
    def process_csr(cls, common_name, csr, private_key, country, state, city,
                    organisation, branch):
        """ Create a PK and a CSR if needed."""
        if csr:
            if branch or organisation or city or state or country:
                cls.echo('Following options are only used to generate'
                         ' the CSR.')
        else:
            params = (('CN', common_name),
                      ('OU', branch),
                      ('O', organisation),
                      ('L', city),
                      ('ST', state),
                      ('C', country))
            params = [(key, val) for key, val in params if val]
            csr = cls.create_csr(common_name, private_key, params)

        if csr and os.path.exists(csr):
            csr = open(csr).read()

        return csr

    @classmethod
    def pretty_format_cert(cls, cert):
        """ Pretty display of a certificate."""
        crt = cert['cert']
        if crt:
            crt = ('-----BEGIN CERTIFICATE-----\n' +
                   '\n'.join([crt[index * 64:(index + 1) * 64]
                              for index in range(len(crt) / 64 + 1)]) +
                   '\n-----END CERTIFICATE-----')
        return crt

    @classmethod
    def delete(cls, cert_id, background=False):
        """ Delete a certificate."""
        result = cls.call('cert.delete', cert_id)

        if background:
            return result

        cls.echo("Deleting your certificate.")
        cls.display_progress(result)
        cls.echo('Your certificate %s has been deleted.' % cert_id)

        return result
