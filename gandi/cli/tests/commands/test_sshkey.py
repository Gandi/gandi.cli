# -*- coding: utf-8 -*-
from datetime import datetime

from .base import CommandTestCase
from ..compat import mock
from gandi.cli.commands import sshkey


class SSHKeyTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(sshkey.list, [])

        self.assertEqual(result.output, """name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
----------
name        : mysecretkey
fingerprint : 09:11:21:e3:90:3c:7d:d5:06:d9:6f:f9:36:e1:99:a6
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):

        result = self.invoke_with_exceptions(sshkey.list, ['--id'])

        self.assertEqual(result.output, """name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
id          : 134
----------
name        : mysecretkey
fingerprint : 09:11:21:e3:90:3c:7d:d5:06:d9:6f:f9:36:e1:99:a6
id          : 141
""")

        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        with mock.patch('gandi.cli.core.utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2015, 7, 1)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args,
                                                                     **kw)

            result = self.invoke_with_exceptions(sshkey.info,
                                                 ['134'])

            self.assertEqual(result.output, """\
name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
""")

            self.assertEqual(result.exit_code, 0)

    def test_info_with_id(self):
        with mock.patch('gandi.cli.core.utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2015, 7, 1)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args,
                                                                     **kw)

            result = self.invoke_with_exceptions(sshkey.info,
                                                 ['134', '--id', '--value'])

            self.assertEqual(result.output, """\
name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
id          : 134
value       : val
""")

            self.assertEqual(result.exit_code, 0)

    def test_delete_id(self):
        result = self.invoke_with_exceptions(sshkey.delete, ['134'])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_delete_name(self):
        result = self.invoke_with_exceptions(sshkey.delete, ['mysecretkey'])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_create_no_value_no_filename(self):
        result = self.invoke_with_exceptions(sshkey.create, ['--name', 'mynewsecretkey'])

        self.assertEqual(result.output, 'Usage: sshkey create [OPTIONS]\n\nError: You must set value OR filename.\n')
        self.assertEqual(result.exit_code, 2)

    def test_create_value_and_filename(self):
        result = self.invoke_with_exceptions(sshkey.create, ['--name', 'mynewsecretkey', '--value', 'value', '--filename', '/dev/null'])

        self.assertEqual(result.output, 'Usage: sshkey create [OPTIONS]\n\nError: You must not set value AND filename.\n')
        self.assertEqual(result.exit_code, 2)

    def test_create_value_return_none(self):
        result = self.invoke_with_exceptions(sshkey.create, ['--name', 'return-none', '--value', 'value'])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_create_value(self):
        result = self.invoke_with_exceptions(sshkey.create, ['--name', 'mynewsecretkey', '--value', 'value'])

        self.assertEqual(result.output, """id          : 200
name        : mynewsecretkey
fingerprint : bb01
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_filename(self):
        from tempfile import NamedTemporaryFile
        fhandle = NamedTemporaryFile()
        fhandle.write('value')
        fhandle.flush()

        result = self.invoke_with_exceptions(sshkey.create, ['--name', 'mynewsecretkey2', '--filename', fhandle])

        self.assertEqual(result.output, """id          : 200
name        : mynewsecretkey2
fingerprint : bb01
""")
        self.assertEqual(result.exit_code, 0)

        fhandle.close()
