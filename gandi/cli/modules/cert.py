import os
import re
from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class Certificate(GandiModule):

    @classmethod
    def from_cn(cls, common_name):
        """ retrieve a certificate by it's common name """
        result = [(cert['id'], [cert['cn']] + cert['altnames'])
                  for cert in cls.list()]

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
        return cls.usable_ids(id, False)

    @classmethod
    def package_list(cls, options=None):
        """ list possible certificate packages """
        options = options or {}
        return cls.safe_call('cert.package.list', options)

    @classmethod
    def list(cls, options=None):
        """ list certificates """
        options = options or {}
        return cls.call('cert.list', options)

    @classmethod
    def info(cls, id):
        """display information about a certificate"""
        return cls.call('cert.info', cls.usable_id(id))

    @classmethod
    def create(cls, csr, duration, package):
        """ create a new certificate """
        params = {'csr': csr, 'package': package, 'duration': duration}

        try:
            result = cls.call('cert.create', params)
        except UsageError as err:
            raise

        return result

    @classmethod
    def create_csr(cls, common_name, private_key=None, params=None):
        params = params or []

        params = [(key, val) for key, val in params if val]
        subj = '/' + '/'.join(['='.join(value) for value in params])

        if private_key and os.path.exists(private_key):
            cmd = 'openssl req -new -key %(key)s -out %(csr)s -subj %(subj)s'
        else:
            private_key = common_name + '.key'
            # TODO check if it exists
            cmd = ('openssl req -new -newkey rsa:2048 -nodes -out %(csr)s '
                   '-keyout %(key)s -subj %(subj)s')

        if private_key.endswith('.crt') or private_key.endswith('.key'):
            csr_file = re.sub('\.(crt|key)$', '.csr', private_key)
        else:
            csr_file = private_key + '.csr'

        cmd = cmd % {'csr': csr_file, 'key': private_key, 'subj': subj}
        result = cls.shell(cmd)
        if not result:
            cls.echo('CSR creation failed')
            cls.echo(cmd)
            return

        return csr_file

    @classmethod
    def pretty_format_cert(cls, cert):
        crt = cert['cert']
        if crt:
            crt = ('-----BEGIN CERTIFICATE-----\n' +
                   '\n'.join([crt[index * 64:(index + 1) * 64]
                              for index in range(len(crt) / 64 + 1)]) +
                   '\n-----END CERTIFICATE-----')
        return crt
