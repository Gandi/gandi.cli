from click.testing import CliRunner

from gandi.cli.core.base import GandiModule
from ..compat import unittest
from ..fixtures.api import Api


class CommandTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        GandiModule._api = Api()
        GandiModule._conffiles = {'global': {'api': {'env': 'test',
                                                     'key': 'apikey0001'}}}

    def tearDown(self):
        GandiModule._api = None
        GandiModule._conffiles = {}
