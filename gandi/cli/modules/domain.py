from gandi.cli.core.base import GandiModule


class Domain(GandiModule):

    @classmethod
    def list(cls, options):
        """list operation"""

        return cls.call('domain.list', options)

    @classmethod
    def info(cls, fqdn):
        """display information about a domain"""

        return cls.call('domain.info', fqdn)

    @classmethod
    def create(cls, fqdn, duration, owner, admin, tech, bill, background):
        """Buy a domain."""

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
        cls.echo("We're creating your domain.")
        cls.display_progress(result)
        cls.echo('Your domain %s have been created.' % fqdn)

    @classmethod
    def from_fqdn(cls, fqdn):
        """retrieve domain id associated to a FQDN"""

        result = cls.list({})
        domains = {}
        for domain in result:
            domains[domain['fqdn']] = domain['id']

        return domains.get(fqdn)

    @classmethod
    def usable_id(cls, id):
        try:
            # id is maybe a fqdn
            qry_id = cls.from_fqdn(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
