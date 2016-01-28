import os
from click.testing import CliRunner

from gandi.cli.core.base import GandiModule
from ..compat import unittest, mock
from ..fixtures.api import Api
from ..fixtures.mocks import MockObject


class CommandTestCase(unittest.TestCase):

    base_mocks = [
        ('gandi.cli.core.base.GandiModule.save', MockObject.blank_func),
        ('gandi.cli.core.base.GandiModule.execute', MockObject.execute),
        ('gandi.cli.core.base.GandiModule.deprecated', MockObject.deprecated),
    ]
    mocks = []

    def setUp(self):
        self.runner = CliRunner()

        self.mocks = self.mocks + self.base_mocks
        self.mocks = [mock.patch(*mock_args) for mock_args in self.mocks]
        for dummy in self.mocks:
            dummy.start()

        GandiModule._api = Api()
        GandiModule._api._calls = {}
        GandiModule._conffiles = {'global': {'api': {'env': 'test',
                                                     'key': 'apikey0001'}}}
        GandiModule._poll_freq = 0.1

        self.api_calls = GandiModule._api._calls

    def tearDown(self):
        GandiModule._api = None
        GandiModule._conffiles = {}

        for dummy in reversed(self.mocks):
            dummy.stop()

    def invoke_with_exceptions(self, cli, args, catch_exceptions=False,
                               **kwargs):
        return self.runner.invoke(cli, args, catch_exceptions=catch_exceptions,
                                  **kwargs)

    def isolated_invoke_with_exceptions(self, cli, args,
                                        catch_exceptions=False,
                                        temp_dir=None,
                                        temp_name=None,
                                        temp_content=None,
                                        **kwargs):

        temp_dir = temp_dir or 'sandbox'
        temp_name = temp_name or 'example.txt'
        with self.runner.isolated_filesystem():
            os.mkdir(temp_dir)

            with open('%s/%s' % (temp_dir, temp_name), 'w') as f:
                f.write(temp_content)

            return self.runner.invoke(cli, args,
                                      catch_exceptions=catch_exceptions,
                                      **kwargs)
