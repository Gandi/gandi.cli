# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import oper


class OperTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(oper.list, [])

        self.assertEqual(result.output, """\
id        : 100303
type      : certificate_update
step      : WAIT
----------
id        : 100302
type      : certificate_update
step      : RUN
----------
id        : 100300
type      : certificate_update
step      : RUN
----------
id        : 100200
type      : billing_prepaid_add_money
step      : BILL
----------
id        : 100100
type      : domain_renew
step      : BILL
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.invoke_with_exceptions(oper.info, ['100100'])

        self.assertEqual(result.output, """\
id        : 100100
type      : domain_renew
step      : BILL
last_error:
""")
        self.assertEqual(result.exit_code, 0)
