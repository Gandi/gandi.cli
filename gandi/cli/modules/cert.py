""" Certificate commands module. """

import os
import re
from click import UsageError
from gandi.cli.core.base import GandiModule


CROSSED_PEM = '''-----BEGIN CERTIFICATE-----
MIIFdzCCBF+gAwIBAgIQE+oocFv07O0MNmMJgGFDNjANBgkqhkiG9w0BAQwFADBv
MQswCQYDVQQGEwJTRTEUMBIGA1UEChMLQWRkVHJ1c3QgQUIxJjAkBgNVBAsTHUFk
ZFRydXN0IEV4dGVybmFsIFRUUCBOZXR3b3JrMSIwIAYDVQQDExlBZGRUcnVzdCBF
eHRlcm5hbCBDQSBSb290MB4XDTAwMDUzMDEwNDgzOFoXDTIwMDUzMDEwNDgzOFow
gYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpOZXcgSmVyc2V5MRQwEgYDVQQHEwtK
ZXJzZXkgQ2l0eTEeMBwGA1UEChMVVGhlIFVTRVJUUlVTVCBOZXR3b3JrMS4wLAYD
VQQDEyVVU0VSVHJ1c3QgUlNBIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAgBJlFzYOw9sIs9CsVw127c0n00yt
UINh4qogTQktZAnczomfzD2p7PbPwdzx07HWezcoEStH2jnGvDoZtF+mvX2do2NC
tnbyqTsrkfjib9DsFiCQCT7i6HTJGLSR1GJk23+jBvGIGGqQIjy8/hPwhxR79uQf
jtTkUcYRZ0YIUcuGFFQ/vDP+fmyc/xadGL1RjjWmp2bIcmfbIWax1Jt4A8BQOujM
8Ny8nkz+rwWWNR9XWrf/zvk9tyy29lTdyOcSOk2uTIq3XJq0tyA9yn8iNK5+O2hm
AUTnAU5GU5szYPeUvlM3kHND8zLDU+/bqv50TmnHa4xgk97Exwzf4TKuzJM7UXiV
Z4vuPVb+DNBpDxsP8yUmazNt925H+nND5X4OpWaxKXwyhGNVicQNwZNUMBkTrNN9
N6frXTpsNVzbQdcS2qlJC9/YgIoJk2KOtWbPJYjNhLixP6Q5D9kCnusSTJV882sF
qV4Wg8y4Z+LoE53MW4LTTLPtW//e5XOsIzstAL81VXQJSdhJWBp/kjbmUZIO8yZ9
HE0XvMnsQybQv0FfQKlERPSZ51eHnlAfV1SoPv10Yy+xUGUJ5lhCLkMaTLTwJUdZ
+gQek9QmRkpQgbLevni3/GcV4clXhB4PY9bpYrrWX1Uu6lzGKAgEJTm4Diup8kyX
HAc/DVL17e8vgg8CAwEAAaOB9DCB8TAfBgNVHSMEGDAWgBStvZh6NLQm9/rEJlTv
A73gJMtUGjAdBgNVHQ4EFgQUU3m/WqorSs9UgOHYm8Cd8rIDZsswDgYDVR0PAQH/
BAQDAgGGMA8GA1UdEwEB/wQFMAMBAf8wEQYDVR0gBAowCDAGBgRVHSAAMEQGA1Ud
HwQ9MDswOaA3oDWGM2h0dHA6Ly9jcmwudXNlcnRydXN0LmNvbS9BZGRUcnVzdEV4
dGVybmFsQ0FSb290LmNybDA1BggrBgEFBQcBAQQpMCcwJQYIKwYBBQUHMAGGGWh0
dHA6Ly9vY3NwLnVzZXJ0cnVzdC5jb20wDQYJKoZIhvcNAQEMBQADggEBAJNl9jeD
lQ9ew4IcH9Z35zyKwKoJ8OkLJvHgwmp1ocd5yblSYMgpEg7wrQPWCcR23+WmgZWn
RtqCV6mVksW2jwMibDN3wXsyF24HzloUQToFJBv2FAY7qCUkDrvMKnXduXBBP3zQ
YzYhBx9G/2CkkeFnvN4ffhkUyWNnkepnB2u0j4vAbkN9w6GAbLIevFOFfdyQoaS8
Le9Gclc1Bb+7RrtubTeZtv8jkpHGbkD4jylW6l/VXxRTrPBPYer3IsynVgviuDQf
Jtl7GQVoP7o81DgGotPmjw7jtHFtQELFhLRAlSv0ZaBIefYdgWOWnU914Ph85I6p
0fKtirOMxyHNwu8=
-----END CERTIFICATE-----'''


URLS = {
    1: {
        'std': {
            'default': {
                'der': 'http://crt.gandi.net/GandiStandardSSLCA.crt',
                'pem':
                    'http://www.gandi.net/static/CAs/GandiStandardSSLCA.pem',
            },
        },
        'pro': {
            'sgc': {
                'pem':
                    'http://www.gandi.net/static/CAs/GandiSGCSSLCA.pem',
            },
            'default': {
                'der': 'http://crt.gandi.net/GandiProSSLCA.crt',
                'pem':
                    'http://www.gandi.net/static/CAs/GandiProSSLCA.pem',
            },
        },
    },
    2: {
        'std': {
            'default': {
                'der': ['http://crt.gandi.net/GandiStandardSSLCA2.crt',
                        'http://crt.usertrust.com/USERTrustRSAAddTrustCA.crt'],
                'pem': [
                    'http://www.gandi.net/static/CAs/GandiStandardSSLCA2.pem'],

            },
        },
        'pro': {
            'default': {
                'der': ['http://crt.gandi.net/GandiProSSLCA2.crt',
                        'http://crt.usertrust.com/USERTrustRSAAddTrustCA.crt'],
                'pem': ['http://www.gandi.net/static/CAs/GandiProSSLCA2.pem',
                        CROSSED_PEM],
            },
        },
    },
}


class Certificate(GandiModule):
    urls = URLS

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
    def get_latest_valid(cls, hosts):
        """ Retrieve valid certificates by fqdn. """
        certs = cls.list({'status': 'valid', 'items_per_page': 500})
        possible = None

        if not isinstance(hosts, (tuple, list)):
            hosts = [hosts]

        for cert in certs:
            cert_hosts = set([cert['cn']] + cert['altnames'])
            if len(set(hosts) - cert_hosts) == 0:
                if (possible and possible['date_end'] < cert['date_end']
                        or not possible):
                        possible = cert

        return possible

    @classmethod
    def from_cn(cls, common_name):
        """ Retrieve a certificate by its common name. """
        # search with cn
        result_cn = [(cert['id'], [cert['cn']] + cert['altnames'])
                     for cert in cls.list({'status': ['pending', 'valid'],
                                           'items_per_page': 500,
                                           'cn': common_name})]
        # search with altname
        result_alt = [(cert['id'], [cert['cn']] + cert['altnames'])
                      for cert in cls.list({'status': ['pending', 'valid'],
                                            'items_per_page': 500,
                                            'altname': common_name})]

        result = result_cn + result_alt
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
            qry_id = [int(id)]
        except ValueError:
            try:
                qry_id = cls.from_cn(id)
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

    __packages__ = None

    @classmethod
    def package_get(cls, package_name):
        if not cls.__packages__:
            cls.__packages__ = dict([(pkg['name'], pkg)
                                     for pkg in cls.package_list()])

        return cls.__packages__.get(package_name)

    @classmethod
    def list(cls, options=None):
        """ List certificates."""
        options = options or {}
        return cls.call('cert.list', options)

    @classmethod
    def info(cls, id):
        """ Display information about a certificate."""
        return cls.call('cert.info', id)

    @classmethod
    def get_package(cls, common_name, type='std', max_altname=None,
                    altnames=None, warranty=None):
        type = type or 'std'

        if max_altname:
            if max_altname < len(altnames):
                cls.echo('You choose --max-altname %s but you have more '
                         'altnames (%s)' % (max_altname, len(altnames)))
                return
        else:
            if '*' in common_name:
                max_altname = 'w'
            elif not altnames:
                max_altname = 1
            else:
                for max_ in [1, 3, 5, 10, 20]:
                    if len(altnames) < max_:
                        max_altname = max_
                        break

                if not max_altname:
                    cls.echo('Too many altnames, max is 20.')
                    return

        pack_filter = 'cert_%s_%s_' % (type, max_altname)
        if warranty:
            pack_filter += '%s_' % (warranty)

        packages = [item['name']
                    for item in cls.package_list()
                    if item['name'].startswith(pack_filter)]

        return packages[0] if packages else None

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
    def create(cls, csr, duration, package, altnames=None, dcv_method=None):
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

    @staticmethod
    def private_key(common_name):
        return common_name.replace('*.', 'wildcard.') + '.key'

    @classmethod
    def gen_pk(cls, common_name, private_key):
        if private_key:
            cmd = 'openssl req -new -key %(key)s -out %(csr)s -subj "%(subj)s"'
            if not os.path.exists(private_key):
                content = private_key
                private_key = cls.private_key(common_name)
                with open(private_key, 'w') as fhandle:
                    fhandle.write(content)
        else:
            private_key = cls.private_key(common_name)
            # TODO check if it exists
            cmd = ('openssl req -new -newkey rsa:2048 -sha256 -nodes '
                   '-out %(csr)s -keyout %(key)s -subj "%(subj)s"')
        return cmd, private_key

    @classmethod
    def create_csr(cls, common_name, private_key=None, params=None):
        """ Create CSR. """
        params = params or []

        params = [(key, val) for key, val in params if val]
        subj = '/' + '/'.join(['='.join(value) for value in params])

        cmd, private_key = cls.gen_pk(common_name, private_key)

        if private_key.endswith('.crt') or private_key.endswith('.key'):
            csr_file = re.sub(r'\.(crt|key)$', '.csr', private_key)
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
    def get_common_name(cls, csr):
        """ Read information from CSR. """
        from tempfile import NamedTemporaryFile
        fhandle = NamedTemporaryFile()
        fhandle.write(csr.encode('latin1'))
        fhandle.flush()
        output = cls.exec_output('openssl req -noout -subject -in %s' %
                                 fhandle.name)
        if not output:
            return

        common_name = output.split('=')[-1].strip()
        fhandle.close()
        return common_name

    @classmethod
    def process_csr(cls, common_name, csr=None, private_key=None,
                    country=None, state=None, city=None, organisation=None,
                    branch=None):
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
            with open(csr) as fcsr:
                csr = fcsr.read()

        return csr

    @classmethod
    def pretty_format_cert(cls, cert):
        """ Pretty display of a certificate."""
        crt = cert.get('cert')
        if crt:
            crt = ('-----BEGIN CERTIFICATE-----\n' +
                   '\n'.join([crt[index * 64:(index + 1) * 64]
                              for index in range(int(len(crt) / 64) + 1)]).rstrip('\n') +  # noqa
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
