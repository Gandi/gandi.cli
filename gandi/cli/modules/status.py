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
        schema = cls.json_get('%s/status/schema' % cls.api_url, empty_key=True,
                              send_key=False)
        descs = {}
        for val in schema['fields']['status']['value']:
            descs.update(val)
        return descs

    @classmethod
    def services(cls):
        """Retrieve services statuses from status.gandi.net."""
        return cls.json_get('%s/services' % cls.api_url, empty_key=True,
                            send_key=False)

    @classmethod
    def status(cls):
        """Retrieve global status from status.gandi.net."""
        return cls.json_get('%s/status' % cls.api_url, empty_key=True,
                            send_key=False)

    @classmethod
    def events(cls, filters):
        """Retrieve events details from status.gandi.net."""
        current = filters.pop('current', False)
        current_params = []
        if current:
            current_params = [('current', 'true')]

        filter_url = uparse.urlencode(sorted(list(filters.items())) + current_params)  # noqa
        events = cls.json_get('%s/events?%s' % (cls.api_url, filter_url),
                              empty_key=True, send_key=False)
        return events

    @classmethod
    def event_timeline(cls, event):
        """Retrieve event timeline url for status.gandi.net."""
        return '%s/timeline/events/%s' % (cls.base_url, event['id'])
