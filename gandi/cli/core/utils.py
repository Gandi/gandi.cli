import time


class MissingConfiguration(Exception):
    """ Raise when configuration if missing"""

    def __init__(self, errors):
        self.errors = errors


class DuplicateResults(Exception):
    """ Raise when multiple results are found"""

    def __init__(self, errors):
        self.errors = errors


def output_line(gandi, key, val, justify):
    """ Base helper to output a key value using left justify"""
    msg = ('%%-%ds: %%s' % justify) % (key, val)
    gandi.echo(msg)


def output_generic(gandi, data, output_keys, justify=10):
    """ Generic helper to output info from a data dict """

    for key in output_keys:
        if key in data:
            output_line(gandi, key, data[key], justify)

def output_vm(gandi, vm, datacenters, output_keys, justify=10):
    """ Helper to output a vm information """

    output_generic(gandi, vm, output_keys, justify)

    if 'datacenter' in output_keys:
        for dc in datacenters:
            if dc['id'] == vm['datacenter_id']:
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)

    if 'ip' in output_keys:
        for iface in vm['ifaces']:
            output_line(gandi, 'bandwidth', iface['bandwidth'], justify)

            for ip in iface['ips']:
                ip_addr = ip['ip']

                output_line(gandi, 'ip%s' % ip['version'], ip_addr, justify)


def output_vhost(gandi, vhost, paas, output_keys, justify=14):
    """ Helper to output a vhost information """

    output_generic(gandi, vhost, output_keys, justify)

    if 'paas_name' in output_keys:
        output_line(gandi, 'paas_name', paas, justify)


def output_paas(gandi, paas, datacenters, vhosts, output_keys, justify=10):
    """ Helper to output a paas information """

    output_generic(gandi, paas, output_keys, justify)

    if 'vhost' in output_keys:
        for entry in vhosts:
            output_line(gandi, 'vhost', entry, justify)

    if 'dc' in output_keys:
        dc_name = paas['datacenter']['iso']
        output_line(gandi, 'datacenter', dc_name, justify)


def output_image(gandi, image, datacenters, output_keys, justify=14):
    """ Helper to output a disk image """

    output_generic(gandi, image, output_keys, justify)

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == image['datacenter_id']:
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)


def output_sshkey(gandi, sshkey, output_keys, justify=12):
    '''Helper to output an ssh key information '''
    output_generic(gandi, sshkey, output_keys, justify)


def check_domain_available(ctx, domain):
    """ Helper to check if a domain is available """
    gandi = ctx.obj
    result = gandi.call('domain.available', [domain])
    while result[domain] == 'pending':
        time.sleep(1)
        result = gandi.call('domain.available', [domain])

    if result[domain] == 'unavailable':
        gandi.echo('%s is not available' % domain)
        return

    return domain

def output_contact_info(gandi, data, output_keys, justify=10):
    """Helper to output chosen contacts info"""
    for key in output_keys:
        if data[key]:
            output_line(gandi, key, data[key]['handle'], justify)

def randomstring(prefix=None):
    """ Helper to generate a random string, used for temporary hostnames """
    if not prefix:
        prefix = 'temp'
    return '%s%s' % (prefix, str(int(time.time())))
