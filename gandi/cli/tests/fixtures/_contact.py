
def list(options):
    return [{'handle': 'AA1-GANDI'},
            {'handle': 'AA2-GANDI'},
            {'handle': 'AA3-GANDI'},
            {'handle': 'AA4-GANDI'},
            {'handle': 'AA5-GANDI'},
            {'handle': 'TEST1-GANDI'},
            {'handle': 'PXP561-GANDI', 'id': 2920674},
            ]


def info(id='PXP561-GANDI'):

    contact = dict([(contact['handle'], contact) for contact in list({})])
    return contact[id]


def create(params):
    return {'handle': 'PP0000-GANDI'}


def create_dry_run(params):

    errors = []
    if params['phone'] == '555-123-456':
        errors.append({'attr': None,
                       'error': '!EC_STRMATCH',
                       'field': 'phone',
                       'field_type': 'String',
                       'reason': "phone: string '555-123-456' does not "
                                 "match '^\\+\\d{1,3}\\.\\d+$'"})

    return errors
