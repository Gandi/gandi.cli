# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import account


class AccountTestCase(CommandTestCase):

    def test_info(self):

        result = self.invoke_with_exceptions(account.info, [])

        self.assertEqual(result.output, """\
handle           : PXP561-GANDI
prepaid          : 1337.42 EUR
credits          :
        available: 2335360
        usage    : 633/h
        time left: 0 year(s) 4 month(s) 29 day(s) 17 hour(s)
""")
        self.assertEqual(result.exit_code, 0)
