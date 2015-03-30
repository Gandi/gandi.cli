try:
    from xmlrpc.client import DateTime
except ImportError:
    from xmlrpclib import DateTime


def list(options):
    return [{'authinfo': 'abcdef0001',
             'date_created': DateTime('20100922T15:06:18'),
             'date_delete': DateTime('20151019T19:14:00'),
             'date_hold_begin': DateTime('20150922T22:00:00'),
             'date_registry_creation': DateTime('20100922T13:06:16'),
             'date_registry_end': DateTime('20150922T00:00:00'),
             'date_updated': DateTime('20140921T03:10:07'),
             'fqdn': 'smurfies.com',
             'id': 236816922,
             'status': [],
             'tld': 'm'},
            {'authinfo': 'abcdef0002',
             'date_created': DateTime('20130410T12:46:05'),
             'date_delete': DateTime('20160507T07:14:00'),
             'date_hold_begin': DateTime('20160410T00:00:00'),
             'date_registry_creation': DateTime('20140410T10:46:04'),
             'date_registry_end': DateTime('20140410T00:00:00'),
             'date_updated': DateTime('20150313T10:30:05'),
             'fqdn': 'roboperk.io',
             'id': 3412062241,
             'status': [],
             'tld': 'io'}]


def info(options):

    ret = {'authinfo': 'abcdef0002',
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
           'fqdn': 'roboperk.io',
           'id': 3412062241,
           'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                           'c.dns.gandi.net'],
           'services': ['gandidns', 'gandimail', 'paas'],
           'status': [],
           'tags': [],
           'tld': 'io',
           'zone_id': 431190141}

    return ret
