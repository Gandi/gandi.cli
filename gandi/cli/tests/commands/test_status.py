import json
import os
from functools import partial
from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import root

# disable SSL requests warning for tests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def _mock_requests(json_path, method, url, *args, **kwargs):
    with open(json_path, 'r') as json_file:
        content = json.load(json_file)

    mock_resp = mock.Mock()
    mock_resp.status_code = 200
    mock_resp.content = content
    mock_resp.json = mock.Mock(return_value=content)
    return mock_resp


def _build_file_path(file_name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_name, "data", file_name)


class StatusTestCase(CommandTestCase):

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status(self, mock_request):
        json_path = _build_file_path("summary_all_ok.json")
        mock_request.side_effect = partial(_mock_requests, json_path)

        result = self.invoke_with_exceptions(root.status, [])

        wanted = ("""\
APIs - PUBLIC API v4          : operational
APIs - PUBLIC API v5          : operational
DNS - LiveDNS                 : operational
DNS - ns6.gandi.net           : operational
DNS - {abc}.dns.gandi.net     : operational
Domain name registration      : operational
Gandimail - Access (IMAP/POP3): operational
Gandimail - Roundcube webmail : operational
Gandimail - SMTP in           : operational
Gandimail - SMTP out          : operational
Gandimail - Sogo webmail      : operational
Hosting - IAAS FR-SD3         : operational
Hosting - IAAS FR-SD5         : operational
Hosting - IAAS FR-SD6         : operational
Hosting - IAAS LU-BI1         : operational
Hosting - PAAS FR-SD3         : operational
Hosting - PAAS FR-SD5         : operational
Hosting - PAAS FR-SD6         : operational
Hosting - PAAS LU-BI1         : operational
Network                       : operational
Portal - www.gandi.net        : operational
Web redirection services      : operational
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status_service(self, mock_request):
        json_path = _build_file_path("summary_all_ok.json")
        mock_request.side_effect = partial(_mock_requests, json_path)

        result = self.invoke_with_exceptions(root.status, ['Network'])

        wanted = ("""\
Network                       : operational
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status_service_incident(self, mock_request):
        json_path = _build_file_path("summary_a_service_down.json")
        mock_request.side_effect = partial(_mock_requests, json_path)

        result = self.invoke_with_exceptions(root.status, ['PAAS LU-BI1'])

        wanted = """\
Hosting - PAAS LU-BI1         : Hard drive issues -\
 http://stspg.io/stc35fvwr5nt
"""

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)
