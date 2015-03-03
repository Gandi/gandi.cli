import re

from click.exceptions import ClickException

from .base import CommandTestCase
from gandi.cli.commands import disk
from gandi.cli.core.utils.size import disk_check_size


class DiskTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(disk.list, [])

        self.assertEqual(result.output, """name      : data
state     : created
size      : 10240
----------
name      : arch64
state     : created
size      : 10240
----------
name      : sys_docker
state     : created
size      : 3072
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        result = self.runner.invoke(disk.info, ['arch64'])

        self.assertEqual(result.output, """name      : arch64
state     : created
size      : 10240
type      : data
id        : 4204
kernel    : 3.2-x86_64
datacenter: FR
vm        : arch64
""")
        self.assertEqual(result.exit_code, 0)

    def test_check_size(self):
        result = disk_check_size(None, None, 2048)
        self.assertEqual(result, 2048)
        self.assertRaises(ClickException, disk_check_size, None, None, 2040)

    def __test_detach(self):
        result = self.runner.invoke(disk.detach, ['data'])
        self.assertEqual(result.output.strip(),
                         "Are you sure to detach data? [y/N]:"
                         )
        self.assertEqual(result.exit_code, 0)

    def test_detach_forced(self):
        result = self.runner.invoke(disk.detach, ['-f', 'data'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The disk is still attached to the vm 80458.
Will detach it.
Detaching your disk(s).
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
