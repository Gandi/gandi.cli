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
        """ Retrieve status descriptions from status.gandi.net. """
        schema = cls.json_call('%s/status/schema' % cls.base_url)
        descs = {}
        for val in schema['fields']['status']['value']:
            descs.update(val)
        return descs

    @classmethod
    def services(cls):
        """Retrieve services statuses from status.gandi.net."""
        return cls.json_call('%s/services' % cls.base_url)

    @classmethod
    def events(cls, filters):
        """Retrieve events details from status.gandi.net."""
        current = filters.pop('current', False)
        current_params = []
        if current:
            dtformat = '%Y-%m-%d%%20%H:%M'
            now = datetime.utcnow().strftime(dtformat)
            current_params = ['date_start__lt=%s' % now,
                              'estimate_date_end=null']
        filter_url = '&'.join(['%s=%s' % (key, val)
                               for key, val in filters.iteritems()]
                              + current_params)

        events = cls.json_call('%s/events?%s' % (cls.base_url, filter_url))
        return events
