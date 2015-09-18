""" Contact namespace commands. """

import click
import time
import webbrowser

# define unicode for python3
try:
    unicode
except NameError:
    unicode = str

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import randomstring
from gandi.cli.core.params import pass_gandi


FIELDS = (('type', 'Choose your contact type',
           {'valid': ((0, 'individual'),
                      (1, 'company'),
                      (2, 'association'),
                      (3, 'public body'),
                      (4, 'reseller')),
            'convert': int}),
          ('given', 'What is your first name', None),
          ('family', 'What is your last name', None),
          ('orgname', 'What is your company name',
           {'display': lambda contact_: contact_['type'] != 0}),
          ('email', 'What is your email address', None),
          ('streetaddr', 'What is your street address', None),
          ('zip', 'What is your zipcode', None),
          ('city', 'Which city', None),
          ('country', 'Which country', None),
          ('phone', 'What is your telephone number', None))


FIELDS_POSITION = dict([(j, i) for i, j in enumerate(
                        [field[0] for field in FIELDS])])


def ask_field(gandi, contact, field, label, checks):
    valid = display = None
    convert = unicode

    if checks:
        valid = checks.get('valid')
        convert = checks.get('convert', unicode)
        display = checks.get('display')

    if display and not display(contact):
        return

    if not valid:
        contact[field] = convert(click.prompt(label))
    elif isinstance(valid, (tuple, list)):
        valid_keys = [unicode(val) for val, _ in valid]
        value = None
        gandi.echo(label)
        while value not in valid_keys:
            for key, val in valid:
                gandi.echo('%s- %s' % (key, val))
            value = click.prompt('')
        contact[field] = convert(value)


@cli.command()
@pass_gandi
def create(gandi):
    """ Create a new contact.
    """
    contact = {}

    for field, label, checks in FIELDS:
        ask_field(gandi, contact, field, label, checks)

    default_pwd = randomstring(16)
    contact['password'] = click.prompt('Please enter your password',
                                       hide_input=True,
                                       confirmation_prompt=True,
                                       default=default_pwd)

    result = True
    while result:
        result = gandi.contact.create_dry_run(contact)

        # display errors
        for err in result:
            gandi.echo(err['reason'])
            field = err['field']

            if field not in FIELDS_POSITION:
                return

            desc = FIELDS[FIELDS_POSITION.get(field)]
            ask_field(gandi, contact, *desc)

    result = gandi.contact.create(contact)
    handle = result['handle']

    gandi.echo('Please activate you public api access from gandi website, and '
               'get the apikey.')
    gandi.echo('Your handle is %s, and the password is the one you defined.' %
               handle)

    # open new browser window
    webbrowser.open('https://www.gandi.net/admin/api_key')
    # just to avoid missing the next question in webbrowser stderr
    time.sleep(1)

    # get the apikey from shell
    apikey = None
    while not apikey:
        apikey = click.prompt('What is your production apikey')

    caller = gandi.get('api.key')
    # save apikey in the conf if none defined else display an help on how to
    # use it
    if caller:
        gandi.echo('You already have an apikey defined, if you want to use the'
                   ' newly created contact, use the env var : ')
        gandi.echo('export API_KEY=%s' % apikey)
    else:
        gandi.echo('Will save your apikey into the config file.')
        gandi.configure(True, 'api.key', apikey)

    return handle
