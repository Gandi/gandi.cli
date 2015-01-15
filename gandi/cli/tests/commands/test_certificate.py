from gandi.cli.commands import certificate

from .base import CommandTestCase


class CertTestCase(CommandTestCase):

    def test_packages(self):

        result = self.runner.invoke(certificate.packages, [])

        #self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, """cert_std_1_0_0
cert_std_w_0_0
cert_std_3_0_0
cert_std_5_0_0
cert_std_10_0_0
cert_std_20_0_0
cert_pro_1_100_0
cert_pro_1_100_SGC
cert_pro_1_10_0
cert_pro_1_250_0
cert_pro_w_250_0
cert_pro_w_250_SGC
cert_bus_1_250_0
cert_bus_1_250_SGC
cert_bus_3_250_0
cert_bus_5_250_0
cert_bus_10_250_0
cert_bus_20_250_0
""")
        self.assertEqual(result.exit_code, 0)

    def test_list(self):

        result = self.runner.invoke(certificate.list, [])

        self.assertEqual(result.output, """cn           : mydomain.name
package      : cert_std_1_0_0
----------
cn           : inter.net
package      : cert_bus_20_250_0
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):

        result = self.runner.invoke(certificate.info, ['inter.net'])

        self.assertEqual(result.output, """cn           : inter.net
date_created : 20140904T14:06:26
date_end     :
package      : cert_bus_20_250_0
status       : valid
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):

        result = self.runner.invoke(certificate.create,
                                    ['--csr', 'dummy_csr',
                                     '--duration', 5,
                                     '--package', 'cert_std_5_0_0'
                                     ])

        self.assertEqual(result.output, '')
        self.assertEqual(result.exit_code, 0)
