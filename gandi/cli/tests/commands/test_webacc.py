# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from .base import CommandTestCase
from gandi.cli.commands import webacc


class WebaccTestCase(CommandTestCase):

    def test_list(self):
        result = self.invoke_with_exceptions(webacc.list, [])

        self.assertEqual(result.output, """\
name          : webacc01
state         : running
ssl           : Disable
Vhosts :
Backends :
\tBackend with ip address 195.142.160.181 no longer exists.
\tYou should remove it.
\tip            : 195.142.160.181
\tport          : 80
\tstate         : running

----
name          : testwebacc
state         : running
ssl           : Disable
Vhosts :
\tvhost         : pouet.iheartcli.com
\tssl           : Disable

Backends :
\tname          : server01
\tip            : 95.142.160.181
\tport          : 80
\tstate         : running

""")
        self.assertEqual(result.exit_code, 0)

    def test_list_output_json(self):
        args = ['--format', 'json']
        result = self.invoke_with_exceptions(webacc.list, args)

        self.assertEqual(result.output, """\
[{"datacenter_id": 3, "date_created": "20160115T162658", "id": 12138, \
"name": "webacc01", "probe": {"enable": true, "host": null, "interval": null, \
"method": null, "response": null, "threshold": null, "timeout": null, \
"url": null, "window": null}, "servers": [{"fallback": false, "id": 14988, \
"ip": "195.142.160.181", "port": 80, "rproxy_id": 132691, \
"state": "running"}], "ssl_enable": false, "state": "running", \
"uuid": 12138, "vhosts": []}, {"datacenter_id": 1, \
"date_created": "20160115T162658", "id": 13263, "name": "testwebacc", \
"probe": {"enable": true, "host": "95.142.160.181", "interval": 10, \
"method": "GET", "response": 200, "threshold": 3, "timeout": 5, "url": "/", \
"window": 5}, "servers": [{"fallback": false, "id": 4988, \
"ip": "95.142.160.181", "port": 80, "rproxy_id": 13269, "state": "running"}], \
"ssl_enable": false, "state": "running", "uuid": 13263, \
"vhosts": [{"cert_id": null, "id": 5171, "name": "pouet.iheartcli.com", \
"rproxy_id": 13263, "state": "running"}]}]
""")
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        result = self.invoke_with_exceptions(webacc.info, ['testwebacc'])

        self.assertEqual(result.output, """\
name          : testwebacc
state         : running
datacenter    : Equinix Paris
ssl           : Disable
algorithm     : client-ip
Vhosts :
\tvhost         : pouet.iheartcli.com
\tssl           : None

Backends :
\tname          : server01
\tip            : 95.142.160.181
\tport          : 80
\tstate         : running

Probe :
\tstate         : Enabled
\thost          : 95.142.160.181
\tinterval      : 10
\tmethod        : GET
\tresponse      : 200
\tthreshold     : 3
\ttimeout       : 5
\turl           : /
\twindow        : 5
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_output_json(self):
        args = ['testwebacc', '--format', 'json']
        result = self.invoke_with_exceptions(webacc.info, args)

        self.assertEqual(result.output, """\
{"datacenter": {"country": "France", "dc_code": "FR-SD2", "id": 1, \
"iso": "FR", "name": "Equinix Paris"}, "date_created": "20160115T162658", \
"id": 13263, "lb": {"algorithm": "client-ip"}, "name": "testwebacc", \
"probe": {"enable": true, "host": "95.142.160.181", "interval": 10, \
"method": "GET", "response": 200, "threshold": 3, "timeout": 5, "url": "/", \
"window": 5}, "servers": [{"fallback": false, "id": 4988, \
"ip": "95.142.160.181", "port": 80, "rproxy_id": 13269, "state": "running"}], \
"ssl_enable": false, "state": "running", "uuid": 13263, \
"vhosts": [{"cert_id": null, "id": 5171, "name": "pouet.iheartcli.com", \
"rproxy_id": 13263, "state": "running"}]}
""")
        self.assertEqual(result.exit_code, 0)

    def test_info_backend_expired(self):
        result = self.invoke_with_exceptions(webacc.info, ['webacc01'])

        self.assertEqual(result.output, """\
name          : webacc01
state         : running
datacenter    : Equinix Paris
ssl           : Disable
algorithm     : client-ip
Vhosts :
Backends :
\tBackend with ip address 195.142.160.181 no longer exists.
\tYou should remove it.
\tip            : 195.142.160.181
\tport          : 80
\tstate         : running

Probe :
\tstate         : Enabled
\thost          :
\tinterval      :
\tmethod        :
\tresponse      :
\tthreshold     :
\ttimeout       :
\turl           :
\twindow        :
""")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        args = ['webacc2', '--datacenter', 'FR-SD3']
        result = self.invoke_with_exceptions(webacc.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your webaccelerator webacc2
\rProgress: [###] 100.00%  00:00:00  \
\nYour webaccelerator have been created""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.create'][0][0]
        self.assertEqual(params['name'], 'webacc2')
        self.assertEqual(params['datacenter_id'], 4)
        self.assertEqual(params['ssl_enable'], False)
        self.assertEqual(params['lb'], {'algorithm': 'client-ip'})
        self.assertEqual(params['zone_alter'], False)
        self.assertEqual(params['override'], True)

    def test_create_datacenter_limited(self):
        args = ['webacc2', '--datacenter', 'FR-SD2']
        result = self.invoke_with_exceptions(webacc.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
/!\ Datacenter FR-SD2 will be closed on 25/12/2017, please consider using \
another datacenter.
Creating your webaccelerator webacc2
\rProgress: [###] 100.00%  00:00:00  \
\nYour webaccelerator have been created""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.create'][0][0]
        self.assertEqual(params['name'], 'webacc2')
        self.assertEqual(params['datacenter_id'], 1)
        self.assertEqual(params['ssl_enable'], False)
        self.assertEqual(params['lb'], {'algorithm': 'client-ip'})
        self.assertEqual(params['zone_alter'], False)
        self.assertEqual(params['override'], True)

    def test_create_datacenter_closed(self):
        args = ['webacc2', '--datacenter', 'US-BA1']
        result = self.invoke_with_exceptions(webacc.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Error: /!\ Datacenter US-BA1 is closed, please choose another datacenter.""")

        self.assertEqual(result.exit_code, 1)

    def test_create_ssl_ok(self):
        args = ['webacc2', '--datacenter', 'FR-SD3', '--vhost',
                'pouet.lol.cat', '--ssl']
        result = self.invoke_with_exceptions(webacc.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please give the private key for certificate id 710 (CN: lol.cat)""")

        self.assertEqual(result.exit_code, 0)

    def test_create_backend_prompt(self):
        args = ['webacc2', '--datacenter', 'FR-SD3',
                '--backend', '195.142.160.181']
        result = self.invoke_with_exceptions(webacc.create, args,
                                             input='8080\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please set a port for backends. \
If you want to set different port for each backend, use `-b ip:port`: 8080
Creating your webaccelerator webacc2
\rProgress: [###] 100.00%  00:00:00  \
\nYour webaccelerator have been created""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.create'][0][0]
        self.assertEqual(params['name'], 'webacc2')
        self.assertEqual(params['datacenter_id'], 4)
        self.assertEqual(params['ssl_enable'], False)
        self.assertEqual(params['lb'], {'algorithm': 'client-ip'})
        self.assertEqual(params['zone_alter'], False)
        self.assertEqual(params['override'], True)
        self.assertEqual(params['servers'], ({'ip': u'195.142.160.181',
                                              'port': 8080},))

    def test_create_backend_port_ok(self):
        args = ['webacc2', '--datacenter', 'FR-SD3',
                '--backend', '195.142.160.181', '--port', 9000]
        result = self.invoke_with_exceptions(webacc.create, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Creating your webaccelerator webacc2
\rProgress: [###] 100.00%  00:00:00  \
\nYour webaccelerator have been created""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.create'][0][0]
        self.assertEqual(params['name'], 'webacc2')
        self.assertEqual(params['datacenter_id'], 4)
        self.assertEqual(params['ssl_enable'], False)
        self.assertEqual(params['lb'], {'algorithm': 'client-ip'})
        self.assertEqual(params['zone_alter'], False)
        self.assertEqual(params['override'], True)
        self.assertEqual(params['servers'], ({'ip': u'195.142.160.181',
                                              'port': 9000},))

    def test_update(self):
        args = ['testwebacc', '-n', 'testwebacc2',
                '--ssl-enable', '--algorithm', 'round-robin']
        result = self.invoke_with_exceptions(webacc.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your webaccelerator
\rProgress: [###] 100.00%  00:00:00  \
\nThe webaccelerator have been udated""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.update'][0][1]
        self.assertEqual(params['name'], 'testwebacc2')
        self.assertEqual(params['ssl_enable'], True)
        self.assertEqual(params['lb'], {'algorithm': 'round-robin'})

    def test_delete_webacc(self):
        args = ['-w', 'webacc01']
        result = self.invoke_with_exceptions(webacc.delete, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Deleting your webaccelerator named webacc01
\rProgress: [###] 100.00%  00:00:00  \
\nWebaccelerator have been deleted""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_vhost(self):
        args = ['-v', 'pouet.iheartcli.com']
        result = self.invoke_with_exceptions(webacc.delete, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Deleting your virtual host pouet.iheartcli.com
\rProgress: [###] 100.00%  00:00:00  \
\nYour virtual host have been removed""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_backend_prompt(self):
        args = ['--backend', '195.142.160.181']
        result = self.invoke_with_exceptions(webacc.delete, args,
                                             input='8080\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please set a port for backends. \
If you want to  different port for each backend, use `-b ip:port`: 8080
Removing backend 195.142.160.181:8080 into webaccelerator
\rProgress: [###] 100.00%  00:00:00  \
\nYour backend have been removed""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_backend_port_ok(self):
        args = ['--backend', '195.142.160.181', '--port', 9000]
        result = self.invoke_with_exceptions(webacc.delete, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Removing backend 195.142.160.181:9000 into webaccelerator
\rProgress: [###] 100.00%  00:00:00  \
\nYour backend have been removed""")

        self.assertEqual(result.exit_code, 0)

    def test_enable_probe(self):
        args = ['webacc01', '-p']
        result = self.invoke_with_exceptions(webacc.enable, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Activating probe on webacc01
\rProgress: [###] 100.00%  00:00:00  \
\nThe probe have been activated""")

        self.assertEqual(result.exit_code, 0)

    def test_enable_probe_no_resource(self):
        args = ['-p']
        result = self.invoke_with_exceptions(webacc.enable, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
You need to indicate the Webaccelerator name""")

        self.assertEqual(result.exit_code, 0)

    def test_enable_backend_prompt(self):
        args = ['webacc01', '--backend', '195.142.160.181']
        result = self.invoke_with_exceptions(webacc.enable, args,
                                             input='8080\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please set a port for backends. \
If you want to  different port for each backend, use `-b ip:port`: 8080
Activating backend 195.142.160.181
\rProgress: [###] 100.00%  00:00:00  \
\nBackend activated""")

        self.assertEqual(result.exit_code, 0)

    def test_enable_backend_port_ok(self):
        args = ['webacc01', '--backend', '195.142.160.181',
                '--port', 9000]
        result = self.invoke_with_exceptions(webacc.enable, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Activating backend 195.142.160.181
\rProgress: [###] 100.00%  00:00:00  \
\nBackend activated""")

        self.assertEqual(result.exit_code, 0)

    def test_disable_probe(self):
        args = ['webacc01', '-p']
        result = self.invoke_with_exceptions(webacc.disable, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Desactivating probe on webacc01
\rProgress: [###] 100.00%  00:00:00  \
\nThe probe have been desactivated""")

        self.assertEqual(result.exit_code, 0)

    def test_disable_probe_no_resource(self):
        args = ['-p']
        result = self.invoke_with_exceptions(webacc.disable, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
You need to indicate the Webaccelerator name""")

        self.assertEqual(result.exit_code, 0)

    def test_disable_backend_port_ok(self):
        args = ['webacc01', '--backend', '195.142.160.181',
                '--port', 9000]
        result = self.invoke_with_exceptions(webacc.disable, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Desactivating backend on server 195.142.160.181
\rProgress: [###] 100.00%  00:00:00  \
\nBackend desactivated""")

        self.assertEqual(result.exit_code, 0)

    def test_disable_backend_prompt(self):
        args = ['webacc01', '--backend', '195.142.160.181']
        result = self.invoke_with_exceptions(webacc.disable, args,
                                             input='8080\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please set a port for backends. \
If you want to  different port for each backend, use `-b ip:port`: 8080
Desactivating backend on server 195.142.160.181
\rProgress: [###] 100.00%  00:00:00  \
\nBackend desactivated""")

        self.assertEqual(result.exit_code, 0)

    def test_add_vhost(self):
        args = ['webacc01', '-v', 'pouet.iheartcli.com', '--zone-alter',
                '--ssl']
        result = self.invoke_with_exceptions(webacc.add, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
There is no certificate for pouet.iheartcli.com.
Create the certificate with (for exemple) :
$ gandi certificate create --cn pouet.iheartcli.com --type std \
\nOr relaunch the current command with --poll-cert option
Adding your virtual host (pouet.iheartcli.com) into webacc01
\rProgress: [###] 100.00%  00:00:00  \
\nYour virtual host habe been added""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['hosting.rproxy.vhost.create'][0][1]
        self.assertEqual(params['vhost'], 'pouet.iheartcli.com')
        self.assertEqual(params['zone_alter'], True)

    def test_add_vhost_ssl_ok(self):
        args = ['webacc01', '-v', 'pouet.lol.cat', '--zone-alter',
                '--ssl']
        result = self.invoke_with_exceptions(webacc.add, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please give the private key for certificate id 710 (CN: lol.cat)""")

        self.assertEqual(result.exit_code, 0)

    def test_add_backend_prompt(self):
        args = ['webacc01', '-b', '195.142.160.181']
        result = self.invoke_with_exceptions(webacc.add, args,
                                             input='80\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Please set a port for backends. \
If you want to  different port for each backend, use `-b ip:port`: 80
Adding backend 195.142.160.181:80 into webaccelerator
\rProgress: [###] 100.00%  00:00:00  \
\nBackend added""")

        self.assertEqual(result.exit_code, 0)

    def test_add_backend_port_ok(self):
        args = ['webacc01', '-b', '195.142.160.181', '--port', 9000]
        result = self.invoke_with_exceptions(webacc.add, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Adding backend 195.142.160.181:9000 into webaccelerator
\rProgress: [###] 100.00%  00:00:00  \
\nBackend added""")

        self.assertEqual(result.exit_code, 0)

    def test_probe_test(self):
        args = ['webacc01', '--window', 5,
                '--timeout', 5, '--threshold', 3, '--interval', 10,
                '--host', '95.142.160.181', '--url', '/',
                '--http-method', 'GET', '--http-response', 200,
                '--test']
        result = self.invoke_with_exceptions(webacc.probe, args)

        self.assertEqual(result.output.strip(), """\
status        : 200
timeout       : 1.0""")
        self.assertEqual(result.exit_code, 0)

    def test_probe_update(self):
        args = ['webacc01', '--window', 5,
                '--timeout', 5, '--threshold', 3, '--interval', 10,
                '--host', '95.142.160.181', '--url', '/',
                '--http-method', 'GET', '--http-response', 200]
        result = self.invoke_with_exceptions(webacc.probe, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Progress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
