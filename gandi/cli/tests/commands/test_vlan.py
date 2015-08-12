# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import vlan


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
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.invoke_with_exceptions(vlan.info, ['vlantest'])

        self.assertEqual(result.output, """\
name       : vlantest
state      : created
subnet     : 192.168.0.0/24
gateway    :
datacenter : LU-BI1
""")
        self.assertEqual(result.exit_code, 0)
