# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import socket

from ..compat import mock
from ..fixtures.mocks import MockObject
from .base import CommandTestCase
from gandi.cli.commands import vm
from gandi.cli.core.base import GandiContextHelper


class VmTestCase(CommandTestCase):

    mocks = [('gandi.cli.core.base.GandiModule.exec_output',
              MockObject.exec_output)]

    def test_list(self):

        result = self.invoke_with_exceptions(vm.list, [])

        self.assertEqual(result.output, """hostname  : vm1426759833
state     : running
----------
hostname  : server01
state     : running
----------
hostname  : server02
state     : halted
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):

        result = self.invoke_with_exceptions(vm.list, ['--id'])

        self.assertEqual(result.output, """hostname  : vm1426759833
state     : running
id        : 152966
----------
hostname  : server01
state     : running
id        : 152967
----------
hostname  : server02
state     : halted
id        : 152968
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_state(self):

        result = self.invoke_with_exceptions(vm.list, ['--state', 'halted'])

        self.assertEqual(result.output, """hostname  : server02
state     : halted
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_filter_datacenter(self):

        result = self.invoke_with_exceptions(vm.list, ['--datacenter', 'FR'])

        self.assertEqual(result.output, """hostname  : server01
state     : running
----------
hostname  : server02
state     : halted
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_ko_resource(self):

        result = self.invoke_with_exceptions(vm.info, [])
        self.assertEqual(result.exit_code, 2)

    def test_info_ok_one_resource(self):

        result = self.invoke_with_exceptions(vm.info, ['server01'])

        self.assertEqual(result.output, """hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR-SD2
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
        args = ['server01', 'vm1426759833']
        result = self.invoke_with_exceptions(vm.info, args)

        self.assertEqual(result.output, """hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR-SD2
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
datacenter    : LU-BI1
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

        result = self.invoke_with_exceptions(vm.info, ['server01', '--stat'])

        expected = u"""hostname      : server01
state         : running
cores         : 1
memory        : 256
console       :
datacenter    : FR-SD2
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

    def test_datacenters(self):

        result = self.invoke_with_exceptions(vm.datacenters, [])

        self.assertEqual(result.output, """\
iso       : FR
name      : Equinix Paris
country   : France
dc_code   : FR-SD2
closing on: 25/12/2017
----------
iso       : US
name      : Level3 Baltimore
country   : United States of America
dc_code   : US-BA1
closing on: 25/12/2016
closed for: vm, paas
----------
iso       : LU
name      : Bissen
country   : Luxembourg
dc_code   : LU-BI1
----------
iso       : FR
name      : France, Paris
country   : France
dc_code   : FR-SD3
closed for: paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_datacenters_id(self):

        result = self.invoke_with_exceptions(vm.datacenters, ['--id'])

        self.assertEqual(result.output, """\
iso       : FR
name      : Equinix Paris
country   : France
dc_code   : FR-SD2
id        : 1
closing on: 25/12/2017
----------
iso       : US
name      : Level3 Baltimore
country   : United States of America
dc_code   : US-BA1
id        : 2
closing on: 25/12/2016
closed for: vm, paas
----------
iso       : LU
name      : Bissen
country   : Luxembourg
dc_code   : LU-BI1
id        : 3
----------
iso       : FR
name      : France, Paris
country   : France
dc_code   : FR-SD3
id        : 4
closed for: paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels(self):

        result = self.invoke_with_exceptions(vm.kernels, [])

        linux_hvm_out = """\
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
"""
        linux_out_dc1 = """\
flavor        : linux
version       : 2.6.18 (deprecated)
version       : 2.6.27-compat-sysfs (deprecated)
version       : 2.6.32
version       : 2.6.27 (deprecated)
version       : 2.6.32-x86_64
version       : 2.6.36 (deprecated)
version       : 2.6.32-x86_64-grsec
version       : 2.6.36-x86_64 (deprecated)
version       : 3.2-i386
version       : 3.2-x86_64
version       : 3.2-x86_64-grsec
version       : 3.10-x86_64
version       : 3.10-i386
"""
        linux_out_dc2 = """\
flavor        : linux
version       : 2.6.18 (deprecated)
version       : 2.6.27-compat-sysfs (deprecated)
version       : 2.6.32
version       : 2.6.27 (deprecated)
version       : 2.6.32-x86_64
version       : 2.6.36 (deprecated)
version       : 2.6.32-x86_64-grsec
version       : 2.6.36-x86_64 (deprecated)
version       : 3.2-i386
version       : 3.2-x86_64
version       : 3.2-x86_64-grsec
version       : 3.10-x86_64
version       : 3.10-i386
"""
        linux_out_dc3 = """\
flavor        : linux
version       : 2.6.32
version       : 2.6.27 (deprecated)
version       : 2.6.32-x86_64
version       : 2.6.32-x86_64-grsec
version       : 3.2-i386
version       : 3.2-x86_64
version       : 3.2-x86_64-grsec
version       : 3.10-x86_64
version       : 3.10-i386
"""
        self.assertTrue(linux_hvm_out in result.output)
        self.assertTrue(linux_out_dc1 in result.output)
        self.assertTrue(linux_out_dc2 in result.output)
        self.assertTrue(linux_out_dc3 in result.output)
        self.assertTrue('datacenter    : Bissen' in result.output)
        self.assertTrue('datacenter    : Level3 Baltimore' in result.output)
        self.assertTrue('datacenter    : Equinix Paris' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_kernels_match(self):

        result = self.invoke_with_exceptions(vm.kernels, ['3.10'])

        linux_out = """\
----------
flavor        : linux
version       : 3.10-x86_64
version       : 3.10-i386
"""
        self.assertTrue(linux_out in result.output)
        self.assertTrue('datacenter    : Bissen' in result.output)
        self.assertTrue('datacenter    : Level3 Baltimore' in result.output)
        self.assertTrue('datacenter    : Equinix Paris' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_kernels_flavor(self):
        args = ['--flavor', 'linux-hvm']
        result = self.invoke_with_exceptions(vm.kernels, args)

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw


datacenter    : Level3 Baltimore
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw


datacenter    : Bissen
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw


datacenter    : France, Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_datacenter(self):
        args = ['--datacenter', 'LU']
        result = self.invoke_with_exceptions(vm.kernels, args)

        linux_out = """\
flavor        : linux
version       : 2.6.32
version       : 2.6.27 (deprecated)
version       : 2.6.32-x86_64
version       : 2.6.32-x86_64-grsec
version       : 3.2-i386
version       : 3.2-x86_64
version       : 3.2-x86_64-grsec
version       : 3.10-x86_64
version       : 3.10-i386
"""
        linux_hvm_out = """\
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
"""
        self.assertTrue(linux_out in result.output)
        self.assertTrue(linux_hvm_out in result.output)
        self.assertTrue('datacenter    : Bissen' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_kernels_vm(self):

        result = self.invoke_with_exceptions(vm.kernels, ['--vm', 'server01'])

        linux_out = """\
flavor        : linux
version       : 2.6.18 (deprecated)
version       : 2.6.27-compat-sysfs (deprecated)
version       : 2.6.32
version       : 2.6.27 (deprecated)
version       : 2.6.32-x86_64
version       : 2.6.36 (deprecated)
version       : 2.6.32-x86_64-grsec
version       : 2.6.36-x86_64 (deprecated)
version       : 3.2-i386
version       : 3.2-x86_64
version       : 3.2-x86_64-grsec
version       : 3.10-x86_64
version       : 3.10-i386
"""
        linux_hvm_out = """\
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
"""
        self.assertTrue(linux_out in result.output)
        self.assertTrue(linux_hvm_out in result.output)
        self.assertTrue('datacenter    : Equinix Paris' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_kernels_all(self):

        args = ['--vm', 'server01', '--datacenter', 'FR',
                '--flavor', 'linux-hvm', '3.12']
        result = self.invoke_with_exceptions(vm.kernels, args)

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
""")
        self.assertEqual(result.exit_code, 0)

    def test_images(self):
        self.maxDiff = None
        result = self.invoke_with_exceptions(vm.images, [])

        self.assertEqual(result.output, """\
label         : Fedora 17 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 527489
datacenter    : LU-BI1
----------
label         : Fedora 17 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 527490
datacenter    : LU-BI1
----------
label         : OpenSUSE 12.2 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 527491
datacenter    : LU-BI1
----------
label         : OpenSUSE 12.2 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 527494
datacenter    : LU-BI1
----------
label         : CentOS 5 32 bits
os_arch       : x86-32
kernel_version: 2.6.32
disk_id       : 726224
datacenter    : LU-BI1
----------
label         : CentOS 5 64 bits
os_arch       : x86-64
kernel_version: 2.6.32-x86_64
disk_id       : 726225
datacenter    : LU-BI1
----------
label         : ArchLinux 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 726230
datacenter    : LU-BI1
----------
label         : ArchLinux 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 726233
datacenter    : LU-BI1
----------
label         : Debian 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 1401491
datacenter    : US-BA1
----------
label         : Debian 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 1349810
datacenter    : FR-SD2
----------
label         : Debian 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 1401327
datacenter    : LU-BI1
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315704
datacenter    : FR-SD2
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315992
datacenter    : US-BA1
----------
label         : Debian 8
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316070
datacenter    : FR-SD2
----------
label         : Debian 8
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316070
datacenter    : LU-BI1
----------
label         : Debian 8
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316070
datacenter    : FR-SD3
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316076
datacenter    : LU-BI1
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315748
datacenter    : FR-SD2
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316144
datacenter    : US-BA1
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316160
datacenter    : LU-BI1
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 2876292
datacenter    : FR-SD2
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 4744388
datacenter    : US-BA1
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 4744392
datacenter    : LU-BI1
----------
label         : Debian 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 1401492
datacenter    : FR-SD3
----------
label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_1426759833
datacenter    : LU-BI1
----------
label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_server01
datacenter    : FR-SD2
----------
label         :
kernel_version:
name          : data
datacenter    : FR-SD2
----------
label         : Debian 7 64 bits
kernel_version: 3.2-x86_64
name          : snaptest
datacenter    : FR-SD2
""")
        self.assertEqual(result.exit_code, 0)

    def test_images_all(self):

        args = ['Ubuntu 14.04', '--datacenter', 'LU']
        result = self.invoke_with_exceptions(vm.images, args)

        self.assertEqual(result.output, """\
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316160
datacenter    : LU-BI1
""")
        self.assertEqual(result.exit_code, 0)

    def test_stop_one(self):
        result = self.invoke_with_exceptions(vm.stop, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_stop_multiple(self):
        args = ['server01', 'vm1426759833']
        result = self.invoke_with_exceptions(vm.stop, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_stop_background(self):
        result = self.invoke_with_exceptions(vm.stop, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_start_one(self):
        result = self.invoke_with_exceptions(vm.start, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Starting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_start_multiple(self):
        args = ['server01', 'vm1426759833']
        result = self.invoke_with_exceptions(vm.start, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Starting your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_start_background(self):
        result = self.invoke_with_exceptions(vm.start, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_reboot_one(self):
        result = self.invoke_with_exceptions(vm.reboot, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Rebooting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_reboot_multiple(self):
        args = ['server01', 'vm1426759833']
        result = self.invoke_with_exceptions(vm.reboot, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Rebooting your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_reboot_background(self):
        result = self.invoke_with_exceptions(vm.reboot, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_prompt(self):
        result = self.invoke_with_exceptions(vm.delete, ['server01'])
        self.assertEqual(result.output.strip(), """\
Are you sure to delete Virtual Machine 'server01'? [y/N]:""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_one(self):
        result = self.invoke_with_exceptions(vm.delete, ['server01', '-f'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00  \n\
Deleting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_multiple(self):
        args = ['server01', 'vm1426759833', '-f']
        result = self.invoke_with_exceptions(vm.delete, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00  \n\
Stopping your Virtual Machine(s) 'vm1426759833'.
\rProgress: [###] 100.00%  00:00:00  \n\
Deleting your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_unknown(self):
        result = self.invoke_with_exceptions(vm.delete, ['server100'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Sorry virtual machine server100 does not exist
Please use one of the following: ['vm1426759833', 'server01', \
'server02', '152966', '152967', '152968']""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_background_ko(self):
        args = ['server01', '-f', '--bg']
        result = self.invoke_with_exceptions(vm.delete, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Virtual machine not stopped, background option disabled
Stopping your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00  \n\
Deleting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_background_ok(self):
        args = ['server02', '-f', '--bg']
        result = self.invoke_with_exceptions(vm.delete, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
id        : 200
step      : WAIT""")

        self.assertEqual(result.exit_code, 0)

    def test_update_ok(self):
        args = ['server01', '--memory', '1024', '--cores', '4']
        result = self.invoke_with_exceptions(vm.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your Virtual Machine server01.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_memory(self):
        args = ['server01', '--memory', '10240', '--cores', '4']
        result = self.invoke_with_exceptions(vm.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
memory update must be done offline.
reboot machine server01? [y/N]:""")

        self.assertEqual(result.exit_code, 0)

    def test_update_memory_reboot(self):
        args = ['server01', '--memory', '10240', '--cores', '4', '--reboot']
        result = self.invoke_with_exceptions(vm.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your Virtual Machine server01.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_background(self):
        args = ['server01', '--memory', '1024', '--cores', '4', '--bg']
        result = self.invoke_with_exceptions(vm.update, args)
        self.assertEqual(result.output, """\
{'id': 200, 'step': 'WAIT'}
""")
        self.assertEqual(result.exit_code, 0)

    def test_update_password(self):
        args = ['server01', '--password']
        result = self.invoke_with_exceptions(vm.update, args,
                                             input='plokiploki\nplokiploki\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \nUpdating your Virtual Machine server01.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_console(self):
        args = ['server01', '--console']
        result = self.invoke_with_exceptions(vm.update, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your Virtual Machine server01.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_console(self):
        args = ['server01']
        result = self.invoke_with_exceptions(vm.console, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
/!\\ Please be aware that if you didn\'t provide a password during creation, \
console service will be unavailable.
/!\\ You can use "gandi vm update" command to set a password.
/!\\ Use ~. ssh escape key to exit.
Updating your Virtual Machine server01.
\rProgress: [###] 100.00%  00:00:00  \n\
ssh 95.142.160.181@console.gandi.net""")

        self.assertEqual(result.exit_code, 0)

    def test_ssh(self):
        args = ['admin@server01']
        result = self.invoke_with_exceptions(vm.ssh, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Requesting access using: ssh admin@95.142.160.181 ...
ssh admin@95.142.160.181""")

        self.assertEqual(result.exit_code, 0)

    def test_ssh_wipe_key(self):
        args = ['admin@server01', '--wipe-key']
        with mock.patch('gandi.cli.modules.iaas.open',
                        create=True) as mock_open:
            mock_open.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(vm.ssh, args)
            self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                    result.output.strip()), """\
Wiping old key and learning the new one
ssh-keygen -R "95.142.160.181"
Requesting access using: ssh admin@95.142.160.181 ...
ssh admin@95.142.160.181""")

            self.assertEqual(result.exit_code, 0)

    def test_ssh_wait(self):
        args = ['server01', '--wait']
        with mock.patch('gandi.cli.modules.iaas.socket',
                        create=True) as mock_socket:
            mock_socket.return_value = mock.MagicMock(name='socket',
                                                      spec=socket.socket)

            result = self.invoke_with_exceptions(vm.ssh, args)
            self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                    result.output.strip()), """\
Waiting for the vm to come online
Requesting access using: ssh root@95.142.160.181 ...
ssh root@95.142.160.181""")

            self.assertEqual(result.exit_code, 0)

    def test_ssh_login(self):
        args = ['server01', '--login', 'joe']
        result = self.invoke_with_exceptions(vm.ssh, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Requesting access using: ssh joe@95.142.160.181 ...
ssh joe@95.142.160.181""")

        self.assertEqual(result.exit_code, 0)

    def test_ssh_identity(self):
        args = ['admin@server01', '-i', 'key.pub']
        result = self.invoke_with_exceptions(vm.ssh, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Requesting access using: ssh -i key.pub admin@95.142.160.181 ...
ssh -i key.pub admin@95.142.160.181""")

        self.assertEqual(result.exit_code, 0)

    def test_ssh_args(self):
        args = ['server01', 'sudo reboot']
        result = self.invoke_with_exceptions(vm.ssh, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Requesting access using: ssh root@95.142.160.181 sudo reboot ...
ssh root@95.142.160.181 sudo reboot""")

        self.assertEqual(result.exit_code, 0)

    def test_create_default_hostname_ok(self):
        args = ['--hostname', 'server500']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n* root user will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: server500, datacenter: FR-SD3
Creating your Virtual Machine server500.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine server500 has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_default_ok(self):
        args = []
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
password: \nRepeat for confirmation: \n* root user will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: vm, datacenter: FR-SD3
Creating your Virtual Machine vm.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine vm has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_ip_not_vlan_ko(self):
        args = ['--hostname', 'server500', '--ip', '10.50.10.10']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n\
--ip can't be used without --vlan.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_vlan_ip_ok(self):
        args = ['--hostname', 'server400', '--vlan', 'vlantest',
                '--ip', '10.50.10.10']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n* Private only ip vm (can't enable \
emergency web console access).
* root user will be created.
Creating your iface.
\rProgress: [###] 100.00%  00:00:00  \n\
Your iface has been created with the following IP addresses:
ip4:\t10.50.10.10
* Configuration used: 1 cores, 256Mb memory, ip private, image Debian 8\
, hostname: server400, datacenter: FR-SD3
Creating your Virtual Machine server400.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine server400 has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_login_ok(self):
        args = ['--login', 'administrator']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
password: \nRepeat for confirmation: \n\
* root and administrator users will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: vm, datacenter: FR-SD3
Creating your Virtual Machine vm.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine vm has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_background_ok(self):
        args = ['--hostname', 'server500', '--background']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n* root user will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: server500, datacenter: FR-SD3
* IAAS backend is now creating your VM and its associated resources in the \
background.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_sshkey_ok(self):
        args = ['--sshkey', 'mysecretkey']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper())
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
* root user will be created.
* SSH key authorization will be used.
* No password supplied for vm (required to enable emergency web console \
access).
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: vm, datacenter: FR-SD3
Creating your Virtual Machine vm.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine vm has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_dc_code_ok(self):
        args = ['--datacenter', 'FR-SD3']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
password: \nRepeat for confirmation: \n* root user will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: vm, datacenter: FR-SD3
Creating your Virtual Machine vm.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine vm has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_datacenter_closed(self):
        args = ['--datacenter', 'US-BA1']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
Error: /!\ Datacenter US-BA1 is closed, please choose another datacenter.""")

        self.assertEqual(result.exit_code, 1)

    def test_create_datacenter_limited(self):
        args = ['--datacenter', 'FR-SD2']
        result = self.invoke_with_exceptions(vm.create, args,
                                             obj=GandiContextHelper(),
                                             input='plokiploki\nplokiploki\n')
        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'vm\d+', 'vm', output), """\
/!\ Datacenter FR-SD2 will be closed on 25/12/2017, please consider \
using another datacenter.
password: \nRepeat for confirmation: \n\
* root user will be created.
* Configuration used: 1 cores, 256Mb memory, ip v6, image Debian 8\
, hostname: vm, datacenter: FR-SD2
Creating your Virtual Machine vm.
\rProgress: [###] 100.00%  00:00:00  \n\
Your Virtual Machine vm has been created.""")

        self.assertEqual(result.exit_code, 0)
