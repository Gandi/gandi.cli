import re

from .base import CommandTestCase
from ..fixtures.mocks import MockObject
from gandi.cli.core.base import GandiModule
from gandi.cli.commands import contact


class ContactTestCase(CommandTestCase):

    mocks = [('gandi.cli.commands.contact.webbrowser.open',
              MockObject.blank_func)]

    def test_create_dry_run_ok(self):

        args = []
        inputs = ('0\nPeter\nParker\npeter.parker@spiderman.org\n'
                  'Central Park\n2600\nNew York\nUSA\n555-123-456\n'
                  'plokiploki\nplokiploki\n+011.555123456\napikey0001\n')
        result = self.invoke_with_exceptions(contact.create, args,
                                             input=inputs)
        self.assertEqual(re.sub(r'\[\d+\]', '[1234567890123456]',
                                result.output.strip()), """\
Choose your contact type
0- individual
1- company
2- association
3- public body
4- reseller
: 0
What is your first name: Peter
What is your last name: Parker
What is your email address: peter.parker@spiderman.org
What is your street address: Central Park
What is your zipcode: 2600
Which city: New York
Which country: USA
What is your telephone number: 555-123-456
Please enter your password [1234567890123456]: \
\nRepeat for confirmation: \
\nphone: string '555-123-456' does not match '^\\+\\d{1,3}\\.\\d+$'
What is your telephone number: +011.555123456
Please activate you public api access from gandi website, and get the apikey.
Your handle is PP0000-GANDI, and the password is the one you defined.
What is your production apikey: apikey0001
You already have an apikey defined, if you want to use the newly created \
contact, use the env var : \
\nexport API_KEY=apikey0001""")
        self.assertEqual(result.exit_code, 0)

    def test_create_dry_run_unknown_ok(self):

        args = []
        inputs = ('0\nPeter\nParker\ngreen.goblin@spiderman.org\n'
                  'Central Park\n2600\nNew York\nUSA\n555-123-456\n'
                  'plokiploki\nplokiploki\n+011.555123456\napikey0001\n')
        result = self.invoke_with_exceptions(contact.create, args,
                                             input=inputs)
        self.assertEqual(re.sub(r'\[\d+\]', '[1234567890123456]',
                                result.output.strip()), """\
Choose your contact type
0- individual
1- company
2- association
3- public body
4- reseller
: 0
What is your first name: Peter
What is your last name: Parker
What is your email address: green.goblin@spiderman.org
What is your street address: Central Park
What is your zipcode: 2600
Which city: New York
Which country: USA
What is your telephone number: 555-123-456
Please enter your password [1234567890123456]: \
\nRepeat for confirmation: \
\nphone: string '555-123-456' does not match '^\\+\\d{1,3}\\.\\d+$'
What is your telephone number: +011.555123456
planet: Pluto not in list Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, \
Uranus, Neptune""")
        self.assertEqual(result.exit_code, 0)

    def test_create_ok(self):

        args = []
        inputs = ('0\nPeter\nParker\npeter.parker@spiderman.org\n'
                  'Central Park\n2600\nNew York\nUSA\n+011.555123456\n'
                  'plokiploki\nplokiploki\napikey0001\n')
        result = self.invoke_with_exceptions(contact.create, args,
                                             input=inputs)
        self.assertEqual(re.sub(r'\[\d+\]', '[1234567890123456]',
                                result.output.strip()), """\
Choose your contact type
0- individual
1- company
2- association
3- public body
4- reseller
: 0
What is your first name: Peter
What is your last name: Parker
What is your email address: peter.parker@spiderman.org
What is your street address: Central Park
What is your zipcode: 2600
Which city: New York
Which country: USA
What is your telephone number: +011.555123456
Please enter your password [1234567890123456]: \
\nRepeat for confirmation: \
\nPlease activate you public api access from gandi website, and get the apikey.
Your handle is PP0000-GANDI, and the password is the one you defined.
What is your production apikey: apikey0001
You already have an apikey defined, if you want to use the newly created \
contact, use the env var : \
\nexport API_KEY=apikey0001""")
        self.assertEqual(result.exit_code, 0)

    def test_create_apikey_ok(self):

        args = []
        inputs = ('0\nPeter\nParker\npeter.parker@spiderman.org\n'
                  'Central Park\n2600\nNew York\nUSA\n+011.555123456\n'
                  'plokiploki\nplokiploki\napikey0002\n')

        GandiModule._conffiles = {'global': {}}

        result = self.invoke_with_exceptions(contact.create, args,
                                             input=inputs)
        self.assertEqual(re.sub(r'\[\d+\]', '[1234567890123456]',
                                result.output.strip()), """\
Choose your contact type
0- individual
1- company
2- association
3- public body
4- reseller
: 0
What is your first name: Peter
What is your last name: Parker
What is your email address: peter.parker@spiderman.org
What is your street address: Central Park
What is your zipcode: 2600
Which city: New York
Which country: USA
What is your telephone number: +011.555123456
Please enter your password [1234567890123456]: \
\nRepeat for confirmation: \
\nPlease activate you public api access from gandi website, and get the apikey.
Your handle is PP0000-GANDI, and the password is the one you defined.
What is your production apikey: apikey0002
Will save your apikey into the config file.""")
        self.assertEqual(result.exit_code, 0)

        self.assertTrue('api' in GandiModule._conffiles['global'])

        api_key = GandiModule._conffiles['global']['api'].get('key')
        self.assertEqual(api_key,'apikey0002')
