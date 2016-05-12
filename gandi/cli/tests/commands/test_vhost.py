# -*- coding: utf-8 -*-

import re

from .base import CommandTestCase
from gandi.cli.commands import vhost


class VhostTestCase(CommandTestCase):

    def test_list(self):
        args = ['--id', '--names']
        result = self.invoke_with_exceptions(vhost.list, args)

        self.assertEqual(result.output, """\
name          : aa3e0e26f8.url-de-test.ws
state         : running
date_creation : 20130903T22:11:54
paas_id       : 126276
paas_name     : paas_owncloud
----------
name          : cloud.cat.lol
state         : running
date_creation : 20130903T22:24:06
paas_id       : 126276
paas_name     : paas_owncloud
----------
name          : 187832c2b34.testurl.ws
state         : running
date_creation : 20141025T15:50:54
paas_id       : 163744
paas_name     : paas_cozycloud
----------
name          : cloud.iheartcli.com
state         : running
date_creation : 20141025T15:50:54
paas_id       : 163744
paas_name     : paas_cozycloud
----------
name          : cli.sexy
state         : running
date_creation : 20150728T17:50:56
paas_id       : 163744
paas_name     : paas_cozycloud
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['cloud.cat.lol', 'cloud.iheartcli.com', '--id']
        result = self.invoke_with_exceptions(vhost.info, args)

        self.assertEqual(result.output, """\
name          : cloud.cat.lol
state         : running
date_creation : 20130903T22:24:06
ssl           : disabled
paas_id       : 126276
paas_name     : paas_owncloud
----------
name          : cloud.iheartcli.com
state         : running
date_creation : 20141025T15:50:54
ssl           : disabled
paas_id       : 163744
paas_name     : paas_cozycloud
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['pouet.lol.cat', '--paas', 'paas_owncloud']
        result = self.invoke_with_exceptions(vhost.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating a new vhost.
\rProgress: [###] 100.00%  00:00:00  \
\nYour vhost pouet.lol.cat has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_ssl(self):
        args = ['pouet.lol.cat', '--paas', 'paas_owncloud', '--ssl']
        result = self.invoke_with_exceptions(vhost.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please give the private key for certificate id 710 (CN: lol.cat)""")

        self.assertEqual(result.exit_code, 0)

    def test_create_background(self):
        args = ['pouet.lol.cat', '--paas', 'paas_owncloud', '--bg']
        result = self.invoke_with_exceptions(vhost.create, args)

        self.assertEqual(result.output.strip(), """\
{'id': 200, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)

    def test_update_ssl_ko(self):
        args = ['pouet.lol.cat', '--ssl']
        result = self.invoke_with_exceptions(vhost.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please give the private key for certificate id 710 (CN: lol.cat)""")

        self.assertEqual(result.exit_code, 0)

    def test_update_ssl_ok(self):
        args = ['unknown.lol.cat', '--ssl']
        result = self.invoke_with_exceptions(vhost.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
There is no certificate for unknown.lol.cat.
Create the certificate with (for exemple) :
$ gandi certificate create --cn unknown.lol.cat --type std \
\nOr relaunch the current command with --poll-cert option""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_prompt_ok(self):
        args = ['pouet.lol.cat']
        result = self.invoke_with_exceptions(vhost.delete, args,
                                             input='y\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete vhost pouet.lol.cat? [y/N]: y
Deleting your vhost.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_prompt_ko(self):
        args = ['pouet.lol.cat']
        result = self.invoke_with_exceptions(vhost.delete, args,
                                             input='N\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete vhost pouet.lol.cat? [y/N]: N""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_force(self):
        args = ['pouet.lol.cat', '--force']
        result = self.invoke_with_exceptions(vhost.delete, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Deleting your vhost.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_background(self):
        args = ['pouet.lol.cat', '--force', '--bg']
        result = self.invoke_with_exceptions(vhost.delete, args)

        self.assertEqual(result.output.strip(), """\
name      : rproxy_update
paas_id   : 1177220
date_creation: 20150728T17:50:56""")
        self.assertEqual(result.exit_code, 0)
