import httpretty
# disable SSL requests warning for tests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from gandi.cli.commands import root
from .base import CommandTestCase


class StatusTestCase(CommandTestCase):

    def _mock_http_request_base(self, status='SUNNY'):

        response = """{
        "fields": {"status": {"value": [
                {"SUNNY": "All services are up and running"},
                {"CLOUDY": "A scheduled maintenance ongoing"},
                {"FOGGY": "Incident which are not impacting our services."},
                {"STORMY": "An incident ongoing"}]}}}
        """
        httpretty.register_uri(httpretty.GET,
                               'https://status.gandi.net/api/status/schema',
                               body=response,
                               status=200)

        response = """{"status": "%s"}""" % status
        httpretty.register_uri(httpretty.GET,
                               'https://status.gandi.net/api/status',
                               body=response,
                               status=200)

    def _mock_http_request_working(self, status='SUNNY'):

        self._mock_http_request_base(status)
        response = """[
        {"description": "IAAS",
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
        httpretty.register_uri(httpretty.GET,
                               'https://status.gandi.net/api/services',
                               body=response,
                               status=200)

        response = """[]"""

        incident_url = ('https://status.gandi.net/api/events?category='
                        'Incident&current=true')
        httpretty.register_uri(httpretty.GET,
                               incident_url,
                               body=response,
                               status=200)

    def _mock_http_request_incident(self, status='STORMY'):

        self._mock_http_request_base(status)
        response = """[
        {"description": "IAAS",
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
        httpretty.register_uri(httpretty.GET,
                               'https://status.gandi.net/api/services',
                               body=response,
                               status=200)

        response = """
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

        incident_url = ('https://status.gandi.net/api/events?category='
                        'Incident&services=PAAS&current=true')
        httpretty.register_uri(httpretty.GET,
                               incident_url,
                               body=response,
                               status=200)

    def _mock_http_request_incident_no_service(self):

        response = """
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

        incident_url_2 = ('https://status.gandi.net/api/events?category='
                          'Incident&current=true')
        httpretty.register_uri(httpretty.GET,
                               incident_url_2,
                               body=response,
                               status=200)

    @httpretty.activate
    def test_status(self):
        self._mock_http_request_working()

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

    @httpretty.activate
    def test_status_service(self):
        self._mock_http_request_working()

        result = self.invoke_with_exceptions(root.status, ['ssl'])

        wanted = ("""\
SSL       : All services are up and running
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @httpretty.activate
    def test_status_service_incident(self):
        self._mock_http_request_incident('STORMY')

        result = self.invoke_with_exceptions(root.status, ['paas'])

        url = 'https://status.gandi.net/timeline/events/7'
        wanted = ("""\
PAAS      : Incident on a storage unit on Paris datacenter - %s
""") % url

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    @httpretty.activate
    def test_status_no_service_incident(self):
        self._mock_http_request_working('FOGGY')
        self._mock_http_request_incident_no_service()

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
