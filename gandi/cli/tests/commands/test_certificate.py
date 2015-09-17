# -*- coding: utf-8 -*-
import re

from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import certificate


class CertTestCase(CommandTestCase):

    def test_packages(self):

        result = self.invoke_with_exceptions(certificate.packages, [])

        wanted = ("""/!\ "gandi certificate packages" is deprecated.
Please use "gandi certificate plans".
Description            | Name               | Max altnames | Type
-----------------------+--------------------+--------------+-----
Standard Single Domain | cert_std_1_0_0     | 1            | std 
Standard Wildcard      | cert_std_w_0_0     | 1            | std 
Standard Multi Domain  | cert_std_3_0_0     | 3            | std 
Standard Multi Domain  | cert_std_5_0_0     | 5            | std 
Standard Multi Domain  | cert_std_10_0_0    | 10           | std 
Standard Multi Domain  | cert_std_20_0_0    | 20           | std 
Pro Single Domain      | cert_pro_1_10_0    | 1            | pro 
Pro Single Domain      | cert_pro_1_100_0   | 1            | pro 
Pro Single Domain      | cert_pro_1_100_SGC | 1            | pro 
Pro Single Domain      | cert_pro_1_250_0   | 1            | pro 
Pro Wildcard           | cert_pro_w_250_0   | 1            | pro 
Pro Wildcard           | cert_pro_w_250_SGC | 1            | pro 
Business Single Domain | cert_bus_1_250_0   | 1            | bus 
Business Single Domain | cert_bus_1_250_SGC | 1            | bus 
Business Multi Domain  | cert_bus_3_250_0   | 3            | bus 
Business Multi Domain  | cert_bus_5_250_0   | 5            | bus 
Business Multi Domain  | cert_bus_10_250_0  | 10           | bus 
Business Multi Domain  | cert_bus_20_250_0  | 20           | bus 
""")  # noqa

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    def test_plans(self):

        result = self.invoke_with_exceptions(certificate.plans, [])

        wanted = ("""\
Description            | Max altnames | Type | Warranty
-----------------------+--------------+------+---------
Standard Single Domain | 1            | std  | 0       
Standard Wildcard      | 1            | std  | 0       
Standard Multi Domain  | 3            | std  | 0       
Standard Multi Domain  | 5            | std  | 0       
Standard Multi Domain  | 10           | std  | 0       
Standard Multi Domain  | 20           | std  | 0       
Pro Single Domain      | 1            | pro  | 10,000  
Pro Single Domain      | 1            | pro  | 100,000 
Pro Single Domain      | 1            | pro  | 100,000 
Pro Single Domain      | 1            | pro  | 250,000 
Pro Wildcard           | 1            | pro  | 250,000 
Pro Wildcard           | 1            | pro  | 250,000 
Business Single Domain | 1            | bus  | 250,000 
Business Single Domain | 1            | bus  | 250,000 
Business Multi Domain  | 3            | bus  | 250,000 
Business Multi Domain  | 5            | bus  | 250,000 
Business Multi Domain  | 10           | bus  | 250,000 
Business Multi Domain  | 20           | bus  | 250,000 
""")  # noqa

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    def test_list(self):

        result = self.invoke_with_exceptions(certificate.list, [])

        self.assertEqual(result.output, """cn           : mydomain.name
plan         : Standard Single Domain
----------
cn           : inter.net
plan         : Business Multi Domain
----------
cn           : lol.cat
plan         : Standard Single Domain
""")
        self.assertEqual(result.exit_code, 0)

    def test_list_all(self):

        args = ['--id', '--status', '--dates', '--altnames', '--csr',
                '--cert']
        result = self.invoke_with_exceptions(certificate.list, args)

        self.assertEqual(result.output, """cn           : mydomain.name
plan         : Standard Single Domain
id           : 701
status       : pending
date_created : 20140904T14:06:26
date_end     :
csr          : -----BEGIN CERTIFICATE REQUEST-----
MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX...K+I=
-----END CERTIFICATE REQUEST-----
----------
cn           : inter.net
plan         : Business Multi Domain
id           : 706
status       : valid
date_created : 20140904T14:06:26
date_end     :
csr          : -----BEGIN CERTIFICATE REQUEST-----
MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX...K+I=
-----END CERTIFICATE REQUEST-----
----------
cn           : lol.cat
plan         : Standard Single Domain
id           : 710
status       : valid
date_created : 20150318T00:00:00
date_end     : 20160318T00:00:00
csr          : -----BEGIN CERTIFICATE REQUEST-----
MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX...K+I=
-----END CERTIFICATE REQUEST-----
cert         : \
\n-----BEGIN CERTIFICATE-----
MIIE5zCCA8+gAwIBAgIQAkC4TU9JG8wqhf4FCrsNGTANBgkqhkiG9w0BAQsFADBf
MQswCQYDVQQGEwJGUjEOMAwGA1UECBMFUGFyaXMxDj...tU6XzbS6/s2D1/N1wWO
OCD/V3XAROtKr1a0mtJ8n7SZyzr0j3weRbN7nV24RDQ6d4+GHy5zZstKyDrTknlu
yyZuDAAYAQJ+nrL5p1gxVNwj1f5XKFk=
-----END CERTIFICATE-----
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.invoke_with_exceptions(certificate.info, ['inter.net'])

        self.assertEqual(result.output, """cn           : inter.net
date_created : 20140904T14:06:26
date_end     :
plan         : Business Multi Domain
status       : valid
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_all(self):

        args = ['inter.net', '--id', '--altnames', '--csr', '--cert']
        result = self.invoke_with_exceptions(certificate.info, args)

        self.assertEqual(result.output, """cn           : inter.net
date_created : 20140904T14:06:26
date_end     :
plan         : Business Multi Domain
status       : valid
id           : 706
csr          : -----BEGIN CERTIFICATE REQUEST-----
MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX...K+I=
-----END CERTIFICATE REQUEST-----
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        csr = '''-----BEGIN CERTIFICATE REQUEST-----
MIICWjCCAUICAQAwFTETMBEGA1UEAwwKZG9tYWluLnRsZDCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAKYPfDoiWuWDwJb+fZhOHA++9yYy1BbxnY729hSd
/P12kw1HeIL5CGIhZLpJrwRQmLPTlJ0VttFaqpNm7mEISr+GMJzEWBTyD8750hbW
bXwZBcsWi8AsOsnT+sh/cTKGlJctA346HKU3tLlZsvI4ecfnlIZk5Yefgf+78abz
SzSV47gPDUNQvGIzP9QPE4bEFu5NjdxPg3ylaQ5cv8iiWHn4iUCRXlxxNfHmH7xE
ysFlsD6KnKjR5eYLKBcATeqopGPi72KlcDn5lmtdWsd9aGSl5KlkKQC497buqjbr
H31lMAGAC7At6S7AF5GIT5KGjN6KyPrzUOn7FrhNUcnpUQMCAwEAAaAAMA0GCSqG
SIb3DQEBCwUAA4IBAQCBM6wc9DfsI1htRhAz7/RfOIn7kb6LygOSEgfb757My+60
N/WP9ndpmob0PW18B1vXBloZEkO/aNTXCGAIPJXRkeTYVhEE2B7K3pc9IiNmLxXC
3b2cwUjgmNw9wmFZ4AuHqzWHevqix3m7Acpkl5ugcCsTVOX3mx84MSguSC+5AWfm
DG0VmOWZ0tWjyZuKgtoXgHnH3whEac+pM7M3J+z94/msO9hnpUOQNt4XALEoONrv
+xE1FDGhRJAx9AYOtTBQSFLqKB4D6W2hhDVLirxQuJ/lC/l8tyEu96ggfDRrMXE4
v0L9Vc0443fop+UbFCabF0NWM6rJ31Nlv7s3mQIA
-----END CERTIFICATE REQUEST-----'''

        result = self.invoke_with_exceptions(certificate.create,
                                             ['--csr', csr,
                                              '--duration', 5,
                                              '--max-altname', '5',
                                              ])

        wanted = '''The certificate create operation is 1
You can follow it with:
$ gandi certificate follow 1
When the operation is DONE, you can retrieve the .crt with:
$ gandi certificate export "domain.tld"
'''

        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_create_package_deprecated(self):
        csr = '''-----BEGIN CERTIFICATE REQUEST-----
MIICWjCCAUICAQAwFTETMBEGA1UEAwwKZG9tYWluLnRsZDCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAKYPfDoiWuWDwJb+fZhOHA++9yYy1BbxnY729hSd
/P12kw1HeIL5CGIhZLpJrwRQmLPTlJ0VttFaqpNm7mEISr+GMJzEWBTyD8750hbW
bXwZBcsWi8AsOsnT+sh/cTKGlJctA346HKU3tLlZsvI4ecfnlIZk5Yefgf+78abz
SzSV47gPDUNQvGIzP9QPE4bEFu5NjdxPg3ylaQ5cv8iiWHn4iUCRXlxxNfHmH7xE
ysFlsD6KnKjR5eYLKBcATeqopGPi72KlcDn5lmtdWsd9aGSl5KlkKQC497buqjbr
H31lMAGAC7At6S7AF5GIT5KGjN6KyPrzUOn7FrhNUcnpUQMCAwEAAaAAMA0GCSqG
SIb3DQEBCwUAA4IBAQCBM6wc9DfsI1htRhAz7/RfOIn7kb6LygOSEgfb757My+60
N/WP9ndpmob0PW18B1vXBloZEkO/aNTXCGAIPJXRkeTYVhEE2B7K3pc9IiNmLxXC
3b2cwUjgmNw9wmFZ4AuHqzWHevqix3m7Acpkl5ugcCsTVOX3mx84MSguSC+5AWfm
DG0VmOWZ0tWjyZuKgtoXgHnH3whEac+pM7M3J+z94/msO9hnpUOQNt4XALEoONrv
+xE1FDGhRJAx9AYOtTBQSFLqKB4D6W2hhDVLirxQuJ/lC/l8tyEu96ggfDRrMXE4
v0L9Vc0443fop+UbFCabF0NWM6rJ31Nlv7s3mQIA
-----END CERTIFICATE REQUEST-----'''

        result = self.invoke_with_exceptions(certificate.create,
                                             ['--csr', csr,
                                              '--duration', 5,
                                              '--package', 'cert_std_1_0_0',
                                              ])

        wanted = '''\
/!\\ Using --package is deprecated, please replace it by --type (in std, pro \
or bus) and --max-altname to set the max number of altnames.
The certificate create operation is 1
You can follow it with:
$ gandi certificate follow 1
When the operation is DONE, you can retrieve the .crt with:
$ gandi certificate export "domain.tld"
'''

        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_create_no_csr(self):
        result = self.invoke_with_exceptions(certificate.create,
                                             ['--duration', 5,
                                              '--max-altname', '5',
                                              ])

        wanted = """You need a CSR or a CN to create a certificate.
"""

        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_create_no_package_and_option(self):
        csr = '''-----BEGIN CERTIFICATE REQUEST-----
MIICWjCCAUICAQAwFTETMBEGA1UEAwwKZG9tYWluLnRsZDCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAKYPfDoiWuWDwJb+fZhOHA++9yYy1BbxnY729hSd
/P12kw1HeIL5CGIhZLpJrwRQmLPTlJ0VttFaqpNm7mEISr+GMJzEWBTyD8750hbW
bXwZBcsWi8AsOsnT+sh/cTKGlJctA346HKU3tLlZsvI4ecfnlIZk5Yefgf+78abz
SzSV47gPDUNQvGIzP9QPE4bEFu5NjdxPg3ylaQ5cv8iiWHn4iUCRXlxxNfHmH7xE
ysFlsD6KnKjR5eYLKBcATeqopGPi72KlcDn5lmtdWsd9aGSl5KlkKQC497buqjbr
H31lMAGAC7At6S7AF5GIT5KGjN6KyPrzUOn7FrhNUcnpUQMCAwEAAaAAMA0GCSqG
SIb3DQEBCwUAA4IBAQCBM6wc9DfsI1htRhAz7/RfOIn7kb6LygOSEgfb757My+60
N/WP9ndpmob0PW18B1vXBloZEkO/aNTXCGAIPJXRkeTYVhEE2B7K3pc9IiNmLxXC
3b2cwUjgmNw9wmFZ4AuHqzWHevqix3m7Acpkl5ugcCsTVOX3mx84MSguSC+5AWfm
DG0VmOWZ0tWjyZuKgtoXgHnH3whEac+pM7M3J+z94/msO9hnpUOQNt4XALEoONrv
+xE1FDGhRJAx9AYOtTBQSFLqKB4D6W2hhDVLirxQuJ/lC/l8tyEu96ggfDRrMXE4
v0L9Vc0443fop+UbFCabF0NWM6rJ31Nlv7s3mQIA
-----END CERTIFICATE REQUEST-----'''

        result = self.invoke_with_exceptions(certificate.create,
                                             ['--csr', csr,
                                              '--duration', 5,
                                              '--max-altname', '5',
                                              '--package', 'cert_std_1_0_0',
                                              ])

        wanted = """Please do not use --package at the same time you use \
--type, --max-altname or --warranty.
"""

        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_create_warranty(self):
        csr = '''-----BEGIN CERTIFICATE REQUEST-----
MIICWjCCAUICAQAwFTETMBEGA1UEAwwKZG9tYWluLnRsZDCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAKYPfDoiWuWDwJb+fZhOHA++9yYy1BbxnY729hSd
/P12kw1HeIL5CGIhZLpJrwRQmLPTlJ0VttFaqpNm7mEISr+GMJzEWBTyD8750hbW
bXwZBcsWi8AsOsnT+sh/cTKGlJctA346HKU3tLlZsvI4ecfnlIZk5Yefgf+78abz
SzSV47gPDUNQvGIzP9QPE4bEFu5NjdxPg3ylaQ5cv8iiWHn4iUCRXlxxNfHmH7xE
ysFlsD6KnKjR5eYLKBcATeqopGPi72KlcDn5lmtdWsd9aGSl5KlkKQC497buqjbr
H31lMAGAC7At6S7AF5GIT5KGjN6KyPrzUOn7FrhNUcnpUQMCAwEAAaAAMA0GCSqG
SIb3DQEBCwUAA4IBAQCBM6wc9DfsI1htRhAz7/RfOIn7kb6LygOSEgfb757My+60
N/WP9ndpmob0PW18B1vXBloZEkO/aNTXCGAIPJXRkeTYVhEE2B7K3pc9IiNmLxXC
3b2cwUjgmNw9wmFZ4AuHqzWHevqix3m7Acpkl5ugcCsTVOX3mx84MSguSC+5AWfm
DG0VmOWZ0tWjyZuKgtoXgHnH3whEac+pM7M3J+z94/msO9hnpUOQNt4XALEoONrv
+xE1FDGhRJAx9AYOtTBQSFLqKB4D6W2hhDVLirxQuJ/lC/l8tyEu96ggfDRrMXE4
v0L9Vc0443fop+UbFCabF0NWM6rJ31Nlv7s3mQIA
-----END CERTIFICATE REQUEST-----'''

        result = self.invoke_with_exceptions(certificate.create,
                                             ['--csr', csr,
                                              '--duration', 5,
                                              '--max-altname', '5',
                                              '--type', 'std',
                                              '--warranty', '250',
                                              ])

        wanted = """The warranty can only be specified for pro certificates.
"""

        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_export_ok(self):
        args = ['lol.cat']
        with mock.patch('gandi.cli.commands.certificate.open',
                        create=True) as mock_open:
            mock_open.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(certificate.export, args)

        wanted = """wrote lol.cat.crt
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_export_exists(self):
        args = ['lol.cat']
        with mock.patch('gandi.cli.commands.certificate.os.path.isfile',
                        create=True) as mock_isfile:
            mock_isfile.return_value = True

            result = self.invoke_with_exceptions(certificate.export, args)

        wanted = """The file lol.cat.crt already exists.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_export_nothing(self):
        args = ['inter.net']
        result = self.invoke_with_exceptions(certificate.export, args)

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_export_intermediate_ok(self):
        args = ['lol.cat', '-i']
        with mock.patch('gandi.cli.commands.certificate.open',
                        create=True) as mock_open:
            mock_open.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(certificate.export, args)

        wanted = """wrote lol.cat.crt
wrote lol.cat.inter.crt
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_update(self):
        args = ['inter.net']
        result = self.invoke_with_exceptions(certificate.update, args)

        wanted = """\
openssl req -new -newkey rsa:2048 -sha256 -nodes -out inter.net.csr \
-keyout inter.net.key -subj "/CN=inter.net"
The certificate update operation is 400
You can follow it with:
$ gandi certificate follow 400
When the operation is DONE, you can retrieve the .crt with:
$ gandi certificate export "inter.net"
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_follow(self):
        args = ['600']
        result = self.invoke_with_exceptions(certificate.follow, args)

        wanted = """\
type        : certificate_update
step        : DONE
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_change_dcv(self):
        args = ['lol.cat', '--dcv-method', 'dns']
        result = self.invoke_with_exceptions(certificate.change_dcv, args)

        wanted = """\
You have to add these records in your domain zone :
920F78CCE11DA7D9554.lol.cat. 10800 IN CNAME AD6A9D35FF5BD9FB03A41.comodoca.com.
"""
        self.assertEqual(result.output, wanted)
        self.assertEqual(result.exit_code, 0)

    def test_resend_dcv(self):
        args = ['lol.cat']
        result = self.invoke_with_exceptions(certificate.resend_dcv, args)

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)

    def test_delete_force(self):
        args = ['lol.cat', '--force']
        result = self.invoke_with_exceptions(certificate.delete, args)

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(output, """\
Deleting your certificate.
\rProgress: [###] 100.00%  00:00:00  \
\nYour certificate 710 has been deleted.""")
        self.assertEqual(result.exit_code, 0)
