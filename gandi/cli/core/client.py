# -*- coding: utf-8 -*-
""" XML-RPC connection helper. """

import socket

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

from gandi.cli import __version__
from gandi.cli.core.utils.xmlrpc import RequestsTransport, requests


class APICallFailed(Exception):

    """ Raise when an error occured during an API call. """

    def __init__(self, errors, code=None):
        """ Initialize exception. """
        self.errors = errors
        self.code = code


class GandiTransport(RequestsTransport):

    """ Mixin to send custom User-Agent in requests."""

    user_agent = 'gandi.cli/%s' % __version__


class DryRunException(APICallFailed):
    dry_run = None

    def __init__(self, message, code, dry_run):
        super(DryRunException, self).__init__(message, code)
        self.dry_run = dry_run


class XMLRPCClient(object):

    """ Class wrapper for xmlrpc calls to Gandi public API. """

    def __init__(self, host, debug=False):
        """ Initialize xml-rpc endpoint connector. """
        self.debug = debug
        self.endpoint = xmlrpclib.ServerProxy(
            host, allow_none=True, use_datetime=True,
            transport=GandiTransport(use_datetime=True, host=host))

    def request(self, apikey, method, *args, **kwargs):
        """ Make a xml-rpc call to remote API. """
        dry_run = kwargs.get('dry_run', False)

        try:
            func = getattr(self.endpoint, method)
            return func(apikey, *args)
        except (socket.error, requests.exceptions.ConnectionError):
            msg = 'Gandi API service is unreachable'
            raise APICallFailed(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error: %s' % err
            if dry_run:
                args[-1]['--dry-run'] = True
                ret = func(apikey, *args)
                raise DryRunException(msg, err.faultCode, ret)
            raise APICallFailed(msg, err.faultCode)
        except TypeError as err:
            msg = 'An unknown error as occured: %s' % err
            raise APICallFailed(msg)
