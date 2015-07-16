# -*- coding: utf-8 -*-
import re

from .base import CommandTestCase
from gandi.cli.commands import ip
from gandi.cli.core.base import GandiContextHelper


class IpTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(ip.list, [])

        self.assertEqual(result.output, """\
ip         : 95.142.160.181
state      : created
type       : public
datacenter : FR
----------
ip         : 2001:4b98:dc2:43:216:3eff:fece:e25f
state      : created
type       : private
vlan       : pouet
datacenter : LU
----------
ip         : 2001:4b98:dc0:47:216:3eff:feb2:3862
state      : created
type       : public
datacenter : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_details(self):
        args = ['--id', '--version', '--vm', '--reverse']
        result = self.invoke_with_exceptions(ip.list, args)

        self.assertEqual(result.output, """\
ip         : 95.142.160.181
state      : created
id         : 203968
version    : 4
reverse    : xvm-160-181.dc0.ghst.net
type       : public
vm         : server01
datacenter : FR
----------
ip         : 2001:4b98:dc2:43:216:3eff:fece:e25f
state      : created
id         : 204557
version    : 6
reverse    : xvm6-dc2-fece-e25f.ghst.net
type       : private
vlan       : pouet
datacenter : LU
----------
ip         : 2001:4b98:dc0:47:216:3eff:feb2:3862
state      : created
id         : 204558
version    : 6
reverse    : xvm6-dc0-feb2-3862.ghst.net
type       : public
vm         : server01
datacenter : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_attached(self):

        result = self.invoke_with_exceptions(ip.list, ['--attached'])

        self.assertEqual(result.output, """\
ip         : 95.142.160.181
state      : created
type       : public
datacenter : FR
----------
ip         : 2001:4b98:dc0:47:216:3eff:feb2:3862
state      : created
type       : public
datacenter : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_detached(self):

        result = self.invoke_with_exceptions(ip.list, ['--detached'])

        self.assertEqual(result.output, """\
ip         : 2001:4b98:dc2:43:216:3eff:fece:e25f
state      : created
type       : private
vlan       : pouet
datacenter : LU
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_type(self):

        result = self.invoke_with_exceptions(ip.list, ['--type', 'private'])

        self.assertEqual(result.output, """\
ip         : 2001:4b98:dc2:43:216:3eff:fece:e25f
state      : created
type       : private
vlan       : pouet
datacenter : LU
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_datacenter(self):

        result = self.invoke_with_exceptions(ip.list, ['--datacenter', 'FR'])

        self.assertEqual(result.output, """\
ip         : 95.142.160.181
state      : created
type       : public
datacenter : FR
----------
ip         : 2001:4b98:dc0:47:216:3eff:feb2:3862
state      : created
type       : public
datacenter : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_vlan(self):

        result = self.invoke_with_exceptions(ip.list, ['--vlan', 'pouet'])

        self.assertEqual(result.output, """\
ip         : 2001:4b98:dc2:43:216:3eff:fece:e25f
state      : created
type       : private
vlan       : pouet
datacenter : LU
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_attached_detached(self):
        args = ['--detached', '--attached']
        result = self.invoke_with_exceptions(ip.list, args)

        self.assertEqual(result.output, """\
You can't set --attached and --detached at the same time.
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['95.142.160.181']
        result = self.invoke_with_exceptions(ip.info, args)

        self.assertEqual(result.output, """\
ip         : 95.142.160.181
state      : created
reverse    : xvm-160-181.dc0.ghst.net
type       : public
vm         : server01
datacenter : FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_update_ko(self):
        args = ['95.142.160.181']
        result = self.invoke_with_exceptions(ip.update, args)

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_update_reverse(self):
        args = ['95.142.160.181', '--reverse', 'plop.bloup.com']
        result = self.invoke_with_exceptions(ip.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your IP
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_ko(self):
        args = ['395.142.160.181', 'vm1426759833']
        result = self.invoke_with_exceptions(ip.attach, args)

        self.assertTrue("Can't find this ip 395.142.160.181" in result.output)
        self.assertEqual(result.exit_code, 2)

    def test_attach_already(self):
        args = ['95.142.160.181', 'server01']
        result = self.invoke_with_exceptions(ip.attach, args, input='y\n')

        self.assertEqual(result.output, """\
This ip is already attached to this vm.
""")
        self.assertEqual(result.exit_code, 0)

    def test_attach(self):
        args = ['95.142.160.181', 'vm1426759833']
        result = self.invoke_with_exceptions(ip.attach, args, input='y\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure you want to detach 95.142.160.181 from vm 152967 [y/N]: y
The iface is still attached to the vm 152967.
Will detach it.
\rProgress: [###] 100.00%  00:00:00  \
\n\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_force(self):
        args = ['95.142.160.181', 'vm1426759833', '--force']
        result = self.invoke_with_exceptions(ip.attach, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The iface is still attached to the vm 152967.
Will detach it.
\rProgress: [###] 100.00%  00:00:00  \
\n\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_refuse(self):
        args = ['95.142.160.181', 'vm1426759833']
        result = self.invoke_with_exceptions(ip.attach, args, input='N\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure you want to detach 95.142.160.181 from vm 152967 [y/N]: N""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_background(self):
        args = ['95.142.160.181', 'vm1426759833', '--force', '--bg']
        result = self.invoke_with_exceptions(ip.attach, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
The iface is still attached to the vm 152967.
Will detach it.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_create_default(self):
        args = []
        result = self.invoke_with_exceptions(ip.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your iface.
\rProgress: [###] 100.00%  00:00:00  \
\nYour iface has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.iface.create'][0][0]
        self.assertEqual(params['datacenter_id'], 3)
        self.assertEqual(params['bandwidth'], 102400)
        self.assertEqual(params['ip_version'], 4)

    def test_create_params(self):
        args = ['--datacenter', 'FR', '--bandwidth', '51200',
                '--ip-version', '6']
        result = self.invoke_with_exceptions(ip.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your iface.
\rProgress: [###] 100.00%  00:00:00  \
\nYour iface has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.iface.create'][0][0]
        self.assertEqual(params['datacenter_id'], 1)
        self.assertEqual(params['bandwidth'], 51200)
        self.assertEqual(params['ip_version'], 6)

    def test_create_params_vlan_ko(self):
        args = ['--datacenter', 'FR', '--bandwidth', '51200',
                '--ip-version', '6', '--vlan', 'pouet']
        result = self.invoke_with_exceptions(ip.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
You must have an --ip-version to 4 when having a vlan.""")
        self.assertEqual(result.exit_code, 0)

    def test_create_params_vlan_ok(self):
        args = ['--datacenter', 'FR', '--bandwidth', '51200',
                '--ip-version', '4', '--vlan', 'pouet']
        result = self.invoke_with_exceptions(ip.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your iface.
\rProgress: [###] 100.00%  00:00:00  \
\nYour iface has been created.""")
        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.iface.create'][0][0]
        self.assertEqual(params['datacenter_id'], 1)
        self.assertEqual(params['bandwidth'], 51200)
        self.assertEqual(params['ip_version'], 4)
        self.assertEqual(params['vlan'], 717)
