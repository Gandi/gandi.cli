import re

from .base import CommandTestCase
from gandi.cli.commands import mail
from gandi.cli.core.base import GandiContextHelper


class MailTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(mail.list, ['iheartcli.com'])

        self.assertEqual(result.output, """admin
""")

        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.info, args)

        self.assertEqual(result.output, """login           : admin
aliases         :
fallback email  :
quota usage     : 233 KiB / unlimited
responder active: no
responder text  :
""")

        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['contact@iheartcli.com', '--quota', '2', '--fallback',
                'admin@cli.sexy', '--alias', 'god@iheartcli.com']
        result = self.invoke_with_exceptions(mail.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')

        self.assertEqual(result.output, """password: \
\nRepeat for confirmation: \
\nCreating your mailbox.
Creating aliases.
""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.mailbox.create'][0][2]
        self.assertEqual(params['password'], 'plokiploki')
        self.assertEqual(params['quota'], 2)
        self.assertEqual(params['fallback_email'], 'admin@cli.sexy')

    def test_create_with_password(self):
        args = ['contact2@iheartcli.com', '--quota', '2', '--fallback',
                'admin@cli.sexy', '--alias', 'god@iheartcli.com',
                '--password', 'password_for_create']
        result = self.invoke_with_exceptions(mail.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(result.output, """Creating your mailbox.
Creating aliases.
""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.mailbox.create'][0][2]
        self.assertEqual(params['password'], 'password_for_create')
        self.assertEqual(params['quota'], 2)
        self.assertEqual(params['fallback_email'], 'admin@cli.sexy')

    def test_delete_force(self):
        args = ['admin@iheartcli.com', '--force']
        result = self.invoke_with_exceptions(mail.delete, args)

        self.assertEqual(result.output, '')

        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.delete, args, input='y\n')

        self.assertEqual(result.output, """\
Are you sure to delete the mailbox admin@iheartcli.com ? [y/N]: y
""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_force_refused(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.delete, args, input='\n')

        self.assertEqual(result.output, """\
Are you sure to delete the mailbox admin@iheartcli.com ? [y/N]: \n""")

        self.assertEqual(result.exit_code, 0)

    def test_udpate(self):
        args = ['admin@iheartcli.com', '--quota', '2', '--fallback',
                'admin@cli.sexy', '--alias-add', 'doge@iheartcli.com',
                '--alias-del', 'god@iheartcli.com', '--password']

        result = self.invoke_with_exceptions(mail.update, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')

        self.assertEqual(result.output, """password: \
\nRepeat for confirmation: \
\nUpdating your mailbox.
Updating aliases.
""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['domain.mailbox.update'][0][2]
        self.assertEqual(params['password'], 'plokiploki')
        self.assertEqual(params['quota'], 2)
        self.assertEqual(params['fallback_email'], 'admin@cli.sexy')

    def test_purge(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.purge, args, input='y\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to purge mailbox admin@iheartcli.com ? [y/N]: y
Purging in progress
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_purge_alias(self):
        args = ['admin@iheartcli.com', '--alias']
        result = self.invoke_with_exceptions(mail.purge, args, input='y\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to purge all aliases for mailbox admin@iheartcli.com ? [y/N]: y\
""")

        self.assertEqual(result.exit_code, 0)

    def test_purge_alias_refused(self):
        args = ['admin@iheartcli.com', '--alias']
        result = self.invoke_with_exceptions(mail.purge, args, input='\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to purge all aliases for mailbox admin@iheartcli.com ? [y/N]:\
""")

        self.assertEqual(result.exit_code, 0)

    def test_purge_refused(self):
        args = ['admin@iheartcli.com']
        result = self.invoke_with_exceptions(mail.purge, args, input='\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to purge mailbox admin@iheartcli.com ? [y/N]:\
""")

        self.assertEqual(result.exit_code, 0)
