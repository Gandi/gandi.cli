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
    def list(cls, zone_id, options=None):
        """List zone records for a zone."""
        options = options if options else {}
        return cls.call('domain.zone.record.list', zone_id, 0, options)

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

    @classmethod
    def delete(cls, zone_id, record):
        """Delete a record for a zone"""
        cls.echo('Creating new zone record')
        new_version_id = Zone.new(zone_id)

        cls.echo('Deleting zone record')
        cls.call('domain.zone.record.delete', zone_id, new_version_id, record)

        cls.echo('Activation of new zone version')
        Zone.set(zone_id, new_version_id)

        return new_version_id

    @classmethod
    def zone_update(cls, zone_id, records):
        """Update records for a zone"""
        cls.echo('Creating new zone file')
        new_version_id = Zone.new(zone_id)

        cls.echo('Updating zone records')
        cls.call('domain.zone.record.set', zone_id, new_version_id, records)

        cls.echo('Activation of new zone version')
        Zone.set(zone_id, new_version_id)

        return new_version_id

    @classmethod
    def update(cls, zone_id, old_record, new_record):
        """Update a record in a zone file"""
        cls.echo('Creating new zone file')
        new_version_id = Zone.new(zone_id)

        new_record = new_record.split(' ', 4)
        params_newrecord = {'name': new_record[0], 'ttl': int(new_record[1]),
                            'type': new_record[2], 'value': new_record[3]}

        old_record = old_record.split(' ', 4)
        params = {'name': old_record[0], 'ttl': int(old_record[1]),
                  'type': old_record[2], 'value': old_record[3]}
        record = cls.call('domain.zone.record.list', zone_id, new_version_id,
                          params)

        if record:
            cls.echo('Updating zone records')
            cls.call('domain.zone.record.update', zone_id, new_version_id,
                     {'id': int(record[0]['id'])}, params_newrecord)
            cls.echo('Activation of new zone version')
            Zone.set(zone_id, new_version_id)
            return new_version_id
        else:
            cls.echo('The record to update does not exist. Check records'
                     ' already created with `gandi record list example.com'
                     ' --output`')
            return False
