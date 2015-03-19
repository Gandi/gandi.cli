# -*- coding: utf-8 -*-
import re

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

    def test_datacenters(self):

        result = self.runner.invoke(vm.datacenters, [])

        self.assertEqual(result.output, """\
iso       : FR
name      : Equinix Paris
country   : France
----------
iso       : US
name      : Level3 Baltimore
country   : United States of America
----------
iso       : LU
name      : Bissen
country   : Luxembourg
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels(self):

        result = self.runner.invoke(vm.kernels, [])

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
----------
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


datacenter    : Level3 Baltimore
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
----------
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


datacenter    : Bissen
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
----------
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
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_match(self):

        result = self.runner.invoke(vm.kernels, ['3.10'])

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
----------
flavor        : linux
version       : 3.10-x86_64
version       : 3.10-i386


datacenter    : Level3 Baltimore
----------
flavor        : linux-hvm
----------
flavor        : linux
version       : 3.10-x86_64
version       : 3.10-i386


datacenter    : Bissen
----------
flavor        : linux-hvm
----------
flavor        : linux
version       : 3.10-x86_64
version       : 3.10-i386
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_flavor(self):

        result = self.runner.invoke(vm.kernels, ['--flavor', 'linux-hvm'])

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
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_datacenter(self):

        result = self.runner.invoke(vm.kernels, ['--datacenter', 'LU'])

        self.assertEqual(result.output, """\
datacenter    : Bissen
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
----------
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
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_vm(self):

        result = self.runner.invoke(vm.kernels, ['--vm', 'server01'])

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
version       : grub
version       : raw
----------
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
""")
        self.assertEqual(result.exit_code, 0)

    def test_kernels_all(self):

        args = ['--vm', 'server01', '--datacenter', 'FR',
                '--flavor', 'linux-hvm', '3.12']
        result = self.runner.invoke(vm.kernels, args)

        self.assertEqual(result.output, """\
datacenter    : Equinix Paris
----------
flavor        : linux-hvm
version       : 3.12-x86_64 (hvm)
""")
        self.assertEqual(result.exit_code, 0)

    def test_images(self):

        result = self.runner.invoke(vm.images, [])

        self.assertEqual(result.output, """\
label         : Fedora 17 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 527489
datacenter    : LU
----------
label         : Fedora 17 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 527490
datacenter    : LU
----------
label         : OpenSUSE 12.2 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 527491
datacenter    : LU
----------
label         : OpenSUSE 12.2 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 527494
datacenter    : LU
----------
label         : CentOS 5 32 bits
os_arch       : x86-32
kernel_version: 2.6.32
disk_id       : 726224
datacenter    : LU
----------
label         : CentOS 5 64 bits
os_arch       : x86-64
kernel_version: 2.6.32-x86_64
disk_id       : 726225
datacenter    : LU
----------
label         : ArchLinux 32 bits
os_arch       : x86-32
kernel_version: 3.2-i386
disk_id       : 726230
datacenter    : LU
----------
label         : ArchLinux 64 bits
os_arch       : x86-64
kernel_version: 3.2-x86_64
disk_id       : 726233
datacenter    : LU
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315704
datacenter    : FR
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315992
datacenter    : US
----------
label         : Debian 8 (testing) 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316076
datacenter    : LU
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3315748
datacenter    : FR
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316144
datacenter    : US
----------
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316160
datacenter    : LU
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 2876292
datacenter    : FR
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 4744388
datacenter    : US
----------
label         : CentOS 7 64 bits (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 4744392
datacenter    : LU
----------
label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_1426759833
datacenter    : LU
----------
label         : Debian 7 64 bits (HVM)
kernel_version: 3.12-x86_64 (hvm)
name          : sys_server01
datacenter    : FR
----------
label         :
kernel_version:
name          : data
datacenter    : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_images_all(self):

        args = ['Ubuntu 14.04', '--datacenter', 'LU']
        result = self.runner.invoke(vm.images, args)

        self.assertEqual(result.output, """\
label         : Ubuntu 14.04 64 bits LTS (HVM)
os_arch       : x86-64
kernel_version: 3.12-x86_64 (hvm)
disk_id       : 3316160
datacenter    : LU
""")
        self.assertEqual(result.exit_code, 0)

    def test_stop_one(self):
        result = self.runner.invoke(vm.stop, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_stop_multiple(self):
        result = self.runner.invoke(vm.stop, ['server01', 'vm1426759833'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Stopping your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_stop_background(self):
        result = self.runner.invoke(vm.stop, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_start_one(self):
        result = self.runner.invoke(vm.start, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Starting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_start_multiple(self):
        result = self.runner.invoke(vm.start, ['server01', 'vm1426759833'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Starting your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_start_background(self):
        result = self.runner.invoke(vm.start, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_reboot_one(self):
        result = self.runner.invoke(vm.reboot, ['server01'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Rebooting your Virtual Machine(s) 'server01'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_reboot_multiple(self):
        result = self.runner.invoke(vm.reboot, ['server01', 'vm1426759833'])
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Rebooting your Virtual Machine(s) 'server01, vm1426759833'.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_reboot_background(self):
        result = self.runner.invoke(vm.reboot, ['server01', '--bg'])
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)
