""" Status commands module. """

from datetime import datetime
from gandi.cli.core.base import GandiModule


class Status(GandiModule):

    """ Module to handle CLI commands.

    $ gandi status
    """

    base_url = 'https://status.gandi.net/api'

    @classmethod
    def descriptions(cls):
        schema = cls.json_call('%s/status/schema' % cls.base_url)
        descs = {}
        for val in schema['fields']['status']['value']:
            descs.update(val)
        return descs

    @classmethod
    def services(cls):
        """Retrieve services statuses for status.gandi.net."""
        return cls.json_call('%s/services' % cls.base_url)

    @classmethod
    def events(cls, filters):
        """Retrieve events details for status.gandi.net."""
        current = filters.pop('current', False)
        filter_url = '&'.join(['%s=%s' % (key, val)
                               for key, val in filters.iteritems()])
        events = cls.json_call('%s/events?%s' % (cls.base_url, filter_url))
        now = datetime.utcnow()
        dtformat = '%Y-%m-%dT%H:%M:%S'
        current_events = []
        for event in events:
            if not current:
                current_events.append(event)
                continue
            # don't parse the timezone without dateutil
            ev_start = datetime.strptime(event['date_start'][:-6], dtformat)
            if ev_start < now and not event['date_end']:
                current_events.append(event)

        return events
