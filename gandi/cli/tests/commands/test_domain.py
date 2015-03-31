from .base import CommandTestCase
from gandi.cli.commands import domain


class DomainTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(domain.list, [], catch_exceptions=False)

        self.assertEqual(result.output, """iheartcli.com
cli.sexy
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        result = self.runner.invoke(domain.info, ['iheartcli.com'],
                                    catch_exceptions=False)

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
