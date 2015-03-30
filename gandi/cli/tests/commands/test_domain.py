# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import domain


class DomainTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(domain.list, [])

        self.assertEqual(result.output, """\
smurfies.com
roboperk.io
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['roboperk.io']
        result = self.runner.invoke(domain.info, args)

        self.assertEqual(result.output, """\
owner       : PXP561-GANDI
admin       : PXP561-GANDI
bill        : PXP561-GANDI
tech        : PXP561-GANDI
fqdn        : roboperk.io
nameservers : ['a.dns.gandi.net', 'b.dns.gandi.net', 'c.dns.gandi.net']
services    : ['gandidns', 'gandimail', 'paas']
zone_id     : 431190141
tags        :
""")
        self.assertEqual(result.exit_code, 0)
