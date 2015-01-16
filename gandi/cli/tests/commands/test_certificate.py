from gandi.cli.commands import certificate

from .base import CommandTestCase


class CertTestCase(CommandTestCase):

    def test_packages(self):

        result = self.runner.invoke(certificate.packages, [])

        #self.assertEqual(result.exit_code, 0)
        wanted = (
"""/!\ "gandi certificate packages" is deprecated.
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
""")

        self.assertEqual(result.output, wanted)

        self.assertEqual(result.exit_code, 0)

    def test_list(self):

        result = self.runner.invoke(certificate.list, [])

        self.assertEqual(result.output, """cn           : mydomain.name
plan         : Standard Single Domain
----------
cn           : inter.net
plan         : Business Multi Domain
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.runner.invoke(certificate.info, ['inter.net'])

        self.assertEqual(result.output, """cn           : inter.net
date_created : 20140904T14:06:26
date_end     :
plan         : Business Multi Domain
status       : valid
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

        result = self.runner.invoke(certificate.create,
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
