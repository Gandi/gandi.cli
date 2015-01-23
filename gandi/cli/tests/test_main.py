from .compat import unittest
from .compat import mock


class TestCase(unittest.TestCase):

    def test_main(self):
        cli = mock.Mock()
        with mock.patch('gandi.cli.core.cli.cli', cli):
            from gandi.cli.__main__ import main
            main()
            cli.assert_called_once_with(obj={})
