""" Contains output methods used by commands.

Also custom exceptions and method to generate a random string.
"""
import sys
import time
from datetime import datetime

import json
from click.formatting import measure_table
from click import ClickException

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


class DomainNotAvailable(Exception):

    """ Raise when domain is not available. """

    def __init__(self, errors):
        """ Initialize exception."""
        self.errors = errors


class DatacenterClosed(ClickException):

    """Raise when datacenter is closed: ALL"""

    def __init__(self, message):
        """ Initialize exception."""
        self.message = message


class DatacenterLimited(Exception):

    """Raise when datacenter will soon be closed: NEW"""

    def __init__(self, date):
        """ Initialize exception."""
        self.date = date


def format_list(data):
    """ Remove useless characters to output a clean list."""
    if isinstance(data, (list, tuple)):
        to_clean = ['[', ']', '(', ')', "'"]
        for item in to_clean:
            data = str(data).replace(item, '')
    return data


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

    if 'prepaid' in output_keys:
        prepaid = '%s %s' % (account['prepaid_info']['amount'],
                             account['prepaid_info']['currency'])
        output_line(gandi, 'prepaid', prepaid, justify)

    if 'credit' in output_keys:
        output_line(gandi, 'credits', None, justify)
        available = account.get('credits')
        output_line(gandi, '        available', available, justify)
        # sometimes rating is returning nothing
        usage_str = left_str = 'not available'
        usage = account.get('credit_usage', 0)
        left = account.get('left')
        if usage:
            usage_str = '%d/h' % usage

            years, months, days, hours = left
            left_str = ('%d year(s) %d month(s) %d day(s) %d hour(s)' %
                        (years, months, days, hours))

        output_line(gandi, '        usage', usage_str, justify)
        output_line(gandi, '        time left', left_str, justify)


def output_vm(gandi, vm, datacenters, output_keys, justify=10):
    """ Helper to output a vm information."""
    output_generic(gandi, vm, output_keys, justify)

    if 'datacenter' in output_keys:
        for dc in datacenters:
            if dc['id'] == vm['datacenter_id']:
                dc_name = dc.get('dc_code', dc.get('iso', ''))
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
        # need to encode in utf-8 to work in python2.X
        if sys.version_info < (2, 8):
            graph = graph.encode('utf-8')
        output_line(gandi, key_name, graph, justify)


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
        dc_name = paas['datacenter'].get('dc_code',
                                         paas['datacenter'].get('iso', ''))
        output_line(gandi, 'datacenter', dc_name, justify)

    if 'df' in paas:
        df = paas['df']
        total = df['free'] + df['used']
        if total:
            disk_used = '%.1f%%' % (df['used'] * 100 / total)
            output_line(gandi, 'quota used', disk_used, justify)

    if 'snapshot' in output_keys:
        val = None
        if paas['snapshot_profile']:
            val = paas['snapshot_profile']['name']
        output_line(gandi, 'snapshot', val, justify)

    if 'cache' in paas:
        cache = paas['cache']
        total = cache['hit'] + cache['miss'] + cache['not'] + cache['pass']
        if total:
            output_line(gandi, 'cache', None, justify)
            for key in sorted(cache):
                str_value = '%.1f%%' % (cache[key] * 100 / total)
                output_sub_line(gandi, key, str_value, 5)


def output_image(gandi, image, datacenters, output_keys, justify=14):
    """ Helper to output a disk image."""
    output_generic(gandi, image, output_keys, justify)

    dc_name = 'Nowhere'

    if 'dc' in output_keys:
        for dc in datacenters:
            if dc['id'] == image['datacenter_id']:
                dc_name = dc.get('dc_code', dc.get('iso', ''))

                break

        output_line(gandi, 'datacenter', dc_name, justify)


def output_kernels(gandi, flavor, name_list, justify=14):
    """ Helper to output kernel flavor versions."""
    output_line(gandi, 'flavor', flavor, justify)
    for name in name_list:
        output_line(gandi, 'version', name, justify)


def output_datacenter(gandi, datacenter, output_keys, justify=14):
    """ Helper to output datacenter information."""
    output_generic(gandi, datacenter, output_keys, justify)

    if 'dc_name' in output_keys:
        output_line(gandi, 'datacenter', datacenter['name'], justify)

    if 'status' in output_keys:
        deactivate_at = datacenter.get('deactivate_at')
        if deactivate_at:
            output_line(gandi, 'closing on',
                        deactivate_at.strftime('%d/%m/%Y'), justify)

        closing = []
        iaas_closed_for = datacenter.get('iaas_closed_for')
        if iaas_closed_for == 'ALL':
            closing.append('vm')

        paas_closed_for = datacenter.get('paas_closed_for')
        if paas_closed_for == 'ALL':
            closing.append('paas')

        if closing:
            output_line(gandi, 'closed for', ', '.join(closing), justify)


def output_cmdline(gandi, cmdline, justify=14):
    args = []
    for key in sorted(cmdline, reverse=True):
        if isinstance(cmdline[key], bool):
            args.append(key)
        else:
            args.append('%s=%s' % (key, cmdline[key]))
    output_line(gandi, 'cmdline', ' '.join(args), justify)


def output_disk(gandi, disk, datacenters, vms, profiles, output_keys,
                justify=10):
    """ Helper to output a disk."""
    output_generic(gandi, disk, output_keys, justify)

    if 'kernel' in output_keys and disk.get('kernel_version'):
        output_line(gandi, 'kernel', disk['kernel_version'], justify)

    if 'cmdline' in output_keys and disk.get('kernel_cmdline'):
        output_cmdline(gandi, disk.get('kernel_cmdline'), justify)

    if 'dc' in output_keys:
        dc_name = None
        for dc in datacenters:
            if dc['id'] == disk['datacenter_id']:
                dc_name = dc.get('dc_code', dc.get('iso', ''))
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
                dc_name = dc.get('dc_code', dc.get('iso', ''))
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
                dc_name = dc.get('dc_code', dc.get('iso', ''))
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
                dc_name = dc.get('dc_code', dc.get('iso', ''))
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
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def output_json(gandi, format, value):
    """ Helper to show json output """
    if format == 'json':
        gandi.echo(json.dumps(value, default=date_handler, sort_keys=True))
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


def output_hostedcert(gandi, hcert, output_keys, justify=12):
    output_keys = list(output_keys)
    fqdns = 'fqdns' in output_keys
    vhosts = 'vhosts' in output_keys

    if fqdns:
        output_keys.pop(output_keys.index('fqdns'))

    if vhosts:
        output_keys.pop(output_keys.index('vhosts'))

    output_generic(gandi, hcert, output_keys, justify)

    if fqdns:
        for fqdn in hcert['fqdns']:
            gandi.separator_sub_line()
            output_sub_line(gandi, 'fqdn', fqdn['name'], 10)

    if vhosts:
        for vhost in hcert['related_vhosts']:
            gandi.separator_sub_line()
            output_sub_line(gandi, 'vhost', vhost['name'], 10)
            output_sub_line(gandi, 'type', vhost['type'], 10)


def output_domain(gandi, domain, output_keys, justify=12):
    """ Helper to output a domain information."""
    if 'nameservers' in domain:
        domain['nameservers'] = format_list(domain['nameservers'])

    if 'services' in domain:
        domain['services'] = format_list(domain['services'])

    if 'tags' in domain:
        domain['tags'] = format_list(domain['tags'])

    output_generic(gandi, domain, output_keys, justify)

    if 'created' in output_keys:
        output_line(gandi, 'created', domain['date_created'], justify)

    if 'expires' in output_keys:
        date_end = domain.get('date_registry_end')
        if date_end:
            days_left = (date_end - datetime.now()).days
        output_line(gandi, 'expires',
                    '%s (in %d days)' % (date_end, days_left),
                    justify)

    if 'updated' in output_keys:
        output_line(gandi, 'updated', domain['date_updated'], justify)


def output_mailbox(gandi, mailbox, output_keys, justify=16):
    """ Helper to output a mailbox information."""
    quota = 'quota' in output_keys
    responder = 'responder' in output_keys

    if quota:
        output_keys.pop(output_keys.index('quota'))

    if responder:
        output_keys.pop(output_keys.index('responder'))

    if 'aliases' in output_keys:
        mailbox['aliases'] = sorted(mailbox['aliases'])

    output_generic(gandi, mailbox, output_keys, justify)

    if 'fallback' in output_keys:
        output_line(gandi, 'fallback email', mailbox['fallback_email'],
                    justify)

    if quota:
        granted = mailbox['quota']['granted']
        if mailbox['quota']['granted'] == 0:
            granted = 'unlimited'
        output_line(gandi, 'quota usage',
                    '%s KiB / %s' % (mailbox['quota']['used'], granted),
                    justify)

    if responder:
        responder_status = 'yes' if mailbox['responder']['active'] else 'no'
        output_line(gandi, 'responder active', responder_status, justify)
        output_line(gandi, 'responder text', mailbox['responder']['text'],
                    justify)


def output_forward(gandi, domain, forward, justify=14):
    """ Helper to output a mail forward information."""
    for dest in forward['destinations']:
        output_line(gandi, forward['source'], dest, justify)
