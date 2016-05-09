# -*- coding: utf-8 -*-
import re
from datetime import datetime

from .base import CommandTestCase
from ..compat import mock
from gandi.cli.commands import domain
from gandi.cli.core.utils import DomainNotAvailable


class DomainTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(domain.list, [])

        self.assertEqual(result.output, """iheartcli.com
cli.sexy
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        with mock.patch('gandi.cli.core.utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2015, 7, 1)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args,
                                                                     **kw)

            result = self.invoke_with_exceptions(domain.info,
                                                 ['iheartcli.com'])

        self.assertEqual(result.output, """owner       : AA1-GANDI
admin       : AA2-GANDI
bill        : AA3-GANDI
tech        : AA5-GANDI
reseller    : AA4-GANDI
fqdn        : iheartcli.com
nameservers : a.dns.gandi.net, b.dns.gandi.net, c.dns.gandi.net
services    : gandidns
zone_id     : 424242
tags        : bla
created     : 2010-09-22 15:06:18
expires     : 2015-09-22 00:00:00 (in 83 days)
updated     : 2014-09-21 03:10:07
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_no_option_no_argument(self):
        args = ['--duration', 1,
                '--owner', 'OWNER1-GANDI',
                '--admin', 'ADMIN1-GANDI',
                '--tech', 'TECH1-GANDI',
                '--bill', 'BILL1-GANDI',
                ]
        result = self.invoke_with_exceptions(domain.create, args,
                                             input='idontlike.website\n')

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Name of the domain: idontlike.website
Creating your domain.
\rProgress: [###] 100.00%  00:00:00  \n\
Your domain idontlike.website has been created.""")

        self.assertEqual(result.exit_code, 0)
#         self.assertEqual(result.output.strip(), """\
# Name of the domain.:\
# """)

    def test_create_option(self):
        result = self.invoke_with_exceptions(domain.create,
                                             ['--domain', 'idontlike.website',
                                              '--duration', 1,
                                              '--owner', 'OWNER1-GANDI',
                                              '--admin', 'ADMIN1-GANDI',
                                              '--tech', 'TECH1-GANDI',
                                              '--bill', 'BILL1-GANDI',
                                              '--nameserver', 'a.domain.tld',
                                              '--nameserver', 'b.domain.tld',
                                              ])

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
/!\ --domain option is deprecated and will be removed upon next release.
You should use 'gandi domain create idontlike.website' instead.
Creating your domain.
\rProgress: [###] 100.00%  00:00:00  \n\
Your domain idontlike.website has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_argument(self):
        result = self.invoke_with_exceptions(domain.create,
                                             ['idontlike.website',
                                              '--duration', 1,
                                              '--owner', 'OWNER1-GANDI',
                                              '--admin', 'ADMIN1-GANDI',
                                              '--tech', 'TECH1-GANDI',
                                              '--bill', 'BILL1-GANDI',
                                              ])

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Creating your domain.
\rProgress: [###] 100.00%  00:00:00  \n\
Your domain idontlike.website has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_argument_and_option_different(self):
        result = self.invoke_with_exceptions(domain.create,
                                             ['idontlike.website',
                                              '--domain', 'idontlike.bike',
                                              '--duration', 1,
                                              '--owner', 'OWNER1-GANDI',
                                              '--admin', 'ADMIN1-GANDI',
                                              '--tech', 'TECH1-GANDI',
                                              '--bill', 'BILL1-GANDI',
                                              ])

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
/!\ --domain option is deprecated and will be removed upon next release.
You should use 'gandi domain create idontlike.bike' instead.
/!\ You specified both an option and an argument which are different, \
please choose only one between: idontlike.bike and idontlike.website.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_argument_and_option_equal(self):
        result = self.invoke_with_exceptions(domain.create,
                                             ['idontlike.website',
                                              '--domain', 'idontlike.website',
                                              '--duration', 1,
                                              '--owner', 'OWNER1-GANDI',
                                              '--admin', 'ADMIN1-GANDI',
                                              '--tech', 'TECH1-GANDI',
                                              '--bill', 'BILL1-GANDI',
                                              ])

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
/!\ --domain option is deprecated and will be removed upon next release.
You should use 'gandi domain create idontlike.website' instead.
Creating your domain.
\rProgress: [###] 100.00%  00:00:00  \n\
Your domain idontlike.website has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_background_argument(self):
        args = ['roflozor.com', '--background']
        result = self.invoke_with_exceptions(domain.create, args)

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Duration [1]: \n\
{'id': 400, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)

    def test_create_background_option(self):
        args = ['--domain', 'roflozor.com', '--background']
        result = self.invoke_with_exceptions(domain.create, args)

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Duration [1]: \n\
/!\ --domain option is deprecated and will be removed upon next release.
You should use 'gandi domain create roflozor.com' instead.
{'id': 400, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)

    def test_renew(self):
        result = self.invoke_with_exceptions(domain.renew,
                                             ['iheartcli.com',
                                              '--duration', 1,
                                              ])

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Renewing your domain.
\rProgress: [###] 100.00%  00:00:00  \n\
Your domain iheartcli.com has been renewed.""")

        self.assertEqual(result.exit_code, 0)

    def test_renew_background_ok(self):
        args = ['iheartcli.com', '--background']
        result = self.invoke_with_exceptions(domain.renew, args)

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())
        self.assertEqual(output, """\
Duration [1]: \n\
{'id': 400, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)

    def test_available_with_exception(self):

        self.assertRaises(DomainNotAvailable,
                          self.invoke_with_exceptions, domain.create,
                          ['--domain', 'unavailable1.website',
                           '--duration', 1,
                           '--owner', 'OWNER1-GANDI',
                           '--admin', 'ADMIN1-GANDI',
                           '--tech', 'TECH1-GANDI',
                           '--bill', 'BILL1-GANDI',
                           ])

    def test_available_with_exception_argument(self):
        self.assertRaises(DomainNotAvailable,
                          self.invoke_with_exceptions, domain.create,
                          ['unavailable1.website',
                           '--duration', 1,
                           '--owner', 'OWNER1-GANDI',
                           '--admin', 'ADMIN1-GANDI',
                           '--tech', 'TECH1-GANDI',
                           '--bill', 'BILL1-GANDI',
                           ])
