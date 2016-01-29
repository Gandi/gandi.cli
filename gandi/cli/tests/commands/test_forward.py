# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import CommandTestCase
from gandi.cli.commands import forward


class ForwardTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(forward.list, ['iheartcli.com'])

        self.assertEqual(result.output, """\
admin         : admin@cli.sexy
admin         : grumpy@cat.lol
contact       : contact@cli.sexy
""")

        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['backup@iheartcli.com', '--destination', 'backup@cat.lol']
        result = self.invoke_with_exceptions(forward.create, args)

        self.assertEqual(result.output, """\
Creating mail forward backup@iheartcli.com
""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.forward.create'][0][2]
        self.assertEqual(params['destinations'], ['backup@cat.lol'])

    def test_delete_force(self):
        args = ['admin@iheartcli.com', '--force']
        result = self.invoke_with_exceptions(forward.delete, args)

        self.assertEqual(result.output, '')

        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(forward.delete, args, input='y\n')

        self.assertEqual(result.output, """\
Are you sure to delete the domain mail forward admin@iheartcli.com ? [y/N]: y
""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_force_refused(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(forward.delete, args, input='\n')

        self.assertEqual(result.output, """\
Are you sure to delete the domain mail forward admin@iheartcli.com ? [y/N]: \
\n""")

        self.assertEqual(result.exit_code, 0)

    def test_update(self):
        args = ['admin@iheartcli.com',
                '--dest-add', 'doge@iheartcli.com',
                '--dest-del', 'grumpy@cat.lol']

        result = self.invoke_with_exceptions(forward.update, args)

        self.assertEqual(result.output, """\
Updating mail forward admin@iheartcli.com
""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.forward.update'][0][2]
        self.assertEqual(params['destinations'], ['admin@cli.sexy',
                                                  'doge@iheartcli.com'])

    def test_update_no_param(self):
        args = ['admin@iheartcli.com']

        result = self.invoke_with_exceptions(forward.update, args)

        self.assertEqual(result.output, """\
Nothing to update: you must provide destinations to update, use \
--dest-add/-a or -dest-del/-d parameters.
""")

        self.assertEqual(result.exit_code, 0)
