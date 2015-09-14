import re

from .base import CommandTestCase
from gandi.cli.commands import mail


class MailTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(mail.list, ['iheartcli.com'])

        self.assertEqual(result.output, """admin
""")

        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.info, args)

        self.assertEqual(result.output, """login         : admin
aliases       :
fallback_email:
quota         : {'granted': 0, 'used': 233}
responder     : {'active': False, 'text': None}
""")

        self.assertEqual(result.exit_code, 0)
