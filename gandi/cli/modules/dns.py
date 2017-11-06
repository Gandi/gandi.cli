""" LiveDNS commands module. """
import json

from gandi.cli.core.base import GandiModule


class Dns(GandiModule):

    """ Module to handle CLI commands.

    $ gandi dns create
    $ gandi dns delete
    $ gandi dns domain.list
    $ gandi dns list
    $ gandi dns keys create
    $ gandi dns keys delete
    $ gandi dns keys info
    $ gandi dns keys list
    $ gandi dns keys recover

    """

    api_url = 'https://dns.api.gandi.net/api/v5'

    @classmethod
    def get_sort_url(cls, url, sort_by=None):
        if sort_by:
            if not sort_by.startswith('rrset'):
                sort_key = 'rrset_%s' % sort_by
            else:
                sort_key = sort_by
            url = '%s?sort_by=%s' % (url, sort_key)
        return url

    @classmethod
    def list(cls):
        """List domains."""
        return cls.json_get('%s/domains' % cls.api_url)

    @classmethod
    def type_list(cls):
        """List supported records type."""
        return cls.json_get('%s/dns/rrtypes' % cls.api_url)

    @classmethod
    def get_fqdn_info(cls, fqdn):
        """Retrieve information about a domain"""
        return cls.json_get('%s/domains/%s' % (cls.api_url, fqdn))

    @classmethod
    def records(cls, fqdn, sort_by=None, text=False):
        """Display records information about a domain."""
        meta = cls.get_fqdn_info(fqdn)
        url = meta['domain_records_href']
        kwargs = {}
        if text:
            kwargs = {'headers': {'Accept': 'text/plain'}}
        return cls.json_get(cls.get_sort_url(url, sort_by), **kwargs)

    @classmethod
    def add_record(cls, fqdn, name, type, value, ttl):
        """Create record for a domain."""
        data = {
            "rrset_name": name,
            "rrset_type": type,
            "rrset_values": value,
        }
        if ttl:
            data['rrset_ttl'] = int(ttl)
        meta = cls.get_fqdn_info(fqdn)
        url = meta['domain_records_href']
        return cls.json_post(url, data=json.dumps(data))

    @classmethod
    def update_record(cls, fqdn, name, type, value, ttl, content):
        """Update all records for a domain."""
        data = {
            "rrset_name": name,
            "rrset_type": type,
            "rrset_values": value,
        }
        if ttl:
            data['rrset_ttl'] = int(ttl)
        meta = cls.get_fqdn_info(fqdn)
        if content:
            url = meta['domain_records_href']
            kwargs = {'headers': {'Content-Type': 'text/plain'},
                      'data': content}
            return cls.json_put(url, **kwargs)

        url = '%s/domains/%s/records/%s/%s' % (cls.api_url, fqdn, name, type)
        return cls.json_put(url, data=json.dumps(data))

    @classmethod
    def del_record(cls, fqdn, name, type):
        """Delete record for a domain."""
        meta = cls.get_fqdn_info(fqdn)
        url = meta['domain_records_href']
        delete_url = url
        if name:
            delete_url = '%s/%s' % (delete_url, name)
        if type:
            delete_url = '%s/%s' % (delete_url, type)
        return cls.json_delete(delete_url)

    @classmethod
    def keys(cls, fqdn, sort_by=None):
        """Display keys information about a domain."""
        meta = cls.get_fqdn_info(fqdn)
        url = meta['domain_keys_href']
        return cls.json_get(cls.get_sort_url(url, sort_by))

    @classmethod
    def keys_info(cls, fqdn, key):
        """Retrieve key information."""
        return cls.json_get('%s/domains/%s/keys/%s' %
                            (cls.api_url, fqdn, key))

    @classmethod
    def keys_create(cls, fqdn, flag):
        """Create new key entry for a domain."""
        data = {
            "flags": flag,
        }
        meta = cls.get_fqdn_info(fqdn)
        url = meta['domain_keys_href']
        ret, headers = cls.json_post(url, data=json.dumps(data),
                                     return_header=True)
        return cls.json_get(headers['location'])

    @classmethod
    def keys_delete(cls, fqdn, key):
        """Delete a key for a domain."""
        return cls.json_delete('%s/domains/%s/keys/%s' %
                               (cls.api_url, fqdn, key))

    @classmethod
    def keys_recover(cls, fqdn, key):
        """Recover deleted key for a domain."""
        data = {
            "deleted": False,
        }
        return cls.json_put('%s/domains/%s/keys/%s' % (cls.api_url, fqdn, key),
                            data=json.dumps(data),)
