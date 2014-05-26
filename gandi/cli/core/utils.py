
class MissingConfiguration(Exception):
    """ Raise when configuration if missing"""

    def __init__(self, errors):
        self.errors = errors


def output_vm(gandi, vm, datacenters, output_keys):
    """ Helper to output a vm information """

    for key in output_keys:
        if key in vm:
            msg = '%-10s: %s' % (key, vm[key])
            gandi.echo(msg)

    if 'datacenter' in output_keys:
        for dc in datacenters:
            if dc['id'] == vm['datacenter_id']:
                dc_name = dc['iso']
                break

        msg = '%-10s: %s' % ('datacenter', dc_name)
        gandi.echo(msg)


def output_paas(gandi, paas, datacenters, vhosts, output_keys):
    """ Helper to output a paas information """

    gandi.debug(output_keys)
    for key in output_keys:
        if key in paas:
            msg = '%-10s: %s' % (key, paas[key])
            gandi.echo(msg)

    if 'vhost' in output_keys:
        for entry in vhosts:
            msg = '%-10s: %s' % ('vhost', entry)
            gandi.echo(msg)

    if 'dc' in output_keys:
        dc_name = paas['datacenter']['iso']
        msg = '%-10s: %s' % ('datacenter', dc_name)
        gandi.echo(msg)


def read_ssh_key(ctx, value):
    """ Helper to read content of a filehandler

    Use to read ssh_key when provided on command line using pipe.
    """
    if not value:
        return

    key = value.read()
    return key
