""" Status commands module. """

try:
    import urllib.parse as uparse
except ImportError:
    import urllib as uparse

from gandi.cli.core.base import GandiModule


class Status(GandiModule):

    """ Module to handle CLI commands.

    $ gandi status

    """

    base_url = 'https://status.gandi.net'
    api_url = 'https://status.gandi.net/api'

    @classmethod
    def descriptions(cls):
        """ Retrieve status descriptions from status.gandi.net. """
        schema = cls.json_call('%s/status/schema' % cls.api_url)
        descs = {}
        for val in schema['fields']['status']['value']:
            descs.update(val)
        return descs

    @classmethod
    def services(cls):
        """Retrieve services statuses from status.gandi.net."""
        return cls.json_call('%s/services' % cls.api_url)

    @classmethod
    def status(cls):
        """Retrieve global status from status.gandi.net."""
        return cls.json_call('%s/status' % cls.api_url)

    @classmethod
    def events(cls, filters):
        """Retrieve events details from status.gandi.net."""
        current = filters.pop('current', False)
        current_params = []
        if current:
            current_params = [('current', 'true')]

        filter_url = uparse.urlencode(list(filters.items()) + current_params)
        events = cls.json_call('%s/events?%s' % (cls.api_url, filter_url))
        return events

    @classmethod
    def event_timeline(cls, event):
        """Retrieve event timeline url for status.gandi.net."""
        return '%s/timeline/events/%s' % (cls.base_url, event['id'])
