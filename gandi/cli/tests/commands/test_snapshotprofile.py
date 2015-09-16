# -*- coding: utf-8 -*-

from .base import CommandTestCase
from gandi.cli.commands import snapshotprofile


class SnapshotprofileTestCase(CommandTestCase):

    def test_list(self):

        result = self.invoke_with_exceptions(snapshotprofile.list, [])

        self.assertEqual(result.output, """\
id           : 1
name         : minimal
kept_total   : 2
target       : vm
----------
id           : 2
name         : full_week
kept_total   : 7
target       : vm
----------
id           : 3
name         : security
kept_total   : 10
target       : vm
----------
id           : 7
name         : paas_normal
kept_total   : 3
target       : paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_paas(self):
        args = ['--only-paas']
        result = self.invoke_with_exceptions(snapshotprofile.list, args)

        self.assertEqual(result.output, """\
id           : 7
name         : paas_normal
kept_total   : 3
target       : paas
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_vm(self):
        args = ['--only-vm']
        result = self.invoke_with_exceptions(snapshotprofile.list, args)

        self.assertEqual(result.output, """\
id           : 1
name         : minimal
kept_total   : 2
target       : vm
----------
id           : 2
name         : full_week
kept_total   : 7
target       : vm
----------
id           : 3
name         : security
kept_total   : 10
target       : vm
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        args = ['security']
        result = self.invoke_with_exceptions(snapshotprofile.info, args)

        self.assertEqual(result.output, """\
id           : 3
name         : security
kept_total   : 10
target       : vm
quota_factor : 2.0
----------
name         : hourly6
kept_version : 3
----------
name         : daily
kept_version : 6
----------
name         : weekly4
kept_version : 1
""")
        self.assertEqual(result.exit_code, 0)
