""" Domain commands module. """

from gandi.cli.core.base import GandiModule


class Domain(GandiModule):

    """ Module to handle CLI commands.

    $ gandi domain create
    $ gandi domain info
    $ gandi domain list

    """

    @classmethod
    def list(cls, options):
        """List operation."""
        return cls.call('domain.list', options)

    @classmethod
    def info(cls, fqdn):
        """Display information about a domain."""
        return cls.call('domain.info', fqdn)

    @classmethod
    def create(cls, fqdn, duration, owner, admin, tech, bill, background):
        """Create a domain."""
        if not background and not cls.intty():
            background = True

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

        result = cls.call('domain.create', fqdn, domain_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Creating your domain.')
        cls.display_progress(result)
        cls.echo('Your domain %s has been created.' % fqdn)

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
        except:
            # Otherwise, assume it's a FQDN.
            # This will return `None` if the FQDN is not found.
            qry_id = cls.from_fqdn(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
