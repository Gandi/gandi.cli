""" Dnssec commands module. """

from gandi.cli.core.base import GandiModule


class DNSSEC(GandiModule):

    """ Module to handle CLI commands.

    $ gandi dnssec create
    $ gandi dnssec list
    $ gandi dnssec delete

    """

    @classmethod
    def list(cls, fqdn):
        """List operation."""
        return cls.call('domain.dnssec.list', fqdn)

    @classmethod
    def create(cls, fqdn, flags, algorithm, public_key):
        """Create a dnssec key."""
        fqdn = fqdn.lower()

        params = {
            'flags': flags,
            'algorithm': algorithm,
            'public_key': public_key,
        }

        result = cls.call('domain.dnssec.create', fqdn, params)

        return result

    @classmethod
    def delete(cls, id):
        """Delete this dnss key."""
        return cls.call('domain.dnssec.delete', id)
