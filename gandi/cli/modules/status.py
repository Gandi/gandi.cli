""" Status commands module. """

from gandi.cli.core.base import GandiModule


class Status(GandiModule):

    """ Module to handle CLI commands.

    $ gandi status

    """

    statuspage_api_url = 'https://gandi.statuspage.io/api/v2'

    @classmethod
    def summary(cls):
        """Retrieve summary from gandi.statuspage.io."""
        return cls.json_get('%s/summary.json' % cls.statuspage_api_url,
                            empty_key=True, send_key=False)
