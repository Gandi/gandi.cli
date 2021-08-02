import json
from pathlib import Path
import os

DATA = Path(__file__).resolve().parent.parent / "commands" / "data"


def _domain(domain):
    contact = {
        "city": "Paris",
        "given": "Serge",
        "reachability": "done",
        "family": "Lapin",
        "zip": "75000",
        "extra_parameters": {
            "birth_date": "",
            "birth_department": "",
            "birth_city": "",
            "birth_country": "",
        },
        "orgname": "Lapin SARL",
        "country": "FR",
        "streetaddr": "42 rue de la ruelle",
        "data_obfuscated": True,
        "mail_obfuscated": True,
        "phone": "+33.600000000",
        "state": "FR-IDF",
        "validation": "none",
        "type": 1,
        "email": "admin@example.com",
    }
    return {
        "status": [],
        "dates": {
            "created_at": "2010-09-22T15:06:18Z",
            "deletes_at": "2021-12-20T06:12:16Z",
            "hold_begins_at": "2021-11-22T16:12:16Z",
            "hold_ends_at": "2021-12-20T16:12:16Z",
            "pending_delete_ends_at": "2022-01-19T16:12:16Z",
            "registry_created_at": "2010-09-22T13:06:16Z",
            "registry_ends_at": "2015-09-22T00:00:00Z",
            "renew_begins_at": "2012-01-01T00:00:00Z",
            "restore_ends_at": "2022-01-19T16:12:16Z",
            "updated_at": "2014-09-21T03:10:07Z",
            "authinfo_expires_at": "2021-10-22T15:18:03Z",
        },
        "can_tld_lock": False,
        "tags": [],
        "nameservers": [
            "ns-4-a.gandi.net",
            "ns-176-b.gandi.net",
            "ns-148-c.gandi.net",
        ],
        "contacts": {
            "owner": contact,
            "admin": contact,
            "bill": contact,
            "tech": contact,
        },
        "fqdn": domain,
        "autorenew": {
            "dates": [
                "2021-10-22T15:12:16Z",
                "2021-11-07T16:12:16Z",
                "2021-11-21T16:12:16Z",
            ],
            "org_id": "a22e143d-4625-4617-a09d-fa286ca5b0b6",
            "duration": 1,
            "href": "https://api.gandi.net/v5/domain/domains/{domain}/autorenew",
            "enabled": True,
        },
        "authinfo": "4796ee0d!",
        "sharing_space": {
            "type": "organization",
            "id": "83edbd56-708d-46e9-8936-665e1521570c",
            "reseller": False,
            "name": "AA1-GANDI",
        },
        "tld": "fr",
        "services": ["gandilivedns", "mailboxv2"],
        "id": "17ce04c2-a3a6-4112-aa64-47293187b437",
        "trustee_roles": [],
        "href": f"https://api.gandi.net/v5/domain/domains/{domain}",
        "fqdn_unicode": domain,
    }


RESPONSES = {
    "https://api.gandi.net/v5/livedns/domains": {
        "status": 200,
        "headers": "application/json",
        "body": [
            {
                "domain_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com",  # noqa
                "domain_records_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records",  # noqa
                "fqdn": "iheartcli.com",
            },
            {
                "domain_href": "https://api.gandi.net/v5/livedns/domains/cli.sexy",  # noqa
                "domain_records_href": "https://api.gandi.net/v5/livedns/domains/cli.sexy/records",  # noqa
                "fqdn": "cli.sexy",
            },
        ],
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com": {
        "status": 200,
        "headers": "application/json",
        "body": {
            "domain_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com",  # noqa
            "domain_keys_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys",  # noqa
            "domain_records_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records",  # noqa
            "fqdn": "iheartcli.com",
            "zone_href": "https://dns.api.gandi.net/api/v5/zones/397c514-e7cb-11e6-9429-00163e6dc886",  # noqa
            "zone_records_href": "https://dns.api.gandi.net/api/v5/zones/397c514-e7cb-11e6-9429-00163e6dc886/records",  # noqa
            "zone_uuid": "397c514-e7cb-11e6-9429-00163e6dc886",
        },
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records?sort_by=rrset_name": {  # noqa
        "status": 200,
        "headers": "application/json",
        "body": [
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/%40/A",  # noqa
                "rrset_name": "@",
                "rrset_ttl": 10800,
                "rrset_type": "A",
                "rrset_values": ["217.70.184.38"],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/%40/MX",  # noqa
                "rrset_name": "@",
                "rrset_ttl": 10800,
                "rrset_type": "MX",
                "rrset_values": ["50 fb.mail.gandi.net.", "10 spool.mail.gandi.net."],
            },  # noqa
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/blog/CNAME",  # noqa
                "rrset_name": "blog",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["blogs.vip.gandi.net."],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/imap/CNAME",  # noqa
                "rrset_name": "imap",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["access.mail.gandi.net."],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/pop/CNAME",  # noqa
                "rrset_name": "pop",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["access.mail.gandi.net."],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/smtp/CNAME",  # noqa
                "rrset_name": "smtp",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["relay.mail.gandi.net."],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/webmail/CNAME",  # noqa
                "rrset_name": "webmail",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["webmail.gandi.net."],
            },
            {
                "rrset_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/www/CNAME",  # noqa
                "rrset_name": "www",
                "rrset_ttl": 10800,
                "rrset_type": "CNAME",
                "rrset_values": ["webredir.vip.gandi.net."],
            },
        ],
    },
    "https://api.gandi.net/v5/livedns/dns/rrtypes": {
        "status": 200,
        "headers": "application/json",
        "body": [
            "A",
            "AAAA",
            "CAA",
            "CDS",
            "CNAME",
            "DNAME",
            "DS",
            "LOC",
            "MX",
            "NS",
            "PTR",
            "SPF",
            "SRV",
            "SSHFP",
            "TLSA",
            "TXT",
            "WKS",
        ],
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records": {
        "status": 201,
        "headers": "application/json",
        "body": {"message": "DNS Record Created"},
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/blog/CNAME": {  # noqa
        "status": 204,
        "headers": "application/json",
        "body": {},
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys": {
        "status": 200,
        "headers": {
            "content-type": "application/json",
            "location": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168",
        },  # noqa
        "body": [
            {
                "algorithm": 13,
                "algorithm_name": "ECDSAP256SHA256",
                "deleted": False,
                "ds": "iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a",  # noqa
                "flags": 256,
                "fqdn": "iheartcli.com",
                "key_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168",  # noqa
                "status": "active",
                "uuid": "3415833-2314-4a86-ba1c-c3c58608a168",
            },
            {
                "algorithm": 13,
                "algorithm_name": "ECDSAP256SHA256",
                "deleted": False,
                "ds": "iheartcli.com. 3600 IN DS 43819 13 2 b4e6ed591f28f4a269b9adfaedec836ea0fe63a8f7f5097108297afa5492b70",  # noqa
                "flags": 256,
                "fqdn": "iheartcli.com",
                "key_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/adaab60-bb17-40ed-a13e-88376fe28c86",  # noqa
                "status": "active",
                "uuid": "adaab60-bb17-40ed-a13e-88376fe28c86",
            },
        ],
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168": {  # noqa
        "status": 200,
        "headers": "application/json",
        "body": {
            "algorithm": 13,
            "algorithm_name": "ECDSAP256SHA256",
            "deleted": False,
            "ds": "iheartcli.com. 3600 IN DS 5411 13 2 6153c39cfe4ff8673635490515e19f5336f5b7ee9c5ca4572fc44b24a0e794a",  # noqa
            "flags": 256,
            "fqdn": "iheartcli.com",
            "public_key": "Gnhra3gcNHUL0d05Ia6F/tgBzDD/Km6c2XFZA9RAOcjk/qg9aodc79MQtsTx4/CBlTmCSRIxlXWm1yMmV3LOlw==",  # noqa
            "fingerprint": "626168cae12c674f38958b324e10c7bb63ed74cc9d649bf04766a7c095c865787",  # noqa
            "key_href": "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/3415833-2314-4a86-ba1c-c3c58608a168",  # noqa
            "status": "active",
            "tag": 40658,
            "uuid": "3415833-2314-4a86-ba1c-c3c58608a168",
        },
    },
    "https://api.gandi.net/v5/livedns/domains/iheartcli.com/keys/adaab60-bb17-40ed-a13e-88376fe28c86": {  # noqa
        "status": 204,
        "headers": "application/json",
        "body": {},
    },
    "https://api.gandi.net/v5/domain/domains": {
        "status": 200,
        "headers": "application/json",
        "body": [
            {
                "status": [],
                "dates": {
                    "created_at": "2010-09-22T15:06:18Z",
                    "registry_created_at": "2010-09-22T13:06:16Z",
                    "registry_ends_at": "2015-09-22T00:00:00Z",
                    "updated_at": "2014-09-21T03:10:07Z",
                },
                "tags": [],
                "fqdn": "iheartcli.com",
                "id": "5debe7de-7856-45ad-95ec-5cd4461c3739",
                "autorenew": True,
                "tld": "com",
                "owner": "AA1",
                "orga_owner": "AA1",
                "domain_owner": "AA1",
                "nameserver": {"current": "livedns"},
                "href": "https://api.gandi.net/v5/domain/domains/iheartcli.com",
                "fqdn_unicode": "iheartcli.com",
            },
            {
                "status": [],
                "dates": {
                    "created_at": "2013-04-10T12:46:05Z",
                    "registry_created_at": "2014-04-10T10:46:04Z",
                    "registry_ends_at": "2014-04-10T00:00:00Z",
                    "updated_at": "2015-03-13T10:30:05Z",
                },
                "tags": [],
                "fqdn": "cli.sexy",
                "id": "ab28e88c-b470-433b-a31c-e514476f3711",
                "autorenew": True,
                "tld": "sexy",
                "owner": "PXP561",
                "orga_owner": "PXP561",
                "domain_owner": "PXP561",
                "nameserver": {"current": "livedns"},
                "href": "https://api.gandi.net/v5/domain/domains/cli.sexy",
                "fqdn_unicode": "cli.sexy",
            },
        ],
    },
    "https://api.gandi.net/v5/domain/domains?per_page=100": {
        "status": 200,
        "headers": "application/json",
        "body": [
            {
                "status": [],
                "dates": {
                    "created_at": "2010-09-22T15:06:18Z",
                    "registry_created_at": "2010-09-22T13:06:16Z",
                    "registry_ends_at": "2015-09-22T00:00:00Z",
                    "updated_at": "2014-09-21T03:10:07Z",
                },
                "tags": [],
                "fqdn": "iheartcli.com",
                "id": "5debe7de-7856-45ad-95ec-5cd4461c3739",
                "autorenew": True,
                "tld": "com",
                "owner": "AA1",
                "orga_owner": "AA1",
                "domain_owner": "AA1",
                "nameserver": {"current": "livedns"},
                "href": "https://api.gandi.net/v5/domain/domains/iheartcli.com",
                "fqdn_unicode": "iheartcli.com",
            },
            {
                "status": [],
                "dates": {
                    "created_at": "2013-04-10T12:46:05Z",
                    "registry_created_at": "2014-04-10T10:46:04Z",
                    "registry_ends_at": "2014-04-10T00:00:00Z",
                    "updated_at": "2015-03-13T10:30:05Z",
                },
                "tags": [],
                "fqdn": "cli.sexy",
                "id": "ab28e88c-b470-433b-a31c-e514476f3711",
                "autorenew": True,
                "tld": "sexy",
                "owner": "PXP561",
                "orga_owner": "PXP561",
                "domain_owner": "PXP561",
                "nameserver": {"current": "livedns"},
                "href": "https://api.gandi.net/v5/domain/domains/cli.sexy",
                "fqdn_unicode": "cli.sexy",
            },
        ],
    },
    "https://api.gandi.net/v5/domain/domains/iheartcli.com": {
        "status": 200,
        "headers": "application/json",
        "body": _domain("iheartcli.com"),
    },
    "https://gandi.statuspage.io/api/v2/summary.json": {
        "status": 200,
        "headers": "application/json",
        "body": ...,
    },
}


class FakeJsonClient:
    @classmethod
    def break_a_service(cls):
        RESPONSES["https://gandi.statuspage.io/api/v2/summary.json"] = {
            "status": 200,
            "headers": "application/json",
            "body": json.loads((DATA / "summary_a_service_down.json").read_text()),
        }

    @classmethod
    def restore_services(cls):
        RESPONSES["https://gandi.statuspage.io/api/v2/summary.json"] = {
            "status": 200,
            "headers": "application/json",
            "body": json.loads((DATA / "summary_all_ok.json").read_text()),
        }

    @classmethod
    def request(cls, method, url, **kwargs):
        content = RESPONSES[url]["body"]
        headers = RESPONSES[url]["headers"]
        if kwargs.get("headers", {}).get("Accept") == "text/plain":
            content = """\
@ 10800 IN A 217.70.184.38
@ 10800 IN MX 10 spool.mail.gandi.net.
@ 10800 IN MX 50 fb.mail.gandi.net.
@ 10800 IN SOA ns1.gandi.net. hostmaster.gandi.net. 197539823 10800 3600 604800 10800
blog 10800 IN CNAME blogs.vip.gandi.net.
imap 10800 IN CNAME access.mail.gandi.net.
pop 10800 IN CNAME access.mail.gandi.net.
smtp 10800 IN CNAME relay.mail.gandi.net.
webmail 10800 IN CNAME webmail.gandi.net.
www 10800 IN CNAME webredir.vip.gandi.net."""  # noqa
        content_hdr = kwargs.get("headers", {}).get("Content-Type")
        if method == "PUT" and content_hdr == "text/plain":
            content = {"message": "DNS Record Created"}
        if (
            method == "PUT"
            and url
            == "https://api.gandi.net/v5/livedns/domains/iheartcli.com/records/blog/CNAME"
        ):  # noqa
            content = {"message": "DNS Record Created"}
        return content, headers
