from click.testing import CliRunner

from gandi.cli.core.base import GandiModule
from ..compat import mock, unittest
from ..fixtures.api import Api


class CommandTestCase(unittest.TestCase):
    
    def setUp(self):
        self.runner = CliRunner()
        GandiModule._api = Api()

    def tearDown(self):
        GandiModule._api = None
