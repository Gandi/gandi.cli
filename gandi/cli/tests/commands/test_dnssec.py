# -*- coding: utf-8 -*-
import sys

from .base import CommandTestCase
from gandi.cli.commands import dnssec


class DnssecTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(dnssec.list, ['iheartcli.com'])

        self.maxDiff = None
        if sys.version_info[0] == 2:
            self.assertEqual(result.output, """[{'algorithm': 5,\n  'date_created': datetime.datetime(2012, 2, 24, 17, 16, 8),\n  'digest': '457c626c008cc70d68133254abc4ee4eb79e4e6c99f9423b60b543fa8a69e6ac',\n  'digest_type': 2,\n  'flags': 257,\n  'id': 125,\n  'keytag': 9301,\n  'public_key': 'AwEAAdYixYvq9eJLRQcxUeYJWaxAGXiP/K1/C7XHbUWGzA8AHCRp81FAmfwcw1FrJ7bMViEegewPDGciQSv5HotPPOynUmkZbgztOeejH/+3Il/cM8SW4Et0i+99S7l9as+FI3AYOhsllDJK1WM9smn0S/9igfpR2dGmCyDU ZfeR1A49\\n'}]\n""")  # noqa
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        result = self.invoke_with_exceptions(
            dnssec.create,
            ['iheartcli.com',
             '--flags', '257',
             '--algorithm', '5',
             '--public_key', 'AwEAAdYixYvq9eJLRQcxUeYJWaxAGXiP/K1/C7XHbUWGzA8A'
                             'HCRp81FAmfwcw1FrJ7bMViEegewPDGciQSv5HotPPOynUmkZ'
                             'bgztOeejH/+3Il/cM8SW4Et0i+99S7l9as+FI3AYOhsllDJK'
                             '1WM9smn0S/9igfpR2dGmCyDU ZfeR1A49',
             ])

        self.assertEqual(result.output, """""")
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):

        result = self.invoke_with_exceptions(dnssec.delete, ['125'])

        self.assertEqual(result.output, """Delete successful.\n""")
        self.assertEqual(result.exit_code, 0)

    def test_help(self):

        result = self.invoke_with_exceptions(dnssec.create, ['--help'])

        self.assertIn('--algorithm [1|2|3|5|6|7|8|10|12|13|14|15|16|253|254]', result.output)
        self.assertIn('--flags [256|257]', result.output)

        self.assertEqual(result.exit_code, 0)
