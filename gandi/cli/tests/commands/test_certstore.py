# -*- coding: utf-8 -*-

from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import certstore


class CertStoreTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(certstore.list, [])

        self.assertEqual(result.output, """\
subject   : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
----------
subject   : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
----------
subject   : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test2.domain.fr
----------
subject   : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test3.domain.fr
----------
subject   : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
----------
subject   : /OU=Domain Control Validated/OU=Gandi Standard Wildcard SSL/CN=*.domain.fr
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_all(self):

        result = self.invoke_with_exceptions(certstore.list, ['--id',
                                                              '--vhosts',
                                                              '--dates',
                                                              '--fqdns'])
        self.assertEqual(result.output, """\
id          : 1
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
date_created: 20150407T00:00:00
date_expire : 20160316T00:00:00
	----------
	fqdn      : test1.domain.fr
	----------
	vhost     : test1.domain.fr
	type      : paas
----------
id          : 2
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
date_created: 20150407T00:00:00
date_expire : 20160316T00:00:00
	----------
	fqdn      : test1.domain.fr
	----------
	vhost     : test1.domain.fr
	type      : paas
----------
id          : 3
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test2.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test2.domain.fr
----------
id          : 4
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test3.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test3.domain.fr
----------
id          : 5
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test4.domain.fr
----------
id          : 6
subject     : /OU=Domain Control Validated/OU=Gandi Standard Wildcard SSL/CN=*.domain.fr
date_created: 20150409T00:00:00
date_expire : 20160409T00:00:00
	----------
	fqdn      : *.domain.fr
	----------
	vhost     : *.domain.fr
	type      : paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_fqdn(self):

        result = self.invoke_with_exceptions(certstore.info, ['test1.domain.fr'])

        self.assertEqual(result.output, """\
id          : 1
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
date_created: 20150407T00:00:00
date_expire : 20160316T00:00:00
	----------
	fqdn      : test1.domain.fr
	----------
	vhost     : test1.domain.fr
	type      : paas
----------
id          : 2
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
date_created: 20150407T00:00:00
date_expire : 20160316T00:00:00
	----------
	fqdn      : test1.domain.fr
	----------
	vhost     : test1.domain.fr
	type      : paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_id(self):
        result = self.invoke_with_exceptions(certstore.info, ['1'])

        self.assertEqual(result.output, """\
id          : 1
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
date_created: 20150407T00:00:00
date_expire : 20160316T00:00:00
	----------
	fqdn      : test1.domain.fr
	----------
	vhost     : test1.domain.fr
	type      : paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        result = self.invoke_with_exceptions(certstore.create,
                                             ['--pk', 'PK', '--crt', 'CRT'])

        self.assertEqual(result.output, """\
id          : 5
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test4.domain.fr
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_id(self):
        result = self.invoke_with_exceptions(certstore.create,
                                             ['--pk', 'PK', '--crt-id', '701'])

        self.assertEqual(result.output, """\
id          : 5
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test4.domain.fr
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_missing(self):
        result = self.invoke_with_exceptions(certstore.create,
                                             ['--pk', 'PK'])

        self.assertEqual(result.output, """\
One of --certificate or --certificate-id is needed.
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_too_many(self):
        args = ['--pk', 'PK', '--crt', 'CRT', '--crt-id', '999']
        result = self.invoke_with_exceptions(certstore.create, args)

        self.assertEqual(result.output, """\
Only one of --certificate or --certificate-id is needed.
id          : 5
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test4.domain.fr
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_parameter_files(self):
        args = ['--pk', '/tmp/pk.key', '--crt', '/tmp/key.crt']
        with mock.patch('gandi.cli.commands.certstore.os.path.isfile',
                        create=True) as mock_isfile:
            mock_isfile.return_value = True

            with mock.patch('gandi.cli.commands.certstore.open',
                            create=True) as mock_open:
                mock_open.return_value = mock.MagicMock()

                result = self.invoke_with_exceptions(certstore.create, args)

        self.assertEqual(result.output, """\
id          : 5
subject     : /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test4.domain.fr
date_created: 20150408T00:00:00
date_expire : 20160408T00:00:00
	----------
	fqdn      : test4.domain.fr
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        result = self.invoke_with_exceptions(certstore.delete, ['1'])

        self.assertEqual(result.output, """\
Are you sure to delete the following hosted certificates ?
1: /OU=Domain Control Validated/OU=Gandi Standard SSL/CN=test1.domain.fr
 [y/N]: \

""")
        self.assertEqual(result.exit_code, 0)

        result = self.invoke_with_exceptions(certstore.delete, ['1', '-f'])
        self.assertEqual(result.output, """\
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_unknown(self):
        args = ['100.fr', '-f']
        result = self.invoke_with_exceptions(certstore.delete, args)

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)
