
from .base import CommandTestCase
from gandi.cli.commands import vm


class VmTestCase(CommandTestCase):

    def test_list(self):

        result = self.runner.invoke(vm.list, [])

        self.assertEqual(result.output, """hostname  : arch64
state     : running
----------
hostname  : docker
state     : running
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):

        result = self.runner.invoke(vm.list, ['--id'])

        self.assertEqual(result.output, """hostname  : arch64
state     : running
id        : 80458
----------
hostname  : docker
state     : running
id        : 128620
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_state(self):

        result = self.runner.invoke(vm.list, ['--state', 'halted'])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_list_filter_datacenter(self):

        result = self.runner.invoke(vm.list, ['--datacenter', 'FR'])

        self.assertEqual(result.output, """hostname  : arch64
state     : running
""")
        self.assertEqual(result.exit_code, 0)
