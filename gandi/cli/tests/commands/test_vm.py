# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import vm


class VmTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(vm.list, [])

        self.assertEqual(result.output, """hostname  : vm1426759833
state     : running
----------
hostname  : server01
state     : running
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):

        result = self.runner.invoke(vm.list, ['--id'])

        self.assertEqual(result.output, """hostname  : vm1426759833
state     : running
id        : 152966
----------
hostname  : server01
state     : running
id        : 152967
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_state(self):

        result = self.runner.invoke(vm.list, ['--state', 'halted'])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_datacenter(self):

        result = self.runner.invoke(vm.list, ['--datacenter', 'FR'])

        self.assertEqual(result.output, """hostname  : server01
state     : running
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_ko_resource(self):

        result = self.runner.invoke(vm.info, [])
        self.assertEqual(result.exit_code, 2)

    def test_info_ok_one_resource(self):

        result = self.runner.invoke(vm.info, ['server01'])

        self.assertEqual(result.output, """hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR
----------
bandwidth     : 102400.0
ip4           : 95.142.160.181
ip6           : 2001:4b98:dc0:47:216:3eff:feb2:3862

label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_server01
size          : 3072
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_ok_multiple_resources(self):

        result = self.runner.invoke(vm.info, ['server01', 'vm1426759833'])

        self.assertEqual(result.output, """hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR
----------
bandwidth     : 102400.0
ip4           : 95.142.160.181
ip6           : 2001:4b98:dc0:47:216:3eff:feb2:3862

label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_server01
size          : 3072
----------
hostname      : vm1426759833
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : LU
----------
bandwidth     : 102400.0
ip6           : 2001:4b98:dc2:43:216:3eff:fece:e25f

label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_1426759833
size          : 3072
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_stat(self):

        result = self.runner.invoke(vm.info, ['server01', '--stat'])

        expected = u"""hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR
----------
bandwidth     : 102400.0
ip4           : 95.142.160.181
ip6           : 2001:4b98:dc0:47:216:3eff:feb2:3862

label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_server01
size          : 3072

vm network stats
in            :    ▁▁ ▂▁ ▁▁▁▂▂▁▁     ▉▃▁
out           :    ▁▃ ▉▂ ▆▆▁▃▄▁▁ ▁  ▁▉▅▇
disk network stats
read          :     ▁ ▁▁ ▁  ▉        ▁▃▁
write         :     ▁    ▁  ▂        ▉▁▁
"""
        self.assertEqual(result.output, expected)
        self.assertEqual(result.exit_code, 0)
