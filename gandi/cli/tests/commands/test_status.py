import httpretty

from gandi.cli.commands import root
from .base import CommandTestCase


class StatusTestCase(CommandTestCase):

    def _mock_http_request(self):

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

        response = """{"status": "SUNNY"}"""
        httpretty.register_uri(httpretty.GET,
                               'https://status.gandi.net/api/status',
                               body=response,
                               status=200)

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

    @httpretty.activate
    def test_status(self):
        self._mock_http_request()

        result = self.runner.invoke(root.status, [])

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
        self._mock_http_request()

        result = self.runner.invoke(root.status, ['ssl'])

        wanted = ("""\
SSL       : All services are up and running
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)
