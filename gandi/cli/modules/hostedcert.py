""" Hosted certificate commands module. """

import os
import re
from click import UsageError
from gandi.cli.core.base import GandiModule


class HostedCert(GandiModule):
    """ Module to handle CLI commands.

    $ gandi certstore list
    $ gandi certstore info
    $ gandi certstore create
    $ gandi certstore delete
    """

    @classmethod
    def from_fqdn(cls, fqdn):
        return cls.list({'fqdns': '%s' % fqdn, 'state': 'created'})

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from single input. """
        hcs = cls.from_fqdn(id)
        if hcs:
            return [hc_['id'] for hc_ in hcs]

        try:
            return int(id)
        except (TypeError, ValueError):
            pass

    @classmethod
    def list(cls, options=None):
        """ List hosted certificates. """
        options = options or {}
        return cls.call('cert.hosted.list', options)

    @classmethod
    def info(cls, id):
        """ Display information about a hosted certificate. """
        return cls.call('cert.hosted.info', id)

    @classmethod
    def infos(cls, fqdn):
        """ Display information about hosted certificates for a fqdn. """
        ids = cls.usable_id(fqdn)
        if not ids:
            return []

        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        return [cls.info(id_) for id_ in ids]

    @classmethod
    def create(cls, key, crt):
        """ Add a new crt in the hosted cert store. """
        options = {'crt': crt, 'key': key}
        return cls.call('cert.hosted.create', options)
