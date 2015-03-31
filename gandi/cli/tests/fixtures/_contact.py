def list(options):
    return [{'handle': 'AA1-GANDI'},
            {'handle': 'AA2-GANDI'},
            {'handle': 'AA3-GANDI'},
            {'handle': 'AA4-GANDI'},
            {'handle': 'AA5-GANDI'},
            {'handle': 'TEST1-GANDI'},
            ]


def info(id='TEST1-GANDI'):

    contact = dict([(contact['handle'], contact) for contact in list({})])
    return contact[id]
