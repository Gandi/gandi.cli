import json
import os
from functools import partial
from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import root
from gandi.cli.tests.fixtures.json import FakeJsonClient
# disable SSL requests warning for tests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


class StatusTestCase(CommandTestCase):

    def test_status(self):
        FakeJsonClient.restore_services()
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

    def test_status_service(self):
        FakeJsonClient.restore_services()
        result = self.invoke_with_exceptions(root.status, ['Network'])
        wanted = ("""\
Network                       : operational
""")
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_status_service_incident(self):
        FakeJsonClient.break_a_service()
        result = self.invoke_with_exceptions(root.status, ['PAAS LU-BI1'])
        wanted = """\
Hosting - PAAS LU-BI1         : Hard drive issues -\
 http://stspg.io/stc35fvwr5nt
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)
