from ..compat import mock, ReasonableBytesIO
from .base import CommandTestCase
from gandi.cli.commands import dns

# disable SSL requests warning for tests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


RESPONSES = {
    'https://dns.api.gandi.net/api/v5/domains': {
        'status': 200,
        'headers': 'application/json',
        'body': [{'domain_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com',  # noqa
                  'domain_records_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records',  # noqa
                  'fqdn': 'iheartcli.com'},
                 {'domain_href': 'https://dns.api.gandi.net/api/v5/domains/cli.sexy',  # noqa
                  'domain_records_href': 'https://dns.api.gandi.net/api/v5/domains/cli.sexy/records',  # noqa
                  'fqdn': 'cli.sexy'}],
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com': {
        'status': 200,
        'headers': 'application/json',
        'body': {'domain_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com',  # noqa
                 'domain_keys_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys',  # noqa
                 'domain_records_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records',  # noqa
                 'fqdn': 'iheartcli.com',
                 'zone_href': 'https://dns.api.gandi.net/api/v5/zones/397c514-e7cb-11e6-9429-00163e6dc886',  # noqa
                 'zone_records_href': 'https://dns.api.gandi.net/api/v5/zones/397c514-e7cb-11e6-9429-00163e6dc886/records',  # noqa
                 'zone_uuid': '397c514-e7cb-11e6-9429-00163e6dc886'}
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records?sort_by=rrset_name': {  # noqa
        'status': 200,
        'headers': 'application/json',
        'body': [{'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/%40/A',  # noqa
                  'rrset_name': '@',
                  'rrset_ttl': 10800,
                  'rrset_type': 'A',
                  'rrset_values': ['217.70.184.38']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/%40/MX',  # noqa
                  'rrset_name': '@',
                  'rrset_ttl': 10800,
                  'rrset_type': 'MX',
                  'rrset_values': ['50 fb.mail.gandi.net.', '10 spool.mail.gandi.net.']},  # noqa
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/blog/CNAME',  # noqa
                  'rrset_name': 'blog',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['blogs.vip.gandi.net.']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/imap/CNAME',  # noqa
                  'rrset_name': 'imap',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['access.mail.gandi.net.']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/pop/CNAME',  # noqa
                  'rrset_name': 'pop',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['access.mail.gandi.net.']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/smtp/CNAME',  # noqa
                  'rrset_name': 'smtp',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['relay.mail.gandi.net.']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/webmail/CNAME',  # noqa
                  'rrset_name': 'webmail',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['webmail.gandi.net.']},
                 {'rrset_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/www/CNAME',  # noqa
                  'rrset_name': 'www',
                  'rrset_ttl': 10800,
                  'rrset_type': 'CNAME',
                  'rrset_values': ['webredir.vip.gandi.net.']}],
    },
    'https://dns.api.gandi.net/api/v5/dns/rrtypes': {
        'status': 200,
        'headers': 'application/json',
        'body': ['A', 'AAAA', 'CAA', 'CDS', 'CNAME', 'DNAME', 'DS', 'LOC',
                 'MX', 'NS', 'PTR', 'SPF', 'SRV', 'SSHFP', 'TLSA', 'TXT',
                 'WKS'],
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records': {
        'status': 201,
        'headers': 'application/json',
        'body': {'message': 'DNS Record Created'},
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/blog/CNAME': {  # noqa
        'status': 204,
        'headers': 'application/json',
        'body': {},
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys': {
        'status': 200,
        'headers': {'content-type': 'application/json',
                    'location': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168'},  # noqa
        'body': [{'algorithm': 13,
                  'algorithm_name': 'ECDSAP256SHA256',
                  'deleted': False,
                  'ds': 'iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a',  # noqa
                  'flags': 256,
                  'fqdn': 'iheartcli.com',
                  'key_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168',  # noqa
                  'status': 'active',
                  'uuid': '3415833-2314-4a86-ba1c-c3c58608a168'},
                 {'algorithm': 13,
                  'algorithm_name': 'ECDSAP256SHA256',
                  'deleted': False,
                  'ds': 'iheartcli.com. 3600 IN DS 43819 13 2 b4e6ed591f28f4a269b9adfaedec836ea0fe63a8f7f5097108297afa5492b70',  # noqa
                  'flags': 256,
                  'fqdn': 'iheartcli.com',
                  'key_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/adaab60-bb17-40ed-a13e-88376fe28c86',  # noqa
                  'status': 'active',
                  'uuid': 'adaab60-bb17-40ed-a13e-88376fe28c86'}],
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168': {  # noqa
        'status': 200,
        'headers': 'application/json',
        'body': {'algorithm': 13,
                 'algorithm_name': 'ECDSAP256SHA256',
                 'deleted': False,
                 'ds': 'iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a',  # noqa
                 'flags': 256,
                 'fqdn': 'iheartcli.com',
                 'public_key': 'Gnhra3gcNHUL0d05Ia6F/tgBzDD/Km6c2XFZA9RAOcjk/qg9aodc79MQtsTx4/CBlTmCSRIxlXWm1yMmV3LOlw==',  # noqa
                 'fingerprint': '626168cae12c674f38958b324e10c7bb63ed74cc9d649bf04766a7c095c865787',  # noqa
                 'key_href': 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168',  # noqa
                 'status': 'active',
                 'tag': 40658,
                 'uuid': '3415833-2314-4a86-ba1c-c3c58608a168'},
    },
    'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/keys/adaab60-bb17-40ed-a13e-88376fe28c86': {  # noqa
        'status': 204,
        'headers': 'application/json',
        'body': {},
    },
}


def _mock_requests(method, url, *args, **kwargs):
    # print(method, url, args, kwargs)
    content = RESPONSES[url]['body']
    headers = RESPONSES[url]['headers']
    if kwargs.get('headers', {}).get('Accept') == 'text/plain':
        content = """\
@ 10800 IN A 217.70.184.38
@ 10800 IN MX 10 spool.mail.gandi.net.
@ 10800 IN MX 50 fb.mail.gandi.net.
@ 10800 IN SOA ns1.gandi.net. hostmaster.gandi.net. 197539823 10800 3600 604800 10800
blog 10800 IN CNAME blogs.vip.gandi.net.
imap 10800 IN CNAME access.mail.gandi.net.
pop 10800 IN CNAME access.mail.gandi.net.
smtp 10800 IN CNAME relay.mail.gandi.net.
webmail 10800 IN CNAME webmail.gandi.net.
www 10800 IN CNAME webredir.vip.gandi.net."""  # noqa
    content_hdr = kwargs.get('headers', {}).get('Content-Type')
    if method == 'PUT' and content_hdr == 'text/plain':
        content = {'message': 'DNS Record Created'}
    if method == 'PUT' and url == 'https://dns.api.gandi.net/api/v5/domains/iheartcli.com/records/blog/CNAME':  # noqa
        content = {'message': 'DNS Record Created'}
    mock_resp = mock.Mock()
    mock_resp.status_code = 200
    mock_resp.content = content
    mock_resp.headers = headers
    mock_resp.json = mock.Mock(return_value=content)
    return mock_resp


class DnsTestCase(CommandTestCase):

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_domain_list(self, mock_request):
        mock_request.side_effect = _mock_requests

        result = self.invoke_with_exceptions(dns.domain_list, [])

        wanted = """\
iheartcli.com
cli.sexy
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_list(self, mock_request):
        mock_request.side_effect = _mock_requests

        result = self.invoke_with_exceptions(dns.list, ['iheartcli.com'])

        wanted = """\
name        : @
ttl         : 10800
type        : A
values      : 217.70.184.38
----------
name        : @
ttl         : 10800
type        : MX
values      : 50 fb.mail.gandi.net., 10 spool.mail.gandi.net.
----------
name        : blog
ttl         : 10800
type        : CNAME
values      : blogs.vip.gandi.net.
----------
name        : imap
ttl         : 10800
type        : CNAME
values      : access.mail.gandi.net.
----------
name        : pop
ttl         : 10800
type        : CNAME
values      : access.mail.gandi.net.
----------
name        : smtp
ttl         : 10800
type        : CNAME
values      : relay.mail.gandi.net.
----------
name        : webmail
ttl         : 10800
type        : CNAME
values      : webmail.gandi.net.
----------
name        : www
ttl         : 10800
type        : CNAME
values      : webredir.vip.gandi.net.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_list_filter(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', '--type', 'CNAME']
        result = self.invoke_with_exceptions(dns.list, args)

        wanted = """\
----------
name        : blog
ttl         : 10800
type        : CNAME
values      : blogs.vip.gandi.net.
----------
name        : imap
ttl         : 10800
type        : CNAME
values      : access.mail.gandi.net.
----------
name        : pop
ttl         : 10800
type        : CNAME
values      : access.mail.gandi.net.
----------
name        : smtp
ttl         : 10800
type        : CNAME
values      : relay.mail.gandi.net.
----------
name        : webmail
ttl         : 10800
type        : CNAME
values      : webmail.gandi.net.
----------
name        : www
ttl         : 10800
type        : CNAME
values      : webredir.vip.gandi.net.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_list_filter_args(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'CNAME']
        result = self.invoke_with_exceptions(dns.list, args)

        wanted = """\
----------
name        : blog
ttl         : 10800
type        : CNAME
values      : blogs.vip.gandi.net.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_list_unknown(self, mock_request):
        mock_request.side_effect = _mock_requests

        result = self.invoke_with_exceptions(dns.list, ['example.com'])

        wanted = """\
Sorry domain example.com does not exist
Please use one of the following: iheartcli.com, cli.sexy
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_list_text(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', '--text']
        result = self.invoke_with_exceptions(dns.list, args)

        wanted = """\
@ 10800 IN A 217.70.184.38
@ 10800 IN MX 10 spool.mail.gandi.net.
@ 10800 IN MX 50 fb.mail.gandi.net.
@ 10800 IN SOA ns1.gandi.net. hostmaster.gandi.net. 197539823 10800 3600 604800 10800
blog 10800 IN CNAME blogs.vip.gandi.net.
imap 10800 IN CNAME access.mail.gandi.net.
pop 10800 IN CNAME access.mail.gandi.net.
smtp 10800 IN CNAME relay.mail.gandi.net.
webmail 10800 IN CNAME webmail.gandi.net.
www 10800 IN CNAME webredir.vip.gandi.net.
"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_create(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'cname', 'blog.cli.sexy']
        result = self.invoke_with_exceptions(dns.create, args)

        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_missing(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com']
        result = self.invoke_with_exceptions(dns.update, args)

        wanted = """Cannot find parameters for zone content to update.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_unknown(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['example.com']
        result = self.invoke_with_exceptions(dns.update, args)

        wanted = """\
Sorry domain example.com does not exist
Please use one of the following: iheartcli.com, cli.sexy
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_argument_ok(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', '--file', 'sandbox/example.txt']

        content = """\
blog 10800 IN CNAME blogs.vip.gandi.net.
"""
        result = self.isolated_invoke_with_exceptions(dns.update, args,
                                                      temp_content=content)
        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_parameters_ok(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'cname', 'blog.cli.sexy']

        result = self.invoke_with_exceptions(dns.update, args)
        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_parameters_ko(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'cname']

        result = self.invoke_with_exceptions(dns.update, args)
        wanted = """You must provide one or more value parameter.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_update_pipe_ok(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com']

        content = b"""\
blog 10800 IN CNAME blogs.vip.gandi.net.
"""
        result = self.invoke_with_exceptions(dns.update, args,
                                             input=ReasonableBytesIO(content))
        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_create_multiple(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'cname', 'blog.cli.sexy',
                'glop.cli.sexy']
        result = self.invoke_with_exceptions(dns.create, args)

        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_create_type_case(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'CNAME', 'blog.cli.sexy']
        result = self.invoke_with_exceptions(dns.create, args)

        wanted = """DNS Record Created
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_create_unknown(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['example.com', 'blog', 'CNAME', 'blog.cli.sexy']
        result = self.invoke_with_exceptions(dns.create, args)

        wanted = """\
Sorry domain example.com does not exist
Please use one of the following: iheartcli.com, cli.sexy
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_delete(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'CNAME', '-f']
        result = self.invoke_with_exceptions(dns.delete, args)

        wanted = """Delete successful.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_delete_unknown(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['example.com', 'blog', 'CNAME', '-f']
        result = self.invoke_with_exceptions(dns.delete, args)

        wanted = """\
Sorry domain example.com does not exist
Please use one of the following: iheartcli.com, cli.sexy
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_delete_all(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com']
        result = self.invoke_with_exceptions(dns.delete, args, input='\n')

        wanted = """\
Are you sure to delete all records for domain iheartcli.com ? [y/N]: \n"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_delete_name(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog']
        result = self.invoke_with_exceptions(dns.delete, args, input='\n')

        wanted = """\
Are you sure to delete all 'blog' name records for domain iheartcli.com ? [y/N]: \n"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_delete_prompt(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'blog', 'CNAME']
        result = self.invoke_with_exceptions(dns.delete, args, input='\n')

        wanted = """\
Are you sure to delete all 'blog' records of type CNAME for domain iheartcli.com ? [y/N]: \n"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_list(self, mock_request):
        mock_request.side_effect = _mock_requests

        result = self.invoke_with_exceptions(dns.keys_list, ['iheartcli.com'])
        wanted = """\
uuid           : 3415833-2314-4a86-ba1c-c3c58608a168
algorithm      : 13
algorithm_name : ECDSAP256SHA256
ds             : iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a
flags          : 256
status         : active
----------
uuid           : adaab60-bb17-40ed-a13e-88376fe28c86
algorithm      : 13
algorithm_name : ECDSAP256SHA256
ds             : iheartcli.com. 3600 IN DS 43819 13 2 b4e6ed591f28f4a269b9adfaedec836ea0fe63a8f7f5097108297afa5492b70
flags          : 256
status         : active
"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_info(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', '3415833-2314-4a86-ba1c-c3c58608a168']
        result = self.invoke_with_exceptions(dns.keys_info, args)
        wanted = """\
uuid           : 3415833-2314-4a86-ba1c-c3c58608a168
algorithm      : 13
algorithm_name : ECDSAP256SHA256
ds             : iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a
fingerprint    : 626168cae12c674f38958b324e10c7bb63ed74cc9d649bf04766a7c095c865787
public_key     : Gnhra3gcNHUL0d05Ia6F/tgBzDD/Km6c2XFZA9RAOcjk/qg9aodc79MQtsTx4/CBlTmCSRIxlXWm1yMmV3LOlw==
flags          : 256
tag            : 40658
status         : active
"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_create(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', '256']
        result = self.invoke_with_exceptions(dns.keys_create, args)
        wanted = """\
uuid           : 3415833-2314-4a86-ba1c-c3c58608a168
algorithm      : 13
algorithm_name : ECDSAP256SHA256
ds             : iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a
fingerprint    : 626168cae12c674f38958b324e10c7bb63ed74cc9d649bf04766a7c095c865787
public_key     : Gnhra3gcNHUL0d05Ia6F/tgBzDD/Km6c2XFZA9RAOcjk/qg9aodc79MQtsTx4/CBlTmCSRIxlXWm1yMmV3LOlw==
flags          : 256
tag            : 40658
status         : active
"""  # noqa
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_delete_ok(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'adaab60-bb17-40ed-a13e-88376fe28c86', '-f']
        result = self.invoke_with_exceptions(dns.keys_delete, args)
        wanted = """Delete successful.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_delete_prompt(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'adaab60-bb17-40ed-a13e-88376fe28c86']
        result = self.invoke_with_exceptions(dns.keys_delete, args, input='\n')
        wanted = """\
Are you sure you want to delete key adaab60-bb17-40ed-a13e-88376fe28c86 on \
domain iheartcli.com? [y/N]: \n"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_dns_keys_recover(self, mock_request):
        mock_request.side_effect = _mock_requests
        args = ['iheartcli.com', 'adaab60-bb17-40ed-a13e-88376fe28c86']
        result = self.invoke_with_exceptions(dns.keys_recover, args)
        wanted = """Recover successful.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)
