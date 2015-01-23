from click.testing import CliRunner

from gandi.cli.core.base import GandiModule
from ..compat import unittest, mock
from ..fixtures.api import Api
from ..fixtures.mocks import MockObject


class CommandTestCase(unittest.TestCase):

    mocks = [('gandi.cli.core.base.GandiModule.save', MockObject.blank_func)]

    def setUp(self):
        self.runner = CliRunner()

        self.mocks = [mock.patch(*mock_args) for mock_args in self.mocks]
        for dummy in self.mocks:
            dummy.start()

        GandiModule._api = Api()
        GandiModule._conffiles = {'global': {'api': {'env': 'test',
                                                     'key': 'apikey0001'}}}

    def tearDown(self):
        GandiModule._api = None
        GandiModule._conffiles = {}

        for dummy in reversed(self.mocks):
            dummy.stop()
