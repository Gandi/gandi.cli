# -*- coding: utf-8 -*-
import re
import sys
from datetime import datetime

from .base import CommandTestCase
from ..compat import mock
from gandi.cli.commands import dnssec


class DnssecTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(dnssec.list, ['iheartcli.com'])

        self.maxDiff = None
        if sys.version_info[0] == 2:
            self.assertEqual(result.output, """[{'algorithm': 5,\n  'date_created': datetime.datetime(2012, 2, 24, 17, 16, 8),\n  'digest': '457c626c008cc70d68133254abc4ee4eb79e4e6c99f9423b60b543fa8a69e6ac',\n  'digest_type': 2,\n  'flags': 257,\n  'id': 125,\n  'keytag': 9301,\n  'public_key': 'AwEAAdYixYvq9eJLRQcxUeYJWaxAGXiP/K1/C7XHbUWGzA8AHCRp81FAmfwcw1FrJ7bMViEegewPDGciQSv5HotPPOynUmkZbgztOeejH/+3Il/cM8SW4Et0i+99S7l9as+FI3AYOhsllDJK1WM9smn0S/9igfpR2dGmCyDU ZfeR1A49\\n'}]\n""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        result = self.invoke_with_exceptions(
            dnssec.create,
            ['iheartcli.com',
             '--flags', 257,
             '--algorithm', 5,
             '--public_key', 'AwEAAdYixYvq9eJLRQcxUeYJWaxAGXiP/K1/C7XHbUWGzA8AHCRp81FA'
                             'mfwcw1FrJ7bMViEegewPDGciQSv5HotPPOynUmkZbgztOeejH/+3Il/c'
                             'M8SW4Et0i+99S7l9as+FI3AYOhsllDJK1WM9smn0S/9igfpR2dGmCyDU ZfeR1A49',
             ])

        self.assertEqual(result.output, """""")
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):

        result = self.invoke_with_exceptions(dnssec.delete, ['125'])

        self.assertEqual(result.output, """Delete successful.\n""")
        self.assertEqual(result.exit_code, 0)
