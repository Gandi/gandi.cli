""" Webaccelerator commands module """

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Webacc(GandiModule):

    """ Module to handle CLI commands.

    $ gandi webacc list
    $ gandi webacc info
    $ gandi webacc create
    $ gandi webacc add
    $ gandi webacc delete
    $ gandi webacc enable
    $ gandi webacc disable
    $ gandi webacc probe

    """

    @classmethod
    def list(cls, options=None):
        """ List all webaccelerator """
        if not options:
            options = {}
        return cls.call('hosting.rproxy.list', options)

    @classmethod
    def info(cls, id):
        """ Get information about a Webaccelerator """
        return cls.call('hosting.rproxy.info', cls.usable_id(id))

    @classmethod
    def create(cls, name, datacenter, backends, vhosts, algorithm,
               ssl_enable, zone_alter):
        """ Create a webaccelerator """
        datacenter_id_ = int(Datacenter.usable_id(datacenter))
        params = {
            'datacenter_id': datacenter_id_,
            'name': name,
            'lb': {'algorithm': algorithm},
            'override': True,
            'ssl_enable': ssl_enable,
            'zone_alter': zone_alter
        }
        if vhosts:
            params['vhosts'] = vhosts
        if backends:
            params['servers'] = backends
        try:
            result = cls.call('hosting.rproxy.create', params)
            cls.echo('Creating your webaccelerator %s' % params['name'])
            cls.display_progress(result)
            cls.echo('Your webaccelerator have been created')
            return result
        except Exception as err:
            if err.code == 580142:
                for vhost in params['vhosts']:
                    dns_entry = cls.call(
                        'hosting.rproxy.vhost.get_dns_entries',
                        {'datacenter': datacenter_id_, 'vhost': vhost})
                    txt_record = "@ 3600 IN TXT \"%s=%s\"" % (dns_entry['key'],
                                                              dns_entry['txt'])

                    cname_record = "%s 3600 IN CNAME %s" % (dns_entry['key'],
                                                            dns_entry['cname'])

                    cls.echo('The domain %s don\'t use Gandi DNS or you have'
                             ' not sufficient right to alter the zone file. '
                             'Edit your zone file adding this TXT and CNAME '
                             'record and try again :' % vhost)
                    cls.echo(txt_record)
                    cls.echo(cname_record)
                    cls.echo('\nOr add a file containing %s at :\n'
                             'http://%s/%s.txt\n' % (dns_entry['txt'],
                                                     dns_entry['domain'],
                                                     dns_entry['txt']))
                    cls.separator_line('-', 4)
            else:
                cls.echo(err)

    @classmethod
    def update(cls, resource, new_name, algorithm, ssl_enable, ssl_disable):
        """ Update a webaccelerator"""
        params = {}
        if new_name:
            params['name'] = new_name
        if algorithm:
            params['lb'] = {'algorithm': algorithm}
        if ssl_enable:
            params['ssl_enable'] = ssl_enable
        if ssl_disable:
            params['ssl_enable'] = False

        result = cls.call('hosting.rproxy.update', cls.usable_id(resource),
                          params)
        cls.echo('Updating your webaccelerator')
        cls.display_progress(result)
        cls.echo('The webaccelerator have been udated')
        return result

    @classmethod
    def delete(cls, name):
        """ Delete a webaccelerator """
        result = cls.call('hosting.rproxy.delete', cls.usable_id(name))
        cls.echo('Deleting your webaccelerator named %s' % name)
        cls.display_progress(result)
        cls.echo('Webaccelerator have been deleted')
        return result

    @classmethod
    def backend_list(cls, options):
        """ List all servers used by webaccelerator """
        return cls.call('hosting.rproxy.server.list', options)

    @classmethod
    def backend_add(cls, name, backend):
        """ Add a backend into a webaccelerator """
        oper = cls.call(
            'hosting.rproxy.server.create', cls.usable_id(name), backend)
        cls.echo('Adding backend %s:%s into webaccelerator' %
                 (backend['ip'], backend['port']))
        cls.display_progress(oper)
        cls.echo('Backend added')
        return oper

    @classmethod
    def backend_remove(cls, backend):
        """ Remove a backend on a webaccelerator """
        server = cls.backend_list(backend)
        if server:
            oper = cls.call('hosting.rproxy.server.delete', server[0]['id'])
            cls.echo('Removing backend %s:%s into webaccelerator' %
                     (backend['ip'], backend['port']))
            cls.display_progress(oper)
            cls.echo('Your backend have been removed')
            return oper
        else:
            return cls.echo('No backend found')

    @classmethod
    def backend_enable(cls, backend):
        """ Enable a backend for a server """
        server = cls.backend_list(backend)
        if server:
            oper = cls.call('hosting.rproxy.server.enable', server[0]['id'])
            cls.echo('Activating backend %s' % server[0]['ip'])
            cls.display_progress(oper)
            cls.echo('Backend activated')
            return oper
        else:
            return cls.echo('No backend found')

    @classmethod
    def backend_disable(cls, backend):
        """ Disable a backend for a server """
        server = cls.backend_list(backend)
        oper = cls.call('hosting.rproxy.server.disable',
                        server[0]['id'])
        cls.echo('Desactivating backend on server %s' %
                 server[0]['ip'])
        cls.display_progress(oper)
        cls.echo('Backend desactivated')
        return oper

    @classmethod
    def vhost_list(cls):
        """ List all vhosts used by webaccelerator """
        return cls.call('hosting.rproxy.vhost.list')

    @classmethod
    def vhost_add(cls, resource, params):
        """ Add a vhost into a webaccelerator """
        try:
            oper = cls.call(
                'hosting.rproxy.vhost.create', cls.usable_id(resource), params)
            cls.echo('Adding your virtual host (%s) into %s' %
                     (params['vhost'], resource))
            cls.display_progress(oper)
            cls.echo('Your virtual host habe been added')
            return oper
        except Exception as err:
            if err.code == 580142:
                dc = cls.info(resource)
                dns_entry = cls.call('hosting.rproxy.vhost.get_dns_entries',
                                     {'datacenter': dc['datacenter']['id'],
                                      'vhost': params['vhost']})
                txt_record = "%s 3600 IN TXT \"%s=%s\"" % (dns_entry['key'],
                                                           dns_entry['key'],
                                                           dns_entry['txt'])

                cname_record = "%s 3600 IN CNAME %s" % (dns_entry['key'],
                                                        dns_entry['cname'])

                cls.echo('The domain don\'t use Gandi DNS or you have not'
                         ' sufficient right to alter the zone file. '
                         'Edit your zone file adding this TXT and CNAME '
                         'record and try again :')
                cls.echo(txt_record)
                cls.echo(cname_record)
                cls.echo('\nOr add a file containing %s at :\n'
                         'http://%s/%s.txt\n' % (dns_entry['txt'],
                                                 dns_entry['domain'],
                                                 dns_entry['txt']))

            else:
                cls.echo(err)

    @classmethod
    def vhost_remove(cls, name):
        """ Delete a vhost in a webaccelerator """
        oper = cls.call('hosting.rproxy.vhost.delete', name)
        cls.echo('Deleting your virtual host %s' % name)
        cls.display_progress(oper)
        cls.echo('Your virtual host have been removed')
        return oper

    @classmethod
    def probe(cls, resource, enable, disable, test, host, interval,
              http_method, http_response, threshold, timeout, url, window):
        """ Set a probe for a webaccelerator """
        params = {
            'host': host,
            'interval': interval,
            'method': http_method,
            'response': http_response,
            'threshold': threshold,
            'timeout': timeout,
            'url': url,
            'window': window
        }
        if enable:
            params['enable'] = True
        elif disable:
            params['enable'] = False
        if test:
            result = cls.call(
                'hosting.rproxy.probe.test', cls.usable_id(resource), params)
        else:
            result = cls.call(
                'hosting.rproxy.probe.update', cls.usable_id(resource), params)
            cls.display_progress(result)
        return result

    @classmethod
    def probe_enable(cls, resource):
        """ Activate a probe on a webaccelerator """
        oper = cls.call('hosting.rproxy.probe.enable', cls.usable_id(resource))
        cls.echo('Activating probe on %s' % resource)
        cls.display_progress(oper)
        cls.echo('The probe have been activated')
        return oper

    @classmethod
    def probe_disable(cls, resource):
        """ Disable a probe on a webaccelerator """
        oper = cls.call('hosting.rproxy.probe.disable',
                        cls.usable_id(resource))
        cls.echo('Desactivating probe on %s' % resource)
        cls.display_progress(oper)
        cls.echo('The probe have been desactivated')
        return oper

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be hostname, vhost, id. """
        try:
            # id is maybe a hostname
            qry_id = cls.from_name(id)
            if not qry_id:
                # id is maybe an ip
                qry_id = cls.from_ip(id)
            if not qry_id:
                qry_id = cls.from_vhost(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def from_name(cls, name):
        """Retrieve webacc id associated to a webacc name."""
        result = cls.list({'items_per_page': 500})
        webaccs = {}
        for webacc in result:
            webaccs[webacc['name']] = webacc['id']
        return webaccs.get(name)

    @classmethod
    def from_ip(cls, ip):
        """Retrieve webacc id associated to a webacc ip"""
        result = cls.list({'items_per_page': 500})
        webaccs = {}
        for webacc in result:
            for server in webacc['servers']:
                webaccs[server['ip']] = webacc['id']
        return webaccs.get(ip)

    @classmethod
    def from_vhost(cls, vhost):
        """Retrieve webbacc id associated to a webacc vhost"""
        result = cls.list({'items_per_page': 500})
        webaccs = {}
        for webacc in result:
            for vhost in webacc['vhosts']:
                webaccs[vhost['name']] = webacc['id']
        return webaccs.get(vhost)
