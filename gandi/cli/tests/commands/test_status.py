import json
from functools import partial
from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import root

# disable SSL requests warning for tests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


RESPONSES = {
    'https://status.gandi.net/api/status/schema': {
        'status': 200,
        'headers': 'application/json',
        'body': """{"fields": {"status": {"value": [
                   {"SUNNY": "All services are up and running"},
                   {"CLOUDY": "A scheduled maintenance ongoing"},
                   {"FOGGY": "Incident which are not impacting our services."},
                   {"STORMY": "An incident ongoing"}]}}}"""
    },
}


def _mock_requests(status, method, url, *args, **kwargs):
    content = None
    if status == 'SUNNY':
        if url == 'https://status.gandi.net/api/services':
            content = """[{"description": "IAAS",
                           "name": "IAAS",
                           "status": "SUNNY"},
                          {"description": "PAAS",
                           "name": "PAAS",
                           "status": "SUNNY"},
                          {"description": "Site",
                          "name": "Site",
                          "status": "SUNNY"},
                          {"description": "API",
                          "name": "API",
                          "status": "SUNNY"},
                          {"description": "SSL",
                          "name": "SSL",
                          "status": "SUNNY"},
                          {"description": "Domain",
                          "name": "Domain",
                          "status": "SUNNY"},
                          {"description": "Email",
                          "name": "Email",
                          "status": "SUNNY"}]"""
        if url == 'https://status.gandi.net/api/events?category=Incident&current=true':  # noqa
            content = """[]"""

    if status == 'STORMY':
        if url == 'https://status.gandi.net/api/services':
            content = """[{"description": "IAAS",
                           "name": "IAAS",
                           "status": "SUNNY"},
                          {"description": "PAAS",
                           "name": "PAAS",
                           "status": "STORMY"},
                          {"description": "Site",
                          "name": "Site",
                          "status": "SUNNY"},
                          {"description": "API",
                          "name": "API",
                          "status": "SUNNY"},
                          {"description": "SSL",
                          "name": "SSL",
                          "status": "SUNNY"},
                          {"description": "Domain",
                          "name": "Domain",
                          "status": "SUNNY"},
                          {"description": "Email",
                          "name": "Email",
                          "status": "SUNNY"}]"""
        if url == 'https://status.gandi.net/api/events?category=Incident&services=PAAS&current=true':  # noqa
            content = """
                [{"category": "Incident",
                "date_end": "2014-10-08T06:20:00+00:00",
                "date_start": "2014-10-07T18:00:00+00:00",
                "duration": 740,
                "estimate_date_end": "2014-10-08T06:20:00+00:00",
                "id": "7",
                "services": [
                    "IAAS",
                    "PAAS"
                ],
                "title": "Incident on a storage unit on Paris datacenter"}]
                """

    if status == 'FOGGY':
        if url == 'https://status.gandi.net/api/services':
            content = """[{"description": "IAAS",
                           "name": "IAAS",
                           "status": "SUNNY"},
                          {"description": "PAAS",
                           "name": "PAAS",
                           "status": "SUNNY"},
                          {"description": "Site",
                          "name": "Site",
                          "status": "SUNNY"},
                          {"description": "API",
                          "name": "API",
                          "status": "SUNNY"},
                          {"description": "SSL",
                          "name": "SSL",
                          "status": "SUNNY"},
                          {"description": "Domain",
                          "name": "Domain",
                          "status": "SUNNY"},
                          {"description": "Email",
                          "name": "Email",
                          "status": "SUNNY"}]"""
        if url == 'https://status.gandi.net/api/events?category=Incident&current=true':  # noqa
            content = """
                [{"category": "Incident",
                "date_end": "2015-04-15T22:06:43+00:00",
                "date_start": "2015-04-15T21:30:00+00:00",
                "duration": 36,
                "estimate_date_end": "2015-04-15T22:30:00+00:00",
                "id": "15",
                "services": [],
                "title": "Reachability issue on our website"
                }]
                """

    if url == 'https://status.gandi.net/api/status':
        content = """{"status": "%s"}""" % status
    elif not content:
        content = RESPONSES[url]['body']

    content = json.loads(content)
    mock_resp = mock.Mock()
    mock_resp.status_code = 200
    mock_resp.content = content
    mock_resp.json = mock.Mock(return_value=content)
    return mock_resp


class StatusTestCase(CommandTestCase):

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status(self, mock_request):
        mock_request.side_effect = partial(_mock_requests, 'SUNNY')

        result = self.invoke_with_exceptions(root.status, [])

        wanted = ("""\
IAAS      : All services are up and running
PAAS      : All services are up and running
Site      : All services are up and running
API       : All services are up and running
SSL       : All services are up and running
Domain    : All services are up and running
Email     : All services are up and running
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status_service(self, mock_request):
        mock_request.side_effect = partial(_mock_requests, 'SUNNY')

        result = self.invoke_with_exceptions(root.status, ['ssl'])

        wanted = ("""\
SSL       : All services are up and running
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status_service_incident(self, mock_request):
        mock_request.side_effect = partial(_mock_requests, 'STORMY')

        result = self.invoke_with_exceptions(root.status, ['paas'])

        url = 'https://status.gandi.net/timeline/events/7'
        wanted = ("""\
PAAS      : Incident on a storage unit on Paris datacenter - %s
""") % url

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @mock.patch('gandi.cli.core.client.requests.request')
    def test_status_no_service_incident(self, mock_request):
        mock_request.side_effect = partial(_mock_requests, 'FOGGY')

        result = self.invoke_with_exceptions(root.status, [])

        wanted = ("""\
Reachability issue on our website - https://status.gandi.net/timeline/events/15
IAAS      : All services are up and running
PAAS      : All services are up and running
Site      : All services are up and running
API       : All services are up and running
SSL       : All services are up and running
Domain    : All services are up and running
Email     : All services are up and running
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)
