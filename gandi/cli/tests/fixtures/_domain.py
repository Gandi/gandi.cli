from datetime import datetime

try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime

type_list = list


def list(options):
    return [{'authinfo': 'abcdef0001',
             'autorenew': None,
             'zone_id': 424242,
             'tags': 'bla',
             'contacts': {'owner': {'handle': 'AA1-GANDI'},
                          'admin': {'handle': 'AA2-GANDI'},
                          'bill': {'handle': 'AA3-GANDI'},
                          'reseller': {'handle': 'AA4-GANDI'},
                          'tech': {'handle': 'AA5-GANDI'}},
             'date_created': datetime(2010, 9, 22, 15, 6, 18),
             'date_delete': datetime(2015, 10, 19, 19, 14, 0),
             'date_hold_begin': datetime(2015, 9, 22, 22, 0, 0),
             'date_registry_creation': datetime(2010, 9, 22, 13, 6, 16),
             'date_registry_end': datetime(2015, 9, 22, 0, 0, 0),
             'date_updated': datetime(2014, 9, 21, 3, 10, 7),
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns'],
             'fqdn': 'iheartcli.com',
             'id': 236816922,
             'status': [],
             'tld': 'com'},
            {'authinfo': 'abcdef0002',
             'autorenew': None,
             'contacts': {'admin': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'bill': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'owner': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'reseller': None,
                          'tech': {'handle': 'PXP561-GANDI', 'id': 2920674}},
             'date_created': DateTime('20130410T12:46:05'),
             'date_delete': DateTime('20160507T07:14:00'),
             'date_hold_begin': DateTime('20160410T00:00:00'),
             'date_registry_creation': DateTime('20140410T10:46:04'),
             'date_registry_end': DateTime('20140410T00:00:00'),
             'date_updated': DateTime('20150313T10:30:05'),
             'date_hold_end': DateTime('20151020T20:00:00'),
             'date_pending_delete_end': DateTime('20151119T00:00:00'),
             'date_renew_begin': DateTime('20120101T00:00:00'),
             'date_restore_end': DateTime('20151119T00:00:00'),
             'fqdn': 'cli.sexy',
             'id': 3412062241,
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns', 'gandimail', 'paas'],
             'status': [],
             'tags': [],
             'tld': 'sexy',
             'zone_id': None}]


def info(id):
    domain = dict([(domain['fqdn'], domain) for domain in list({})])
    return domain[id]


def available(domains):

    ret = {}
    for domain in domains:
        if 'unavailable' in domain:
            ret[domain] = 'unavailable'
        elif 'pending' in domain:
            ret[domain] = 'pending'
        else:
            ret[domain] = 'available'

    return ret


def create(domain, params):
    return {'id': 400, 'step': 'WAIT'}


def renew(domain, params):
    return {'id': 400, 'step': 'WAIT'}


def mailbox_list(domain, options):
    return [{'login': 'admin',
             'responder': {'active': False},
             'quota': {'granted': 0, 'used': 233}}]


def mailbox_info(domain, login):
    ret = {'aliases': [],
           'login': 'admin',
           'responder': {'active': False, 'text': None},
           'fallback_email': '',
           'quota': {'granted': 0, 'used': 233}}
    return ret


def mailbox_create(domain, login, params):
    return {'id': 400, 'step': 'WAIT'}


def mailbox_delete(domain, login):
    return {'id': 400, 'step': 'WAIT'}


def mailbox_update(domain, login, params):
    return {'id': 400, 'step': 'WAIT'}


def mailbox_alias_set(domain, login, aliases):
    return {'id': 400, 'step': 'WAIT'}


def mailbox_purge(domain, login):
    return {'id': 400, 'step': 'WAIT'}


def forward_list(domain, options):
    return [{'source': 'admin',
             'destinations': ['admin@cli.sexy', 'grumpy@cat.lol']},
            {'source': 'contact',
             'destinations': ['contact@cli.sexy']}]


def forward_create(domain, source, options):
    return [{'source': source,
             'destinations': options['destinations']}]


def forward_update(domain, source, options):
    return [{'source': source,
             'destinations': options['destinations']}]


def forward_delete(domain, source):
    return True


def zone_record_list(zone_id, version, options=None):
    ret = [{'id': 337085079,
            'name': '*',
            'ttl': 10800,
            'type': 'A',
            'value': '73.246.104.110'},
           {'id': 337085078,
            'name': '@',
            'ttl': 10800,
            'type': 'A',
            'value': '73.246.104.110'},
           {'id': 337085081,
            'name': 'much',
            'ttl': 10800,
            'type': 'A',
            'value': '192.243.24.132'},
           {'id': 337085072,
            'name': 'blog',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'blogs.vip.gandi.net.'},
           {'id': 337085082,
            'name': 'cloud',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'gpaas6.dc0.gandi.net.'},
           {'id': 337085075,
            'name': 'imap',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'access.mail.gandi.net.'},
           {'id': 337085071,
            'name': 'pop',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'access.mail.gandi.net.'},
           {'id': 337085074,
            'name': 'smtp',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'relay.mail.gandi.net.'},
           {'id': 337085073,
            'name': 'webmail',
            'ttl': 10800,
            'type': 'CNAME',
            'value': 'agent.mail.gandi.net.'},
           {'id': 337085077,
            'name': '@',
            'ttl': 10800,
            'type': 'MX',
            'value': '50 fb.mail.gandi.net.'},
           {'id': 337085076,
            'name': '@',
            'ttl': 10800,
            'type': 'MX',
            'value': '10 spool.mail.gandi.net.'}]

    options = options or {}
    options.pop('items_per_page', None)

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
