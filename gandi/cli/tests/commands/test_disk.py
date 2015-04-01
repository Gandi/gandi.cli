import re

from click.exceptions import ClickException

from .base import CommandTestCase
from gandi.cli.commands import disk
from gandi.cli.core.utils.size import disk_check_size


class DiskTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(disk.list, [])

        self.assertEqual(result.output, """name      : sys_1426759833
state     : created
size      : 3072
----------
name      : sys_server01
state     : created
size      : 3072
----------
name      : data
state     : created
size      : 3072
""")

        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        result = self.invoke_with_exceptions(disk.info, ['sys_server01'])

        self.assertEqual(result.output, """name      : sys_server01
state     : created
size      : 3072
type      : data
id        : 4969249
kernel    : 3.12-x86_64 (hvm)
datacenter: FR
vm        : server01
""")
        self.assertEqual(result.exit_code, 0)

    def test_check_size(self):
        result = disk_check_size(None, None, 2048)
        self.assertEqual(result, 2048)
        self.assertRaises(ClickException, disk_check_size, None, None, 2040)

    def test_detach(self):
        result = self.invoke_with_exceptions(disk.detach, ['data'])
        self.assertEqual(result.output.strip(),
                         "Are you sure you want to detach data? [y/N]:")
        self.assertEqual(result.exit_code, 0)

    def test_detach_forced(self):
        result = self.invoke_with_exceptions(disk.detach, ['-f', 'data'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The disk is still attached to the vm 152967.
Will detach it.
Detaching your disk(s).
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
