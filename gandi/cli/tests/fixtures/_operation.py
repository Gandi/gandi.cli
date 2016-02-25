try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime

type_list = list


def list(options):

    ret = [{'date_created': DateTime('20150915T18:29:16'),
            'date_start': None,
            'date_updated': DateTime('20150915T18:29:17'),
            'errortype': None,
            'eta': -1863666,
            'id': 100100,
            'cert_id': None,
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
            'cert_id': None,
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
            'type': 'billing_prepaid_add_money'},
           {'step': 'RUN',
            'cert_id': 710,
            'id': 100300,
            'type': 'certificate_update',
            'params': {'cert_id': 710,
                       'param_type': 'certificate_update',
                       'prepaid_id': 100000,
                       'inner_step': 'comodo_oper_updated',
                       'dcv_method': 'email',
                       'csr': '-----BEGIN CERTIFICATE REQUEST-----'
                              'MIICxjCCAa4CAQAwgYAxCzAJBgNVBAYTAkZSMQsw'
                              '0eWfyJJTOypoToCtdGoye507GOsgIysfRWaExay5'
                              '-----END CERTIFICATE REQUEST-----',
                       'remote_addr': '127.0.0.1'}},
           {'step': 'RUN',
            'cert_id': 706,
            'id': 100302,
            'type': 'certificate_update',
            'params': {'cert_id': 706,
                       'param_type': 'certificate_update',
                       'prepaid_id': 100000,
                       'inner_step': 'comodo_oper_updated',
                       'dcv_method': 'dns',
                       'csr': '-----BEGIN CERTIFICATE REQUEST-----'
                              'MIICxjCCAa4CAQAwgYAxCzAJBgNVBAYTAkZSMQsw'
                              '0eWfyJJTOypoToCtdGoye507GOsgIysfRWaExay5'
                              '-----END CERTIFICATE REQUEST-----',
                       'remote_addr': '127.0.0.1'}},
           {'step': 'WAIT',
            'cert_id': 701,
            'id': 100303,
            'type': 'certificate_update',
            'params': {'cert_id': 706,
                       'param_type': 'certificate_update',
                       'prepaid_id': 100000,
                       'inner_step': 'check_email_sent',
                       'dcv_method': 'dns',
                       'remote_addr': '127.0.0.1'}},
           ]

    options.pop('sort_by', None)
    options.pop('items_per_page', None)

    def compare(op, option):
        if isinstance(option, (type_list, tuple)):
            return op in option
        return op == option

    for fkey in options:
        ret = [op for op in ret if compare(op[fkey], options[fkey])]

    return ret


def info(id):

    if id == 200:
        return {'step': 'DONE'}

    if id == 300:
        return {'step': 'DONE', 'vm_id': 9000}

    if id == 400:
        return {'step': 'DONE'}

    if id == 600:
        return {'step': 'DONE', 'type': 'certificate_update',
                'params': {'cert_id': 710,
                           'param_type': 'certificate_update',
                           'prepaid_id': 100000,
                           'remote_addr': '127.0.0.1'}}

    return [oper for oper in list({}) if oper['id'] == id][0]
