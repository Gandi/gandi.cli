# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import record


class RecordTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(record.list, ['iheartcli.com'])

        self.assertEqual(result.output, """\
name        : *
type        : A
value       : 73.246.104.110
ttl         : 10800
----------
name        : @
type        : A
value       : 73.246.104.110
ttl         : 10800
----------
name        : much
type        : A
value       : 192.243.24.132
ttl         : 10800
----------
name        : blog
type        : CNAME
value       : blogs.vip.gandi.net.
ttl         : 10800
----------
name        : cloud
type        : CNAME
value       : gpaas6.dc0.gandi.net.
ttl         : 10800
----------
name        : imap
type        : CNAME
value       : access.mail.gandi.net.
ttl         : 10800
----------
name        : pop
type        : CNAME
value       : access.mail.gandi.net.
ttl         : 10800
----------
name        : smtp
type        : CNAME
value       : relay.mail.gandi.net.
ttl         : 10800
----------
name        : webmail
type        : CNAME
value       : agent.mail.gandi.net.
ttl         : 10800
----------
name        : @
type        : MX
value       : 50 fb.mail.gandi.net.
ttl         : 10800
----------
name        : @
type        : MX
value       : 10 spool.mail.gandi.net.
ttl         : 10800
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_format_text(self):
        args = ['iheartcli.com', '--format', 'text']
        result = self.invoke_with_exceptions(record.list, args)

        self.assertEqual(result.output, """\
* 10800 IN A 73.246.104.110
@ 10800 IN A 73.246.104.110
much 10800 IN A 192.243.24.132
blog 10800 IN CNAME blogs.vip.gandi.net.
cloud 10800 IN CNAME gpaas6.dc0.gandi.net.
imap 10800 IN CNAME access.mail.gandi.net.
pop 10800 IN CNAME access.mail.gandi.net.
smtp 10800 IN CNAME relay.mail.gandi.net.
webmail 10800 IN CNAME agent.mail.gandi.net.
@ 10800 IN MX 50 fb.mail.gandi.net.
@ 10800 IN MX 10 spool.mail.gandi.net.
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_format_json(self):
        args = ['iheartcli.com', '--format', 'json']
        result = self.invoke_with_exceptions(record.list, args)

        self.assertEqual(result.output, """\
[
    {
        "id": 337085079,
        "name": "*",
        "ttl": 10800,
        "type": "A",
        "value": "73.246.104.110"
    },
    {
        "id": 337085078,
        "name": "@",
        "ttl": 10800,
        "type": "A",
        "value": "73.246.104.110"
    },
    {
        "id": 337085081,
        "name": "much",
        "ttl": 10800,
        "type": "A",
        "value": "192.243.24.132"
    },
    {
        "id": 337085072,
        "name": "blog",
        "ttl": 10800,
        "type": "CNAME",
        "value": "blogs.vip.gandi.net."
    },
    {
        "id": 337085082,
        "name": "cloud",
        "ttl": 10800,
        "type": "CNAME",
        "value": "gpaas6.dc0.gandi.net."
    },
    {
        "id": 337085075,
        "name": "imap",
        "ttl": 10800,
        "type": "CNAME",
        "value": "access.mail.gandi.net."
    },
    {
        "id": 337085071,
        "name": "pop",
        "ttl": 10800,
        "type": "CNAME",
        "value": "access.mail.gandi.net."
    },
    {
        "id": 337085074,
        "name": "smtp",
        "ttl": 10800,
        "type": "CNAME",
        "value": "relay.mail.gandi.net."
    },
    {
        "id": 337085073,
        "name": "webmail",
        "ttl": 10800,
        "type": "CNAME",
        "value": "agent.mail.gandi.net."
    },
    {
        "id": 337085077,
        "name": "@",
        "ttl": 10800,
        "type": "MX",
        "value": "50 fb.mail.gandi.net."
    },
    {
        "id": 337085076,
        "name": "@",
        "ttl": 10800,
        "type": "MX",
        "value": "10 spool.mail.gandi.net."
    }
]
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_no_zone(self):

        result = self.invoke_with_exceptions(record.list, ['cli.sexy'])

        self.assertEqual(result.output, """\
No zone records found, domain cli.sexy doesn't seems to be managed at Gandi.
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_output(self):

        args = ['iheartcli.com', '--output']

        with mock.patch('gandi.cli.commands.record.open',
                        create=True) as mock_open:
            mock_open.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(record.list, args)

        self.assertEqual(result.output, """\
Your zone file have been writen in iheartcli.com_424242
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_output_reset(self):

        args = ['iheartcli.com', '--output']

        with mock.patch('gandi.cli.commands.record.os.path.isfile',
                        create=True) as mock_isfile:
            mock_isfile.return_value = mock.MagicMock()

            with mock.patch('gandi.cli.commands.record.open',
                            create=True) as mock_open:
                mock_open.return_value = mock.MagicMock()

                result = self.invoke_with_exceptions(record.list, args)

        self.assertEqual(result.output, """\
Your zone file have been writen in iheartcli.com_424242
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_no_zone(self):
        args = ['cli.sexy', '--name', '@', '--type', 'A',
                '--value', '127.0.0.1']
        result = self.invoke_with_exceptions(record.create, args)

        self.assertEqual(result.output, """\
No zone records found, domain cli.sexy doesn't seems to be managed at Gandi.
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['iheartcli.com', '--name', '@', '--type', 'A', '--ttl', 3600,
                '--value', '127.0.0.1']
        result = self.invoke_with_exceptions(record.create, args)

        self.assertEqual(result.output, """\
Creating new zone version
Updating zone version
Activation of new zone version
""")
        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.zone.record.add'][0][2]
        self.assertEqual(params['name'], '@')
        self.assertEqual(params['type'], 'A')
        self.assertEqual(params['value'], '127.0.0.1')
        self.assertEqual(params['ttl'], 3600)

    def test_delete_no_zone(self):
        args = ['cli.sexy']
        result = self.invoke_with_exceptions(record.delete, args)

        self.assertEqual(result.output, """\
No zone records found, domain cli.sexy doesn't seems to be managed at Gandi.
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_all_ko(self):
        args = ['iheartcli.com']
        result = self.invoke_with_exceptions(record.delete, args, input='N\n')

        self.assertEqual(result.output, """\
This command without parameters --type, --name or --value will remove all \
records in this zone file. Are you sur to perform this action ? [y/N]: N
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_all(self):
        args = ['iheartcli.com']
        result = self.invoke_with_exceptions(record.delete, args, input='y\n')

        self.assertEqual(result.output, """\
This command without parameters --type, --name or --value will remove all \
records in this zone file. Are you sur to perform this action ? [y/N]: y
Creating new zone record
Deleting zone record
Activation of new zone version
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        args = ['iheartcli.com', '--name', '@', '--type', 'A',
                '--value', '127.0.0.1']
        result = self.invoke_with_exceptions(record.delete, args)

        self.assertEqual(result.output, """\
Creating new zone record
Deleting zone record
Activation of new zone version
""")
        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.zone.record.delete'][0][2]
        self.assertEqual(params['name'], '@')
        self.assertEqual(params['type'], 'A')
        self.assertEqual(params['value'], '127.0.0.1')

    def test_update_no_zone(self):
        args = ['cli.sexy']
        result = self.invoke_with_exceptions(record.update, args)

        self.assertEqual(result.output, """\
No zone records found, domain cli.sexy doesn't seems to be managed at Gandi.
""")
        self.assertEqual(result.exit_code, 0)

    def test_update_no_param(self):
        args = ['iheartcli.com']
        result = self.invoke_with_exceptions(record.update, args)

        self.assertEqual(result.output, """\
You must indicate a zone file or a record. \
Use `gandi record update --help` for more information
""")
        self.assertEqual(result.exit_code, 0)

    def test_update(self):
        args = ['iheartcli.com',
                '--record', '* 10800 A 73.246.104.110',
                '--new-record', '@ 3600 A 127.0.0.1']
        result = self.invoke_with_exceptions(record.update, args)

        self.assertEqual(result.output, """\
Creating new zone file
Updating zone records
Activation of new zone version
""")
        self.assertEqual(result.exit_code, 0)

    def test_update_file(self):
        args = ['iheartcli.com', '--file', 'sandbox/example.txt']

        content = """\
* 10800 IN A 73.246.104.110
@ 10800 IN A 73.246.104.110
much 10800 IN A 192.243.24.132
blog 10800 IN CNAME blogs.vip.gandi.net.
cloud 10800 IN CNAME gpaas6.dc0.gandi.net.
imap 10800 IN CNAME access.mail.gandi.net.
pop 10800 IN CNAME access.mail.gandi.net.
smtp 10800 IN CNAME relay.mail.gandi.net.
webmail 10800 IN CNAME agent.mail.gandi.net.
@ 10800 IN MX 50 fb.mail.gandi.net.
@ 10800 IN MX 10 spool.mail.gandi.net.
"""

        result = self.isolated_invoke_with_exceptions(record.update, args,
                                                      temp_content=content)
        self.assertEqual(result.output, """\
Creating new zone file
Updating zone records
Activation of new zone version
""")
        self.assertEqual(result.exit_code, 0)
