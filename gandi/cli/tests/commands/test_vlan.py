# -*- coding: utf-8 -*-

import re

from .base import CommandTestCase
from gandi.cli.commands import vlan
from gandi.cli.core.base import GandiContextHelper


class VlanTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(vlan.list, [])

        self.assertEqual(result.output, """\
name      : vlantest
state     : created
datacenter: FR-SD2
----------
name      : pouet
state     : created
datacenter: FR-SD2
----------
name      : intranet
state     : created
datacenter: FR-SD3
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filters(self):
        args = ['--id', '--subnet', '--gateway']
        result = self.invoke_with_exceptions(vlan.list, args)

        self.assertEqual(result.output, """\
name      : vlantest
state     : created
id        : 123
subnet    : 10.7.13.0/24
gateway   : 10.7.13.254
datacenter: FR-SD2
----------
name      : pouet
state     : created
id        : 717
subnet    : 192.168.232.0/24
gateway   : 192.168.232.254
datacenter: FR-SD2
----------
name      : intranet
state     : created
id        : 999
subnet    : 10.7.242.0/24
gateway   : 10.7.242.254
datacenter: FR-SD3
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_datacenter(self):
        args = ['--id', '--subnet', '--gateway', '--datacenter', 'FR-SD3']
        result = self.invoke_with_exceptions(vlan.list, args)

        self.assertEqual(result.output, """\
name      : intranet
state     : created
id        : 999
subnet    : 10.7.242.0/24
gateway   : 10.7.242.254
datacenter: FR-SD3
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['vlantest']
        result = self.invoke_with_exceptions(vlan.info, args)

        self.assertEqual(result.output, """\
name       : vlantest
state      : created
subnet     : 10.7.13.0/24
gateway    : 10.7.13.254
datacenter : FR-SD2
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_ip(self):
        args = ['pouet', '--ip']
        result = self.invoke_with_exceptions(vlan.info, args)

        self.assertEqual(result.output, """\
name       : pouet
state      : created
subnet     : 192.168.232.0/24
gateway    : 192.168.232.254 don't exists
datacenter : FR-SD2
----------
bandwidth  : 102400.0
vm         : server02
ip         : 192.168.232.252
----------
bandwidth  : 204800.0
vm         : server02
ip         : 192.168.232.253
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        args = ['intranet']
        result = self.invoke_with_exceptions(vlan.delete, args, input='y\n',
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete vlan 'intranet'? [y/N]: y
Deleting your vlan.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_force(self):
        args = ['intranet', '--force']
        result = self.invoke_with_exceptions(vlan.delete, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Deleting your vlan.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_background(self):
        args = ['intranet', '--force', '--bg']
        result = self.invoke_with_exceptions(vlan.delete, args,
                                             obj=GandiContextHelper())

        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_unknown(self):
        args = ['vlanunknown']
        result = self.invoke_with_exceptions(vlan.delete, args)

        self.assertEqual(result.output, """\
Sorry vlan vlanunknown does not exist
Please use one of the following: ['vlantest', 'pouet', 'intranet', \
'123', '717', '999']
""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_refuse(self):
        args = ['intranet']
        result = self.invoke_with_exceptions(vlan.delete, args, input='\n',
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete vlan 'intranet'? [y/N]:""")

        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['--name', 'testvlan', '--datacenter', 'FR-SD3',
                '--subnet', '10.7.70.0/24', '--gateway', '10.7.70.254']
        result = self.invoke_with_exceptions(vlan.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your vlan.
\rProgress: [###] 100.00%  00:00:00  \
\nYour vlan testvlan has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.vlan.create'][0][0]
        self.assertEqual(params['datacenter_id'], 4)
        self.assertEqual(params['subnet'], '10.7.70.0/24')
        self.assertEqual(params['name'], 'testvlan')
        self.assertEqual(params['gateway'], '10.7.70.254')

    def test_create_datacenter_limited(self):
        args = ['--name', 'testvlan', '--datacenter', 'FR-SD2',
                '--subnet', '10.7.70.0/24', '--gateway', '10.7.70.254']
        result = self.invoke_with_exceptions(vlan.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
/!\ Datacenter FR-SD2 will be closed on 25/12/2017, please consider using \
another datacenter.
Creating your vlan.
\rProgress: [###] 100.00%  00:00:00  \
\nYour vlan testvlan has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.vlan.create'][0][0]
        self.assertEqual(params['datacenter_id'], 1)
        self.assertEqual(params['subnet'], '10.7.70.0/24')
        self.assertEqual(params['name'], 'testvlan')
        self.assertEqual(params['gateway'], '10.7.70.254')

    def test_create_datacenter_closed(self):
        args = ['--name', 'testvlan', '--datacenter', 'US-BA1',
                '--subnet', '10.7.70.0/24', '--gateway', '10.7.70.254']
        result = self.invoke_with_exceptions(vlan.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Error: /!\ Datacenter US-BA1 is closed, please choose another datacenter.""")

        self.assertEqual(result.exit_code, 1)

    def test_create_background(self):
        args = ['--name', 'testvlanbg', '--bg']
        result = self.invoke_with_exceptions(vlan.create, args,
                                             obj=GandiContextHelper())

        self.assertEqual(result.output.strip(), """\
{'id': 200, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.vlan.create'][0][0]
        self.assertEqual(params['datacenter_id'], 4)
        self.assertEqual(params['name'], 'testvlanbg')

    def test_update(self):
        args = ['pouet', '--name', 'chocolat',
                '--gateway', '10.7.70.254',
                '--bandwidth', '204800']

        result = self.invoke_with_exceptions(vlan.update, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your vlan.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.vlan.update'][0][1]
        self.assertEqual(params['name'], 'chocolat')
        self.assertEqual(params['gateway'], '10.7.70.254')

    def test_update_gateway_vm_unknown(self):
        args = ['pouet', '--name', 'chocolat',
                '--gateway', 'server01',
                '--bandwidth', '204800']

        result = self.invoke_with_exceptions(vlan.update, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Can't find 'server01' in 'pouet' vlan""")

        self.assertEqual(result.exit_code, 0)

    def test_update_gateway_vm(self):
        args = ['pouet', '--name', 'chocolat',
                '--gateway', 'server01',
                '--create',
                '--bandwidth', '204800']

        result = self.invoke_with_exceptions(vlan.update, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Will create a new ip in this vlan for vm server01
Creating your iface.
\rProgress: [###] 100.00%  00:00:00  \
\nYour iface has been created with the following IP addresses:
ip4:\t95.142.160.181
ip6:\t2001:4b98:dc0:47:216:3eff:feb2:3862
Attaching your iface.
\rProgress: [###] 100.00%  00:00:00  \
\nUpdating your vlan.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.vlan.update'][0][1]
        self.assertEqual(params['name'], 'chocolat')
        self.assertEqual(params['gateway'], '95.142.160.181')

    def test_update_gateway_multiple_ips(self):
        args = ['pouet', '--name', 'chocolat',
                '--gateway', 'server02']

        result = self.invoke_with_exceptions(vlan.update, args,
                                             obj=GandiContextHelper())

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
This vm has two ips in the vlan, don't know which one to choose \
(213.167.231.3, 192.168.232.252)""")

        self.assertEqual(result.exit_code, 0)
