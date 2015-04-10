try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime


type_list = list


def package_list(options):
    return [{'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 287,
             'id': 1,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_std_1_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 2,
             'max_domains': 3,
             'min_domains': 1,
             'name': 'cert_std_3_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 289,
             'id': 3,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_std_w_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 1},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 24,
             'id': 4,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_10_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 10000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 34,
             'id': 5,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_100_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 100000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 317,
             'id': 6,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_100_SGC',
             'sgc': 1,
             'trustlogo': 1,
             'warranty': 100000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 7,
             'id': 7,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_250_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 35,
             'id': 8,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_w_250_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 1},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 323,
             'id': 9,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_w_250_SGC',
             'sgc': 1,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 1},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 337,
             'id': 10,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_bus_1_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 338,
             'id': 11,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_bus_1_250_SGC',
             'sgc': 1,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 12,
             'max_domains': 5,
             'min_domains': 1,
             'name': 'cert_std_5_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 13,
             'max_domains': 10,
             'min_domains': 1,
             'name': 'cert_std_10_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 14,
             'max_domains': 20,
             'min_domains': 1,
             'name': 'cert_std_20_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 15,
             'max_domains': 3,
             'min_domains': 1,
             'name': 'cert_bus_3_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 16,
             'max_domains': 5,
             'min_domains': 1,
             'name': 'cert_bus_5_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 17,
             'max_domains': 10,
             'min_domains': 1,
             'name': 'cert_bus_10_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 18,
             'max_domains': 20,
             'min_domains': 1,
             'name': 'cert_bus_20_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0}
            ]


def list(options):
    return [{'trustlogo': False,
             'assumed_name': None,
             'package': 'cert_std_1_0_0',
             'order_number': None,
             'altnames': [],
             'trustlogo_token': {'mydomain.name': 'adadadadad'},
             'date_incorporation': None,
             'card_pay_trustlogo': False,
             'contact': 'TEST1-GANDI',
             'date_start': None,
             'ida_email': None,
             'business_category': None,
             'cert': None,
             'date_end': None,
             'status': 'pending',
             'csr': '-----BEGIN CERTIFICATE REQUEST-----\n'
                    'MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX'
                    '...'
                    'K+I=\n-----END CERTIFICATE REQUEST-----',
             'date_updated': DateTime('20140904T14:06:26'),
             'software': 2,
             'id': 701,
             'joi_locality': None,
             'date_created': DateTime('20140904T14:06:26'),
             'cn': 'mydomain.name',
             'sha_version': 1,
             'middleman': '',
             'ida_tel': None,
             'ida_fax': None,
             'comodo_id': None,
             'joi_country': None,
             'joi_state': None},
            {'trustlogo': False,
             'assumed_name': None,
             'package': 'cert_bus_20_250_0',
             'order_number': None,
             'altnames': [],
             'trustlogo_token': {'inter.net': 'adadadadad'},
             'date_incorporation': None,
             'card_pay_trustlogo': False,
             'contact': 'TEST1-GANDI',
             'date_start': None,
             'ida_email': None,
             'business_category': None,
             'cert': None,
             'date_end': None,
             'status': 'valid',
             'csr': '-----BEGIN CERTIFICATE REQUEST-----\n'
                    'MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX'
                    '...'
                    'K+I=\n-----END CERTIFICATE REQUEST-----',
             'date_updated': DateTime('20140904T14:06:26'),
             'software': 2,
             'id': 706,
             'joi_locality': None,
             'date_created': DateTime('20140904T14:06:26'),
             'cn': 'inter.net',
             'sha_version': 1,
             'middleman': '',
             'ida_tel': None,
             'ida_fax': None,
             'comodo_id': None,
             'joi_country': None,
             'joi_state': None}
            ]


def info(id):
    cert = dict([(cert['id'], cert) for cert in list({})])
    return cert[id]


def create(*args):
    return {'id': 1}


def hosted_list(options):
    fqdns_id = {'test1.domain.fr': [1, 2],
                'test2.domain.fr': [3],
                'test3.domain.fr': [4],
                'test4.domain.fr': [5],
                '*.domain.fr': [6]}

    ret = [{'date_created': DateTime('20150407T00:00:00'),
            'date_expire': DateTime('20160316T00:00:00'),
            'id': 1,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'SSL/CN=test1.domain.fr'},
           {'date_created': DateTime('20150407T00:00:00'),
            'date_expire': DateTime('20160316T00:00:00'),
            'id': 2,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'SSL/CN=test1.domain.fr'},
           {'date_created': DateTime('20150408T00:00:00'),
            'date_expire': DateTime('20160408T00:00:00'),
            'id': 3,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'SSL/CN=test2.domain.fr'},
           {'date_created': DateTime('20150408T00:00:00'),
            'date_expire': DateTime('20160408T00:00:00'),
            'id': 4,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'SSL/CN=test3.domain.fr'},
           {'date_created': DateTime('20150408T00:00:00'),
            'date_expire': DateTime('20160408T00:00:00'),
            'id': 5,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'SSL/CN=test4.domain.fr'},
           {'date_created': DateTime('20150409T00:00:00'),
            'date_expire': DateTime('20160409T00:00:00'),
            'id': 6,
            'state': u'created',
            'subject': u'/OU=Domain Control Validated/OU=Gandi Standard '
                        'Wildcard SSL/CN=*.domain.fr'}]

    options.pop('items_per_page', None)
    fqdns = options.pop('fqdns', None)

    if fqdns:
        if not isinstance(fqdns, (type_list, tuple)):
            fqdns = [fqdns]
        for fqdn in fqdns:
            options.setdefault('id', []).extend(fqdns_id.get(fqdn, []))

    def compare(hc, option):
        if isinstance(option, (type_list, tuple)):
            return hc in option
        return hc == option

    for fkey in options:
        ret = [hc for hc in ret if compare(hc[fkey], options[fkey])]

    return ret


def hosted_info(id):
    additionals = {
        1: {'fqdns': [{'type': u'cn', 'name': u'test1.domain.fr'}],
            'related_vhosts': [{'service_id': 1,
                                'type': 'paas',
                                'id': 1,
                                'name': 'test1.domain.fr'}]},
        2: {'fqdns': [{'type': u'cn', 'name': u'test1.domain.fr'}],
            'related_vhosts': [{'service_id': 1,
                                'type': 'paas',
                                'id': 1,
                                'name': 'test1.domain.fr'}]},
        3: {'fqdns': [{'type': u'cn', 'name': u'test2.domain.fr'}],
            'related_vhosts': []},
        4: {'fqdns': [{'type': u'cn', 'name': u'test3.domain.fr'}],
            'related_vhosts': []},
        5: {'fqdns': [{'type': u'cn', 'name': u'test4.domain.fr'}],
            'related_vhosts': []},
        6: {'fqdns': [{'type': u'cn', 'name': u'*.domain.fr'}],
            'related_vhosts': [{'service_id': 2,
                                'type': 'paas',
                                'id': 2,
                                'name': '*.domain.fr'}]}}
    def additional(hc):
        hc.update(additionals[hc['id']])
        return hc

    hc = dict([(hc['id'], additional(hc)) for hc in hosted_list({})])
    return hc[id]
