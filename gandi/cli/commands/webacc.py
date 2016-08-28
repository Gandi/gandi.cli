""" Webaccelerator namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import (
    output_generic, output_json, output_sub_generic,
    DatacenterLimited
)
from gandi.cli.core.params import (
    pass_gandi, BACKEND, DATACENTER, WEBACC_NAME, WEBACC_VHOST_NAME
)


@cli.command()
@click.option('--limit', help="Limit the number of results", default=100,
              show_default=True)
@click.option('--format', type=click.Choice(['json', 'pretty-json']),
              required=False, help="Choose the output format")
@pass_gandi
def list(gandi, limit, format):
    """ List webaccelerators """
    options = {
        'items_per_page': limit,
    }

    result = gandi.webacc.list(options)
    if format:
        output_json(gandi, format, result)
        return result

    output_keys = ['name', 'state', 'ssl']
    for num, webacc in enumerate(result):
        if num:
            gandi.separator_line('-', 4)

        webacc['ssl'] = 'Enabled' if webacc['ssl_enable'] else 'Disable'
        output_generic(gandi, webacc, output_keys, justify=14)

        gandi.echo('Vhosts :')
        for num, vhost in enumerate(webacc['vhosts']):
            output_vhosts = ['vhost', 'ssl']
            vhost['vhost'] = vhost['name']
            vhost['ssl'] = 'Disable' if vhost['cert_id'] is None else 'Enabled'
            output_sub_generic(gandi, vhost, output_vhosts,
                               justify=14)
            gandi.echo('')

        gandi.echo('Backends :')
        for server in webacc['servers']:
            try:
                ip = gandi.ip.info(server['ip'])
                iface = gandi.iface.info(ip['iface_id'])
                vm_info = gandi.iaas.info(iface['vm_id'])
                server['name'] = vm_info['hostname']
                output_servers = ['name', 'ip', 'port', 'state']
            except Exception:
                warningmsg = ('\tBackend with ip address %s no longer '
                              'exists.\n\tYou should remove it.'
                              % server['ip'])
                gandi.echo(warningmsg)
                output_servers = ['ip', 'port', 'state']
            output_sub_generic(gandi, server, output_servers,
                               justify=14)
            gandi.echo('')
    return result


@cli.command()
@click.option('--format', type=click.Choice(['json', 'pretty-json']),
              required=False, help="Choose the output format")
@click.argument('resource', type=WEBACC_NAME)
@pass_gandi
def info(gandi, resource, format):
    """ Display information about a webaccelerator """
    result = gandi.webacc.info(resource)
    if format:
        output_json(gandi, format, result)
        return result

    output_base = {
        'name': result['name'],
        'algorithm': result['lb']['algorithm'],
        'datacenter': result['datacenter']['name'],
        'state': result['state'],
        'ssl': 'Disable' if result['ssl_enable'] is False else 'Enabled'
    }
    output_keys = ['name', 'state', 'datacenter', 'ssl', 'algorithm']
    output_generic(gandi, output_base, output_keys, justify=14)

    gandi.echo('Vhosts :')
    for vhost in result['vhosts']:
        output_vhosts = ['vhost', 'ssl']
        vhost['vhost'] = vhost['name']
        vhost['ssl'] = 'None' if vhost['cert_id'] is None else 'Exists'
        output_sub_generic(gandi, vhost, output_vhosts, justify=14)
        gandi.echo('')

    gandi.echo('Backends :')
    for server in result['servers']:
        try:
            ip = gandi.ip.info(server['ip'])
            iface = gandi.iface.info(ip['iface_id'])
            server['name'] = gandi.iaas.info(iface['vm_id'])['hostname']
            output_servers = ['name', 'ip', 'port', 'state']
        except:
            warningmsg = ('\tBackend with ip address %s no longer exists.'
                          '\n\tYou should remove it.' % server['ip'])
            gandi.echo(warningmsg)
            output_servers = ['ip', 'port', 'state']
        output_sub_generic(gandi, server, output_servers, justify=14)
        gandi.echo('')

    gandi.echo('Probe :')
    output_probe = ['state', 'host', 'interval', 'method', 'response',
                    'threshold', 'timeout', 'url', 'window']
    result['probe']['state'] = ('Disable'
                                if result['probe']['enable'] is False
                                else 'Enabled')
    output_sub_generic(gandi, result['probe'], output_probe, justify=14)
    return result


@cli.command()
@click.option('--datacenter', '-dc', type=DATACENTER,
              help="Datacenter where the webaccelerator will be created",
              required=True)
@click.option('--backend', '-b', type=BACKEND, multiple=True,
              help="Backend to add in the webaccelerator, use ip:port")
@click.option('--port', '-p', type=click.INT, required=False,
              help="set a default port backend if not specified with backend")
@click.option('--vhost', '-v', help="Vhost to add in the webaccelerator",
              multiple=True)
@click.option('--ssl', help='Get ssl on that vhost.', is_flag=True)
@click.option('--pk', '--private-key',
              help='Private key used to generate the ssl Certificate.')
@click.option('--poll-cert', help='Will wait for the certificate creation.',
              is_flag=True)
@click.option('--algorithm', type=click.Choice(['client-ip', 'round-robin']),
              help="Choose the loadbalancer algorithm", default='client-ip')
@click.option('--ssl-enable', is_flag=True,
              help="Activate SSL support on the webaccelerator")
@click.option('--zone-alter', is_flag=True,
              help="Alter the zone file of the domain for the vhost if domains"
              "are registred at Gandi")
@click.argument('name')
@pass_gandi
def create(gandi, name, datacenter, backend, port, vhost, algorithm,
           ssl_enable, zone_alter, ssl, private_key, poll_cert):
    """ Create a webaccelerator """
    try:
        gandi.datacenter.is_opened(datacenter, 'iaas')
    except DatacenterLimited as exc:
        gandi.echo('/!\ Datacenter %s will be closed on %s, '
                   'please consider using another datacenter.' %
                   (datacenter, exc.date))

    backends = backend
    for backend in backends:
        # Check if a port is set for each backend, else set a default port
        if 'port' not in backend:
            if not port:
                backend['port'] = click.prompt('Please set a port for '
                                               'backends. If you want to set '
                                               'different port for each '
                                               'backend, use `-b ip:port`',
                                               type=int)
            else:
                backend['port'] = port

    if vhost and not gandi.hostedcert.activate_ssl(vhost,
                                                   ssl,
                                                   private_key,
                                                   poll_cert):
        return

    result = gandi.webacc.create(name, datacenter, backends, vhost, algorithm,
                                 ssl_enable, zone_alter)
    return result


@cli.command()
@click.option('--name', '-n', help="The name of the webaccelerator")
@click.option('--algorithm', type=click.Choice(['client-ip', 'round-robin']),
              help="Choose the loadbalancer algorithm")
@click.option('--ssl-enable', is_flag=True,
              help="Activate SSL support on the webaccelerator")
@click.option('--ssl-disable', is_flag=True,
              help="Deactivate SSL support on the webaccelerator")
@click.argument('resource', required=True, type=WEBACC_NAME)
@pass_gandi
def update(gandi, resource, name, algorithm, ssl_enable, ssl_disable):
    """Update a webaccelerator"""
    result = gandi.webacc.update(resource, name, algorithm, ssl_enable,
                                 ssl_disable)
    return result


@cli.command()
@click.option('--vhost', '-v', help="Remove vhosts in the webaccelerator",
              multiple=True, type=WEBACC_VHOST_NAME)
@click.option('--backend', '-b', help="Remove backends in the webaccelerator",
              multiple=True, type=BACKEND)
@click.option('--port', '-p', type=click.INT, required=False,
              help="The backend port if not specified with backend")
@click.option('--webacc', '-w', type=WEBACC_NAME, required=False,
              help='The webaccelerator name')
@pass_gandi
def delete(gandi, webacc, vhost, backend, port):
    """ Delete a webaccelerator, a vhost or a backend """
    result = []
    if webacc:
        result = gandi.webacc.delete(webacc)

    if backend:
        backends = backend
        for backend in backends:
            if 'port' not in backend:
                if not port:
                    backend['port'] = click.prompt('Please set a port for '
                                                   'backends. If you want to '
                                                   ' different port for '
                                                   'each backend, use `-b '
                                                   'ip:port`', type=int)
                else:
                    backend['port'] = port
            result = gandi.webacc.backend_remove(backend)

    if vhost:
        vhosts = vhost
        for vhost in vhosts:
            result = gandi.webacc.vhost_remove(vhost)

    return result


@cli.command()
@click.option('--vhost', '-v', help="Add vhosts in the webaccelerator",
              multiple=True)
@click.option('--ssl', help='Get ssl on that vhost.', is_flag=True)
@click.option('--pk', '--private-key',
              help='Private key used to generate the ssl Certificate.')
@click.option('--poll-cert', help='Will wait for the certificate creation.',
              is_flag=True)
@click.option('--zone-alter', is_flag=True,
              help="Alter and activate zone file if Gandi DNS are used for"
                   " the domain",)
@click.option('--backend', '-b', help="Add backends in the webaccelerator",
              type=BACKEND, multiple=True)
@click.option('--port', '-p', type=click.INT, required=False,
              help="set a default port backend if not specified with backend")
@click.argument('resource', type=WEBACC_NAME)
@pass_gandi
def add(gandi, resource, vhost, zone_alter, backend, port, ssl, private_key,
        poll_cert):
    """ Add a backend or a vhost on a webaccelerator """
    result = []
    if backend:
        backends = backend
        for backend in backends:
            # Check if a port is set for each backend, else set a default port
            if 'port' not in backend:
                if not port:
                    backend['port'] = click.prompt('Please set a port for '
                                                   'backends. If you want to '
                                                   ' different port for '
                                                   'each backend, use `-b '
                                                   'ip:port`', type=int)
                else:
                    backend['port'] = port
            result = gandi.webacc.backend_add(resource, backend)

    if vhost:
        if not gandi.hostedcert.activate_ssl(vhost, ssl, private_key,
                                             poll_cert):
            return
        vhosts = vhost
        for vhost in vhosts:
            params = {'vhost': vhost}
            if zone_alter:
                params['zone_alter'] = zone_alter
            result = gandi.webacc.vhost_add(resource, params)
    return result


@cli.command()
@click.option('--backend', '-b', help="Enable backends in the webaccelerator",
              multiple=True, type=BACKEND)
@click.option('--port', '-p', type=click.INT, required=False,
              help="set a default port backend if not specified with backend")
@click.option('--probe', '-p', help="Enable probe for the webaccelerator",
              is_flag=True)
@click.argument('resource', required=False, type=WEBACC_NAME)
@pass_gandi
def enable(gandi, resource, backend, port, probe):
    """ Enable a backend or a probe on a webaccelerator """
    result = []
    if backend:
        backends = backend
        for backend in backends:
            if 'port' not in backend:
                if not port:
                    backend['port'] = click.prompt('Please set a port for '
                                                   'backends. If you want to '
                                                   ' different port for '
                                                   'each backend, use `-b '
                                                   'ip:port`', type=int)
                else:
                    backend['port'] = port
            result = gandi.webacc.backend_enable(backend)

    if probe:
        if not resource:
            gandi.echo('You need to indicate the Webaccelerator name')
            return
        result = gandi.webacc.probe_enable(resource)

    return result


@cli.command()
@click.option('--backend', '-b', help="Disable backends in the webaccelerator",
              multiple=True, type=BACKEND)
@click.option('--port', '-p', type=click.INT, required=False,
              help="set a default port backend if not specified with backend")
@click.option('--probe', '-p', help="Disable probe for the webaccelerator",
              is_flag=True)
@click.argument('resource', required=False, type=WEBACC_NAME)
@pass_gandi
def disable(gandi, resource, backend, port, probe):
    """ Disable a backend or a probe on a webaccelerator """
    result = []
    if backend:
        backends = backend
        for backend in backends:
            if 'port' not in backend:
                if not port:
                    backend['port'] = click.prompt('Please set a port for '
                                                   'backends. If you want to '
                                                   ' different port for '
                                                   'each backend, use `-b '
                                                   'ip:port`', type=int)
                else:
                    backend['port'] = port
            result = gandi.webacc.backend_disable(backend)

    if probe:
        if not resource:
            gandi.echo('You need to indicate the Webaccelerator name')
            return
        result = gandi.webacc.probe_disable(resource)

    return result


@cli.command()
@click.option('--enable', '-e', is_flag=True,
              help="Enable the probe on the webaccelerator")
@click.option('--disable', '-d', is_flag=True,
              help="Disable the probe on the webaccelerator")
@click.option('--test', is_flag=True, help="Test probe on the webaccelerator")
@click.option('--host', '-h', help="Set the host to test")
@click.option('--interval', '-i', help="Set interval for the probe",
              type=click.INT)
@click.option('--http-method', '-m', help="Choose HTTP method for the probe",
              type=click.Choice(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']))
@click.option('--http-response', '-r', type=click.INT,
              help="HTTP response code expected by the probe")
@click.option('--threshold', '-t', type=click.INT,
              help="Number of probes to consider in the window")
@click.option('--timeout', help="Timeout in seconds",
              type=click.INT)
@click.option('--url', '-u', help="Probe url in the virtual host",
              type=click.STRING)
@click.option('--window', '-w', type=click.INT,
              help="Total number of probes to consider health decision")
@click.argument('resource', type=WEBACC_NAME)
@pass_gandi
def probe(gandi, resource, enable, disable, test, host, interval, http_method,
          http_response, threshold, timeout, url, window):
    """ Manage a probe for a webaccelerator """
    result = gandi.webacc.probe(resource, enable, disable, test, host,
                                interval, http_method, http_response,
                                threshold, timeout, url, window)
    output_keys = ['status', 'timeout']
    output_generic(gandi, result, output_keys, justify=14)
    return result
