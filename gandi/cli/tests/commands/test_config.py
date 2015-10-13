# -*- coding: utf-8 -*-
""" Configuration namespace tests. """

import os

from .base import CommandTestCase
from gandi.cli.commands import config


class ConfigTestCase(CommandTestCase):

    def test_get_empty(self):
        result = self.invoke_with_exceptions(config.get, [])
        self.assertEqual(result.exit_code, 2)

    def test_get_unknown(self):
        result = self.invoke_with_exceptions(config.get, ['unknown-key'])
        self.assertEqual(result.output, """No value found.
""")
        self.assertEqual(result.exit_code, 1)

    def test_get(self):
        result = self.invoke_with_exceptions(config.get, ['api'])
        self.assertEqual(result.exit_code, 0)

    def test_set_empty(self):
        result = self.invoke_with_exceptions(config.set, [])
        self.assertEqual(result.exit_code, 2)

        result = self.invoke_with_exceptions(config.set, ['some-key'])
        self.assertEqual(result.exit_code, 2)

    def test_set_empty_value(self):
        result = self.invoke_with_exceptions(config.set, ['some-key'])
        self.assertEqual(result.exit_code, 2)

    def test_set_get(self):
        result = self.invoke_with_exceptions(config.set, ['dummy'])
        self.assertEqual(result.exit_code, 2)

        result = self.invoke_with_exceptions(config.set, ['dummy',
                                                          'v4lu3'])
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(config.get, ['dummy'])
        self.assertEqual(result.output, """v4lu3
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_empty(self):
        result = self.invoke_with_exceptions(config.set, [])
        self.assertEqual(result.exit_code, 2)

    def test_delete(self):
        result = self.invoke_with_exceptions(config.set, ['dummy', 'value'])
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(config.get, ['dummy'])
        self.assertEqual(result.output, """value
""")
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(config.delete, ['dummy'])
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(config.get, ['unknown-key'])
        self.assertEqual(result.output, """No value found.
""")
        self.assertEqual(result.exit_code, 1)

    def test_edit(self):
        os.environ['EDITOR'] = '/usr/bin/nano'
        result = self.invoke_with_exceptions(config.get, ['editor'])
        self.assertEqual(result.output, """/usr/bin/nano
""")
        self.assertEqual(result.exit_code, 0)

        del os.environ['EDITOR']
        result = self.invoke_with_exceptions(config.set, ['editor',
                                                          '/usr/bin/vi'])
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(config.get, ['editor'])
        self.assertEqual(result.output, """/usr/bin/vi
""")
        self.assertEqual(result.exit_code, 0)
