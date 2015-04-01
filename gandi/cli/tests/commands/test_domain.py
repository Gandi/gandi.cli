from .base import CommandTestCase
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
        result = self.invoke_with_exceptions(domain.info, ['iheartcli.com'])

        self.assertEqual(result.output, """owner       : AA1-GANDI
admin       : AA2-GANDI
bill        : AA3-GANDI
tech        : AA5-GANDI
reseller    : AA4-GANDI
fqdn        : iheartcli.com
nameservers : ['a.dns.gandi.net', 'b.dns.gandi.net', 'c.dns.gandi.net']
services    : ['gandidns']
zone_id     : 424242
tags        : bla
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        result = self.invoke_with_exceptions(domain.create,
                                             ['--domain', 'idontlike.website',
                                              '--duration', 1,
                                              '--owner', 'OWNER1-GANDI',
                                              '--admin', 'ADMIN1-GANDI',
                                              '--tech', 'TECH1-GANDI',
                                              '--bill', 'BILL1-GANDI',
                                              ])

        self.assertTrue('Your domain idontlike.website has been created'
                        in result.output)
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
