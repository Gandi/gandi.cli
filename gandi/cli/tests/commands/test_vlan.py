# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import vlan


class VlanTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(vlan.list, [])

        self.assertEqual(result.output, """\
name      : vlantest
state     : created
datacenter: FR
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.runner.invoke(vlan.info, ['vlantest'])

        self.assertEqual(result.output, """\
name       : vlantest
state      : created
subnet     : 192.168.0.0/24
gateway    :
datacenter : LU
""")
        self.assertEqual(result.exit_code, 0)
