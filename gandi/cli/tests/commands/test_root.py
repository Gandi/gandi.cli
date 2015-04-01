# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import root


class RootTestCase(CommandTestCase):

    def test_api(self):

        result = self.invoke_with_exceptions(root.api, [])

        self.assertEqual(result.output, """\
API version: 3.3.42
""")
        self.assertEqual(result.exit_code, 0)
