def list(options):
    return [{'fqdn': 'iheartcli.com',
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns'],
             'zone_id': 424242,
             'tags': 'bla',
             'contacts': {'owner': {'handle': 'AA1-GANDI'},
                          'admin': {'handle': 'AA2-GANDI'},
                          'bill': {'handle': 'AA3-GANDI'},
                          'reseller': {'handle': 'AA4-GANDI'},
                          'tech': {'handle': 'AA5-GANDI'}}},
            {'fqdn': 'cli.sexy',
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns'],
             'zone_id': 424242,
             'tags': 'bli',
             'contacts': {'owner': {'handle': 'AA1-GANDI'},
                          'admin': {'handle': 'AA2-GANDI'},
                          'bill': {'handle': 'AA3-GANDI'},
                          'reseller': {'handle': 'AA4-GANDI'},
                          'tech': {'handle': 'AA5-GANDI'}}},
            ]


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


def create(*args):
    return {'id': 200}
