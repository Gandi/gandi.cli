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
----------
name      : snaptest
state     : created
size      : 3072
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_vm(self):

        result = self.invoke_with_exceptions(disk.list, ['--vm'])

        self.assertEqual(result.output, """name      : sys_1426759833
state     : created
size      : 3072
vm        : vm1426759833
----------
name      : sys_server01
state     : created
size      : 3072
vm        : server01
----------
name      : data
state     : created
size      : 3072
vm        : server01
----------
name      : snaptest
state     : created
size      : 3072
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):

        result = self.invoke_with_exceptions(disk.list, ['--id'])

        self.assertEqual(result.output, """name      : sys_1426759833
state     : created
size      : 3072
id        : 4969232
----------
name      : sys_server01
state     : created
size      : 3072
id        : 4969249
----------
name      : data
state     : created
size      : 3072
id        : 4970079
----------
name      : snaptest
state     : created
size      : 3072
id        : 663497
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_type(self):

        result = self.invoke_with_exceptions(disk.list, ['--type'])

        self.assertEqual(result.output, """name      : sys_1426759833
state     : created
size      : 3072
type      : data
----------
name      : sys_server01
state     : created
size      : 3072
type      : data
----------
name      : data
state     : created
size      : 3072
type      : data
----------
name      : snaptest
state     : created
size      : 3072
type      : snapshot
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_only_data(self):

        result = self.invoke_with_exceptions(disk.list, ['--only-data'])

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

    def test_list_only_snapshot(self):

        result = self.invoke_with_exceptions(disk.list, ['--only-snapshot'])

        self.assertEqual(result.output, """name      : snaptest
state     : created
size      : 3072
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_snapshotprofile(self):

        result = self.invoke_with_exceptions(disk.list, ['--snapshotprofile'])

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
profile   : minimal
----------
name      : snaptest
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

    def test_info_multiple(self):
        args = ['sys_server01', 'data']
        result = self.invoke_with_exceptions(disk.info, args)

        self.assertEqual(result.output, """name      : data
state     : created
size      : 3072
type      : data
id        : 4970079
datacenter: FR
vm        : server01
----------
name      : sys_server01
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

    def test_detach_background(self):
        args = ['data', '--bg', '-f']
        result = self.invoke_with_exceptions(disk.detach, args)

        self.assertEqual(result.output, """\
The disk is still attached to the vm 152967.
Will detach it.
[{'id': 200, 'step': 'WAIT'}]
""")

    def test_attach(self):
        args = ['snaptest', 'server01']
        result = self.invoke_with_exceptions(disk.attach, args)
        self.assertEqual(result.output.strip(), """\
Are you sure you want to attach disk 'snaptest' to vm 'server01'? [y/N]:\
""")
        self.assertEqual(result.exit_code, 0)

    def test_attach_forced(self):
        args = ['snaptest', 'server01', '-f']
        result = self.invoke_with_exceptions(disk.attach, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Attaching your disk(s).
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_must_detach(self):
        args = ['data', 'vm1426759833']
        result = self.invoke_with_exceptions(disk.attach, args,
                                             input='y\n')
        self.assertEqual(result.output.strip(), """\
Are you sure you want to attach disk 'data' to vm 'vm1426759833'? [y/N]: y\
\nThis disk is still attached
Are you sure you want to detach data? [y/N]:""")
        self.assertEqual(result.exit_code, 0)

    def test_attach_must_detach_forced(self):
        args = ['data', 'vm1426759833', '-f']
        result = self.invoke_with_exceptions(disk.attach, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The disk is still attached to the vm 152967.
Will detach it.
Detaching your disk.
\rProgress: [###] 100.00%  00:00:00  \
\nAttaching your disk(s).
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_forced_background(self):
        args = ['snaptest', 'server01', '-f', '--bg']
        result = self.invoke_with_exceptions(disk.attach, args)
        self.assertEqual(result.output.strip(), "{'id': 200, 'step': 'WAIT'}")

        self.assertEqual(result.exit_code, 0)

    def test_update_name(self):
        args = ['data', '--name', 'data2']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_kernel(self):
        args = ['data', '--kernel', '3.12-x86_64 (hvm)']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_cmdline(self):
        args = ['data', '--cmdline',
                'root=/dev/xvda1 loglevel=4 console=hvc0 nosep ro']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_snapshotprofile(self):
        args = ['data', '--snapshotprofile', '7']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_snapshotprofile_delete(self):
        args = ['data', '--delete-snapshotprofile']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_size(self):
        args = ['data', '--size', '5G']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your disk.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.api_calls['hosting.disk.update'][0][1],
                         {'size': 5120})

    def test_update_background(self):
        args = ['data', '--name', 'data2', '--bg']
        result = self.invoke_with_exceptions(disk.update, args)
        self.assertEqual(result.output.strip(), "{'id': 200, 'step': 'WAIT'}")

        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        result = self.invoke_with_exceptions(disk.delete, ['data'])
        self.assertEqual(result.output.strip(),
                         "Are you sure you want to delete disk 'data'? [y/N]:")
        self.assertEqual(result.exit_code, 0)

    def test_delete_multiple(self):
        result = self.invoke_with_exceptions(disk.delete, ['data', 'snaptest'])
        self.assertEqual(result.output.strip(), """\
Are you sure you want to delete disk 'data, snaptest'? [y/N]:""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_attached(self):
        result = self.invoke_with_exceptions(disk.delete, ['data', '-f'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The disk is still attached to the vm 152967.
Will detach it.
Detaching your disk(s).
\rProgress: [###] 100.00%  00:00:00  \
\nDeleting your disk.
\rProgress: [###] 100.00%  00:00:00""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_force(self):
        result = self.invoke_with_exceptions(disk.delete, ['snaptest', '-f'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Deleting your disk.
\rProgress: [###] 100.00%  00:00:00""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_background(self):
        args = ['snaptest', '-f', '--bg']
        result = self.invoke_with_exceptions(disk.delete, args)
        self.assertEqual(result.output.strip(), """\
id        : 200
step      : WAIT""")
        self.assertEqual(result.exit_code, 0)

    def test_rollback(self):
        args = ['snaptest']
        result = self.invoke_with_exceptions(disk.rollback, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Disk rollback in progress.
\rProgress: [###] 100.00%  00:00:00""")
        self.assertEqual(result.exit_code, 0)

    def test_rollback_background(self):
        args = ['snaptest', '--bg']
        result = self.invoke_with_exceptions(disk.rollback, args)
        self.assertEqual(result.output.strip(), "{'id': 200, 'step': 'WAIT'}")
        self.assertEqual(result.exit_code, 0)
