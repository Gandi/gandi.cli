""" metric module. """

import time
from datetime import datetime

from gandi.cli.core.base import GandiModule


class Metric(GandiModule):

    """ Module to query metrics

    """

    @classmethod
    def query(cls, resources, time_range, query, resource_type, sampler):
        """Query statistics for given resources."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        now = time.time()
        start_utc = datetime.utcfromtimestamp(now - time_range)
        end_utc = datetime.utcfromtimestamp(now)
        date_format = '%Y-%m-%d %H:%M:%S'
        start = start_utc.strftime(date_format)
        end = end_utc.strftime(date_format)
        query = {'start': start,
                 'end': end,
                 'query': query,
                 'resource_id': resources,
                 'resource_type': resource_type,
                 'sampler': sampler}
        return cls.call('hosting.metric.query', query)
