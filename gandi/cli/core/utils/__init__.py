""" Contains output methods used by commands.

Also custom exceptions and method to generate a random string.
"""

import time

import click
import json
from click.formatting import measure_table

from .ascii_sparks import sparks


class MissingConfiguration(Exception):

    """ Raise when configuration if missing. """

    def __init__(self, errors):
        """ Initialize exception."""
        self.errors = errors


class DuplicateResults(Exception):

    """ Raise when multiple results are found."""

    def __init__(self, errors):
        """ Initialize exception."""
        self.errors = errors


def display_rows(gandi, rows, has_header=True):
    col_len = measure_table(rows)
    formatting = ' | '.join(['%-' + str(l) + 's' for l in col_len])

    if has_header:
        header = rows.pop(0)
        gandi.echo(formatting % tuple(header))
        gandi.echo('-+-'.join(['-' * l for l in col_len]))

    for row in rows:
        gandi.echo(formatting % tuple(row))


def output_line(gandi, key, val, justify):
    """ Base helper to output a key value using left justify."""
    msg = ('%%-%ds:%%s' % justify) % (key, (' %s' % val) if val else '')
    gandi.echo(msg)


def output_generic(gandi, data, output_keys, justify=10):
    """ Generic helper to output info from a data dict."""
    for key in output_keys:
        if key in data:
            output_line(gandi, key, data[key], justify)


def output_account(gandi, account, output_keys, justify=17):
    """ Helper to output an account information."""
    output_generic(gandi, account, output_keys, justify)

    if 'credit' in output_keys:
        output_line(gandi, 'credits', None, justify)
        available = account.get('credits')
        output_line(gandi, '        available', available, justify)
        # sometimes rating is returning nothing
        usage_str = left_str = 'not available'
        usage = account.get('credit_usage', 0)
        if usage:
            usage_str = '%d/h' % usage

            left = available / usage
            years, hours = divmod(left, 365 * 24)
            months, hours = divmod(hours, 31 * 24)
            days, hours = divmod(hours, 24)
            left_str = '%d year(s) %d month(s) %d day(s) %d hour(s)' % \
                       (years, months, days, hours)

        output_line(gandi, '        usage', usage_str, justify)
        output_line(gandi, '        time left', left_str, justify)


def output_vm(gandi, vm, datacenters, output_keys, justify=10):
    """ Helper to output a vm information."""
    output_generic(gandi, vm, output_keys, justify)

    if 'datacenter' in output_keys:
        for dc in datacenters:
            if dc['id'] == vm['datacenter_id']:
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)

    if 'ip' in output_keys:
        for iface in vm['ifaces']:
            gandi.separator_line()
            output_line(gandi, 'bandwidth', iface['bandwidth'], justify)

            for ip in iface['ips']:
                ip_addr = ip['ip']

                output_line(gandi, 'ip%s' % ip['version'], ip_addr, justify)


def output_metric(gandi, metrics, key, justify=10):
    """ Helper to output metrics."""
    for metric in metrics:
        key_name = metric[key].pop()
        values = [point.get('value', 0) for point in metric['points']]
        graph = sparks(values) if max(values) else ''
        output_line(gandi, key_name, graph.encode('utf-8'), justify)


def output_vhost(gandi, vhost, paas, output_keys, justify=14):
    """ Helper to output a vhost information."""
    output_generic(gandi, vhost, output_keys, justify)

    if 'paas_name' in output_keys:
        output_line(gandi, 'paas_name', paas, justify)


def output_paas(gandi, paas, datacenters, vhosts, output_keys, justify=11):
    """ Helper to output a paas information."""
    output_generic(gandi, paas, output_keys, justify)

    if 'sftp_server' in output_keys:
        output_line(gandi, 'sftp_server', paas['ftp_server'], justify)

    if 'vhost' in output_keys:
        for entry in vhosts:
            output_line(gandi, 'vhost', entry, justify)

    if 'dc' in output_keys:
        dc_name = paas['datacenter']['iso']
        output_line(gandi, 'datacenter', dc_name, justify)

    if 'df' in paas:
        df = paas['df']
        total = df['free'] + df['used']
        if total:
            disk_used = '%.1f%%' % (df['used'] * 100 / total)
            output_line(gandi, 'quota used', disk_used, justify)


def output_image(gandi, image, datacenters, output_keys, justify=14):
    """ Helper to output a disk image."""
    output_generic(gandi, image, output_keys, justify)

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == image['datacenter_id']:
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)


def output_kernels(gandi, flavor, name_list, justify=14):
    """ Helper to output kernel flavor versions."""
    output_line(gandi, 'flavor', flavor, justify)
    for name in name_list:
        output_line(gandi, 'version', name, justify)


def output_datacenter(gandi, datacenter, justify=14):
    output_line(gandi, 'datacenter', datacenter['name'], justify)


def output_disk(gandi, disk, datacenters, vms, profiles, output_keys,
                justify=10):
    """ Helper to output a disk."""
    output_generic(gandi, disk, output_keys, justify)

    if 'kernel' in output_keys and disk.get('kernel_version'):
        output_line(gandi, 'kernel', disk['kernel_version'], justify)

    if 'dc' in output_keys:
        dc_name = None
        for dc in datacenters:
            if dc['id'] == disk['datacenter_id']:
                dc_name = dc['iso']
                break

        if dc_name:
            output_line(gandi, 'datacenter', dc_name, justify)

    if 'vm' in output_keys:
        for vm_id in disk['vms_id']:
            vm_name = vms.get(vm_id, {}).get('hostname')
            if vm_name:
                output_line(gandi, 'vm', vm_name, justify)

    if 'profile' in output_keys and disk.get('snapshot_profile'):
        output_line(gandi, 'profile', disk['snapshot_profile']['name'],
                    justify)
    elif 'profile' in output_keys and disk.get('snapshot_profile_id'):
        for profile in profiles:
            if profile['id'] == disk['snapshot_profile_id']:
                output_line(gandi, 'profile', profile['name'], justify)
                break


def output_sshkey(gandi, sshkey, output_keys, justify=12):
    """ Helper to output an ssh key information."""
    output_generic(gandi, sshkey, output_keys, justify)


def output_snapshot_profile(gandi, profile, output_keys, justify=13):
    """ Helper to output a snapshot_profile."""
    schedules = 'schedules' in output_keys
    if schedules:
        output_keys.remove('schedules')
    output_generic(gandi, profile, output_keys, justify)

    if schedules:
        schedule_keys = ['name', 'kept_version']
        for schedule in profile['schedules']:
            gandi.separator_line()
            output_generic(gandi, schedule, schedule_keys, justify)


def check_domain_available(ctx, param, domain):
    """ Helper to check if a domain is available."""
    gandi = ctx.obj
    result = gandi.call('domain.available', [domain])
    while result[domain] == 'pending':
        time.sleep(1)
        result = gandi.call('domain.available', [domain])

    if result[domain] == 'unavailable':
        raise click.ClickException('%s is not available' % domain)
        return

    return domain


def output_contact_info(gandi, data, output_keys, justify=10):
    """Helper to output chosen contacts info."""
    for key in output_keys:
        if data[key]:
            output_line(gandi, key, data[key]['handle'], justify)


def output_cert_oper(gandi, oper, justify=12):
    output_generic(gandi, oper, ['type', 'step'], justify)
    params = dict(oper['params'])
    params['fqdns'] = ', '.join(params.get('fqdns', []))
    output = ['inner_step', 'package_name', 'dcv_method']
    if params['fqdns']:
        output.append('fqdns')
    output_generic(gandi, params, output, justify)


def output_cert(gandi, cert, output_keys, justify=13):
    """Helper to output a certificate information."""
    output = list(output_keys)

    display_altnames = False
    if 'altnames' in output:
        display_altnames = True
        output.remove('altnames')

    display_output = False
    if 'cert' in output:
        display_output = True
        output.remove('cert')

    output_generic(gandi, cert, output, justify)

    if display_output:
        crt = gandi.certificate.pretty_format_cert(cert)
        if crt:
            output_line(gandi, 'cert', '\n' + crt, justify)

    if display_altnames:
        for altname in cert['altnames']:
            output_line(gandi, 'altname', altname, justify)


def output_vlan(gandi, vlan, datacenters, output_keys, justify=10):
    """ Helper to output a vlan information."""
    output_generic(gandi, vlan, output_keys, justify)

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == vlan.get('datacenter_id',
                                    vlan.get('datacenter', {}).get('id')):
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)


def output_iface(gandi, iface, datacenters, vms, output_keys, justify=10):
    """ Helper to output an iface information."""
    output_generic(gandi, iface, output_keys, justify)

    if 'vm' in output_keys:
        vm_name = vms.get(iface['vm_id'], {}).get('hostname')
        if vm_name:
            output_line(gandi, 'vm', vm_name, justify)

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == iface.get('datacenter_id',
                                     iface.get('datacenter', {}).get('id')):
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)

    if 'vlan_' in output_keys:
        vlan = iface.get('vlan') or {}
        output_line(gandi, 'vlan', vlan.get('name', '-'), justify)


def output_ip(gandi, ip, datacenters, vms, ifaces, output_keys, justify=11):
    """ Helper to output an ip information."""
    output_generic(gandi, ip, output_keys, justify)

    if 'type' in output_keys:
        iface = ifaces.get(ip['iface_id'])
        type_ = 'private' if iface.get('vlan') else 'public'
        output_line(gandi, 'type', type_, justify)
        if type_ == 'private':
            output_line(gandi, 'vlan', iface['vlan']['name'], justify)

    if 'vm' in output_keys:
        iface = ifaces.get(ip['iface_id'])
        vm_id = iface.get('vm_id')
        if vm_id:
            vm_name = vms.get(vm_id, {}).get('hostname')
            if vm_name:
                output_line(gandi, 'vm', vm_name, justify)

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == ip.get('datacenter_id',
                                  ip.get('datacenter', {}).get('id')):
                dc_name = dc['iso']
                break

        output_line(gandi, 'datacenter', dc_name, justify)


def randomstring(prefix=None):
    """ Helper to generate a random string, used for temporary hostnames."""
    if not prefix:
        prefix = 'tmp'
    return '%s%s' % (prefix, str(int(time.time())))


def output_list(gandi, val):
    """Helper to generate a beautiful list."""
    for element in val:
        gandi.echo(element)


def date_handler(obj):
    """ Serialize date for json output """
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def output_json(gandi, format, value):
    """ Helper to show json output """
    if format == 'json':
        gandi.echo(json.dumps(value, default=date_handler))
    elif format == 'pretty-json':
        gandi.echo(json.dumps(value, default=date_handler, sort_keys=True,
                   indent=2, separators=(',', ': ')))


def output_sub_line(gandi, key, val, justify):
    """ Base helper to output a key value using left justify."""
    msg = ('\t%%-%ds:%%s' % justify) % (key, (' %s' % val) if val else '')
    gandi.echo(msg)


def output_sub_generic(gandi, data, output_keys, justify=10):
    """ Generic helper to output info from a data dict."""
    for key in output_keys:
        if key in data:
            output_sub_line(gandi, key, data[key], justify)


def output_service(gandi, service, status, justify=10):
    """ Helper to output a status service information."""
    output_line(gandi, service, status, justify)
