try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime


def list(options):

    return [{'date_created': DateTime('20150915T18:29:16'),
             'date_start': None,
             'date_updated': DateTime('20150915T18:29:17'),
             'errortype': None,
             'eta': -1863666,
             'id': 100100,
             'infos': {'extras': {},
                       'id': '',
                       'label': 'iheartcli.com',
                       'product_action': 'renew',
                       'product_name': 'com',
                       'product_type': 'domain',
                       'quantity': ''},
             'last_error': None,
             'params': {'auth_id': 99999999,
                        'current_year': 2015,
                        'domain': 'iheartcli.com',
                        'domain_id': 1234567,
                        'duration': 1,
                        'param_type': 'domain',
                        'remote_addr': '127.0.0.1',
                        'session_id': 2920674,
                        'tld': 'com',
                        'tracker_id': '621cb9f4-472d-4cc1-b4b9-b18cc61e2914'},
             'session_id': 2920674,
             'source': 'PXP561-GANDI',
             'step': 'BILL',
             'type': 'domain_renew'},
            {'date_created': DateTime('20150505T00:00:00'),
             'date_start': None,
             'date_updated': DateTime('20150505T00:00:00'),
             'errortype': None,
             'eta': 0,
             'id': 100200,
             'infos': {'extras': {},
                       'id': '',
                       'label': '',
                       'product_action': 'billing_prepaid_add_money',
                       'product_name': '',
                       'product_type': 'corporate',
                       'quantity': ''},
             'last_error': None,
             'params': {'amount': 50.0,
                        'auth_id': 99999999,
                        'param_type': 'prepaid_add_money',
                        'prepaid_id': 100000,
                        'remote_addr': '127.0.0.1',
                        'tracker_id': 'ab0e5e67-6ca7-4afc-8311-f20080f15cf1'},
             'session_id': 9844958,
             'source': 'PXP561-GANDI',
             'step': 'BILL',
             'type': 'billing_prepaid_add_money'}]


def info(id):

    if id == 200:
        return {'step': 'DONE'}

    if id == 300:
        return {'step': 'DONE', 'vm_id': 9000}

    if id == 400:
        return {'step': 'DONE'}

    return [oper for oper in list({}) if oper['id'] == id][0]
