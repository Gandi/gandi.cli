from datetime import datetime

try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime

type_list = list


def available(domains):

    ret = {}
    for domain in domains:
        if "unavailable" in domain:
            ret[domain] = "unavailable"
        elif "pending" in domain:
            ret[domain] = "pending"
        else:
            ret[domain] = "available"

    return ret


def create(domain, params):
    ret = {"id": 400, "step": "WAIT"}

    if params and "extra" in params:
        ret["extra"] = params["extra"]

    return ret


def renew(domain, params):
    return {"id": 400, "step": "WAIT"}


def mailbox_list(domain, options):
    return [
        {
            "login": "admin",
            "responder": {"active": False},
            "quota": {"granted": 0, "used": 233},
        }
    ]


def mailbox_info(domain, login):
    ret = {
        "aliases": [],
        "login": "admin",
        "responder": {"active": False, "text": None},
        "fallback_email": "",
        "quota": {"granted": 0, "used": 233},
    }
    return ret


def mailbox_create(domain, login, params):
    return {"id": 400, "step": "WAIT"}


def mailbox_delete(domain, login):
    return {"id": 400, "step": "WAIT"}


def mailbox_update(domain, login, params):
    return {"id": 400, "step": "WAIT"}


def mailbox_alias_set(domain, login, aliases):
    return {"id": 400, "step": "WAIT"}


def mailbox_purge(domain, login):
    return {"id": 400, "step": "WAIT"}


def forward_list(domain, options):
    return [
        {"source": "admin", "destinations": ["admin@cli.sexy", "grumpy@cat.lol"]},
        {"source": "contact", "destinations": ["contact@cli.sexy"]},
    ]


def forward_create(domain, source, options):
    return [{"source": source, "destinations": options["destinations"]}]


def forward_update(domain, source, options):
    return [{"source": source, "destinations": options["destinations"]}]


def forward_delete(domain, source):
    return True


def zone_record_list(zone_id, version, options=None):
    ret = [
        {
            "id": 337085079,
            "name": "*",
            "ttl": 10800,
            "type": "A",
            "value": "73.246.104.110",
        },
        {
            "id": 337085078,
            "name": "@",
            "ttl": 10800,
            "type": "A",
            "value": "73.246.104.110",
        },
        {
            "id": 337085081,
            "name": "much",
            "ttl": 10800,
            "type": "A",
            "value": "192.243.24.132",
        },
        {
            "id": 337085072,
            "name": "blog",
            "ttl": 10800,
            "type": "CNAME",
            "value": "blogs.vip.gandi.net.",
        },
        {
            "id": 337085082,
            "name": "cloud",
            "ttl": 10800,
            "type": "CNAME",
            "value": "gpaas6.dc0.gandi.net.",
        },
        {
            "id": 337085075,
            "name": "imap",
            "ttl": 10800,
            "type": "CNAME",
            "value": "access.mail.gandi.net.",
        },
        {
            "id": 337085071,
            "name": "pop",
            "ttl": 10800,
            "type": "CNAME",
            "value": "access.mail.gandi.net.",
        },
        {
            "id": 337085074,
            "name": "smtp",
            "ttl": 10800,
            "type": "CNAME",
            "value": "relay.mail.gandi.net.",
        },
        {
            "id": 337085073,
            "name": "webmail",
            "ttl": 10800,
            "type": "CNAME",
            "value": "agent.mail.gandi.net.",
        },
        {
            "id": 337085077,
            "name": "@",
            "ttl": 10800,
            "type": "MX",
            "value": "50 fb.mail.gandi.net.",
        },
        {
            "id": 337085076,
            "name": "@",
            "ttl": 10800,
            "type": "MX",
            "value": "10 spool.mail.gandi.net.",
        },
    ]

    options = options or {}
    options.pop("items_per_page", None)

    def match(zone, options):
        for fkey in options:
            if zone[fkey] != options[fkey]:
                return

        return zone

    ret = [zone for zone in ret if match(zone, options)]

    return ret


def zone_version_new(zone_id):
    return 242424


def zone_record_add(zone_id, version, data):
    return


def zone_version_set(zone_id, version):
    return


def zone_record_delete(zone_id, version, data):
    return


def zone_record_update(zone_id, version, opts, data):
    return


def zone_record_set(zone_id, version, data):
    return


def dnssec_delete(key_id):
    return {"id": 666, "step": "WAIT"}


def dnssec_list(domain):
    return [
        {
            "algorithm": 5,
            "date_created": datetime(2012, 2, 24, 17, 16, 8),
            "digest": "457c626c008cc70d68133254abc4ee4eb79e4e6c99f9423b60b543"
            "fa8a69e6ac",
            "digest_type": 2,
            "flags": 257,
            "id": 125,
            "keytag": 9301,
            "public_key": "AwEAAdYixYvq9eJLRQcxUeYJWaxAGXiP/K1/C7XHbUWGzA8AHC"
            "Rp81FAmfwcw1FrJ7bMViEegewPDGciQSv5HotPPOynUmkZbgzt"
            "OeejH/+3Il/cM8SW4Et0i+99S7l9as+FI3AYOhsllDJK1WM9sm"
            "n0S/9igfpR2dGmCyDU ZfeR1A49\n",
        }
    ]


def dnssec_create(domain, params):
    return {"id": 667, "step": "WAIT"}
