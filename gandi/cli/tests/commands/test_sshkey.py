from .base import CommandTestCase
from gandi.cli.commands import sshkey


class SSHKeyTestCase(CommandTestCase):

    def test_list(self):
        args = ['--id']
        result = self.invoke_with_exceptions(sshkey.list, args)

        self.assertEqual(result.output, """\
name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
id          : 134
----------
name        : mysecretkey
fingerprint : 09:11:21:e3:90:3c:7d:d5:06:d9:6f:f9:36:e1:99:a6
id          : 141
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['default', '--id', '--value']
        result = self.invoke_with_exceptions(sshkey.info, args)

        self.assertEqual(result.output, """\
name        : default
fingerprint : b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5
id          : 134
value       : ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC63QZAW3tusdv+JuyzOoXTND9/wxKogMwZbxBPPtoN7Hjnyn0kUUHMJ6ji5xpbatRYKOeGAoZDW2TXojvbJdQj7tWsRr7ES0qB9qhDGVSDIJWRQ6f9MQCCLjV5tpBTAwb unknown@lol.cat
""")  # noqa
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        args = ['mysecretkey']
        result = self.invoke_with_exceptions(sshkey.delete, args)

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_create_value_and_filename_ko(self):
        args = ['--name', 'newkey', '--value',
                'ssh-rsa LjV5tpBTAwb unknown@inter.net',
                '--filename', 'sandbox/example.txt']

        content = """\
ssh-rsa LjV5tpBTAwb unknown@inter.net
"""
        result = self.isolated_invoke_with_exceptions(sshkey.create, args,
                                                      temp_content=content)

        self.assertEqual(result.output, """\
Usage: sshkey create [OPTIONS]

Error: You must not set value AND filename.
""")
        self.assertEqual(result.exit_code, 2)

    def test_create_no_value_and_no_filename_ko(self):
        args = ['--name', 'newkey']

        result = self.invoke_with_exceptions(sshkey.create, args)

        self.assertEqual(result.output, """\
Usage: sshkey create [OPTIONS]

Error: You must set value OR filename.
""")
        self.assertEqual(result.exit_code, 2)

    def test_create_value_ok(self):
        args = ['--name', 'newkey', '--value',
                'ssh-rsa LjV5tpBTAwb unknown@inter.net']

        result = self.invoke_with_exceptions(sshkey.create, args)

        self.assertEqual(result.output, """\
id          : 145
name        : newkey
fingerprint : b3:11:67:10:2e:1b:a5:55:ed:16:24:98:3e:2e:ed:f5
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_file_ok(self):
        args = ['--name', 'newkey', '--filename', 'sandbox/example.txt']

        content = """\
ssh-rsa LjV5tpBTAwb unknown@inter.net
"""
        result = self.isolated_invoke_with_exceptions(sshkey.create, args,
                                                      temp_content=content)

        self.assertEqual(result.output, """\
id          : 145
name        : newkey
fingerprint : b3:11:67:10:2e:1b:a5:55:ed:16:24:98:3e:2e:ed:f5
""")
        self.assertEqual(result.exit_code, 0)
