""" Domain commands module. """

import time

from dateutil.parser import isoparse

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DomainNotAvailable


class Domain(GandiModule):

    """ Module to handle CLI commands.

    $ gandi domain create
    $ gandi domain info
    $ gandi domain list

    """
    api_url = 'https://api.gandi.net/v5/domain'

    @classmethod
    def list(cls, limit=100):
        """List operation."""
        return cls.json_get(f"{cls.api_url}/domains?per_page={limit}")

    @classmethod
    def info(cls, fqdn):
        """Display information about a domain."""
        return cls.json_get(f"{cls.api_url}/domains/{fqdn}")

    @classmethod
    def create(cls, fqdn, duration, owner, admin, tech, bill, nameserver,
               extra_parameter, background):
        """Create a domain."""
        fqdn = fqdn.lower()
        if not background and not cls.intty():
            background = True

        result = cls.call('domain.available', [fqdn])
        while result[fqdn] == 'pending':
            time.sleep(1)
            result = cls.call('domain.available', [fqdn])

        if result[fqdn] == 'unavailable':
            raise DomainNotAvailable('%s is not available' % fqdn)

        # retrieve handle of user and save it to configuration
        user_handle = cls.call('contact.info')['handle']
        cls.configure(True, 'api.handle', user_handle)

        owner_ = owner or user_handle
        admin_ = admin or user_handle
        tech_ = tech or user_handle
        bill_ = bill or user_handle

        domain_params = {
            'duration': duration,
            'owner': owner_,
            'admin': admin_,
            'tech': tech_,
            'bill': bill_,
        }

        if nameserver:
            domain_params['nameservers'] = nameserver

        if extra_parameter:
            domain_params['extra'] = {}
            for extra in extra_parameter:
                domain_params['extra'][extra[0]] = extra[1]

        result = cls.call('domain.create', fqdn, domain_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Creating your domain.')
        cls.display_progress(result)
        cls.echo('Your domain %s has been created.' % fqdn)

    @classmethod
    def renew(cls, fqdn, duration, background):
        """Renew a domain."""
        fqdn = fqdn.lower()
        if not background and not cls.intty():
            background = True

        domain_info = cls.info(fqdn)

        current_year = isoparse(domain_info['dates']['registry_ends_at']).year
        domain_params = {
            'duration': duration,
            'current_year': current_year,
        }

        result = cls.call('domain.renew', fqdn, domain_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Renewing your domain.')
        cls.display_progress(result)
        cls.echo('Your domain %s has been renewed.' % fqdn)

    @classmethod
    def autorenew_deactivate(cls, fqdn):
        """Activate deautorenew"""
        fqdn = fqdn.lower()

        result = cls.call('domain.autorenew.deactivate', fqdn)

        return result

    @classmethod
    def autorenew_activate(cls, fqdn):
        """Activate autorenew"""
        fqdn = fqdn.lower()

        result = cls.call('domain.autorenew.activate', fqdn)

        return result

    @classmethod
    def from_fqdn(cls, fqdn):
        """Retrieve domain id associated to a FQDN."""
        result = cls.list({'fqdn': fqdn})
        if len(result) > 0:
            return result[0]['id']

    @classmethod
    def usable_id(cls, id):
        """Retrieve id from input which can be fqdn or id."""
        # Check if it's already an integer.
        try:
            qry_id = int(id)
        except Exception:
            # Otherwise, assume it's a FQDN.
            # This will return `None` if the FQDN is not found.
            qry_id = cls.from_fqdn(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
