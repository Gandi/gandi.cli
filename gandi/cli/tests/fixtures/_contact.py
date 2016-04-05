
def list(options):
    return [{'handle': 'AA1-GANDI'},
            {'handle': 'AA2-GANDI'},
            {'handle': 'AA3-GANDI'},
            {'handle': 'AA4-GANDI'},
            {'handle': 'AA5-GANDI'},
            {'handle': 'TEST1-GANDI'},
            {'handle': 'PXP561-GANDI', 'id': 2920674,
             'prepaid': {'amount': '1337.42',
                         'currency': 'EUR'}}
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

    if params['email'] == 'green.goblin@spiderman.org':
        # add an unknown error
        errors.append({'attr': ['Sun, Mercury, Venus, Earth, Mars, Jupiter,'
                                'Saturn, Uranus, Neptune'],
                       'error': '!EC_ENUMIN',
                       'field': 'planet',
                       'field_type': 'Enum',
                       'reason': 'planet: Pluto not in list Sun, Mercury, '
                                 'Venus, Earth, Mars, Jupiter, '
                                 'Saturn, Uranus, Neptune'})

    return errors


def balance(id='PXP561-GANDI'):

    contact = dict([(contact['handle'], contact) for contact in list({})])
    return contact[id]
