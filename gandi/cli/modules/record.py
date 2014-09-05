""" Record commands module. """

from gandi.cli.core.base import GandiModule


class Zone(GandiModule):

    """ Helper class for domain DNS zones. """

    @classmethod
    def new(cls, zone_id):
        """Create a new zone version."""
        return cls.call('domain.zone.version.new', zone_id)

    @classmethod
    def set(cls, zone_id, version_id):
        """Set active version of a zone."""
        return cls.call('domain.zone.version.set', zone_id, version_id)


class Record(GandiModule):

    """ Module to handle CLI commands.

    $ gandi record list
    $ gandi record create

    """

    @classmethod
    def list(cls, zone_id):
        """List zone records for a zone."""
        return cls.call('domain.zone.record.list', zone_id, 0)

    @classmethod
    def add(cls, zone_id, version_id, record):
        """Add record to a zone."""
        return cls.call('domain.zone.record.add', zone_id, version_id, record)

    @classmethod
    def create(cls, zone_id, record):
        """Create a new zone version for record."""
        cls.echo('Creating new zone version')
        new_version_id = Zone.new(zone_id)

        cls.echo('Updating zone version')
        cls.add(zone_id, new_version_id, record)

        cls.echo('Activation of new zone version')
        Zone.set(zone_id, new_version_id)

        return new_version_id
