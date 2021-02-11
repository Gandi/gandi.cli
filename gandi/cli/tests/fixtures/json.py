class FakeJsonClient:
    @classmethod
    def request(cls, method, url, **kwargs):
        if (method, url) == ('GET', 'https://api.gandi.net/v5/domain/domains/iheartcli.com'):
            return cls.info("iheartcli.com"), {}
        if (method, url) == ('GET', 'https://api.gandi.net/v5/domain/domains?per_page=100'):
            return cls.list(), {}
        raise ValueError(f"Unmocked URL: {url}")

    @classmethod
    def list(cls):
        return [
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
        ]

    @classmethod
    def info(cls, domain):
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
