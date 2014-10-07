# -*- coding: utf-8 -*-
""" XML-RPC connection helper. """

import socket

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

from gandi.cli import __version__
from gandi.cli.core.utils.xmlrpc import RequestsTransport


class APICallFailed(Exception):

    """ Raise when an error occured during an API call. """

    def __init__(self, errors, code=None):
        """ Initialize exception. """
        self.errors = errors
        self.code = code


class GandiTransport(RequestsTransport):

    """ Mixin to send custom User-Agent in requests."""

    user_agent = 'gandi.cli/%s' % __version__


class XMLRPCClient(object):

    """ Class wrapper for xmlrpc calls to Gandi public API. """

    def __init__(self, host, debug=False):
        """ Initialize xml-rpc endpoint connector. """
        self.debug = debug
        self.endpoint = xmlrpclib.ServerProxy(
            host, allow_none=True, use_datetime=True,
            transport=GandiTransport(use_datetime=True, host=host))

    def request(self, apikey, method, *args):
        """ Make a xml-rpc call to remote API. """
        try:
            func = getattr(self.endpoint, method)
            return func(apikey, *args)
        except socket.error:
            msg = 'Gandi API service is unreachable'
            raise APICallFailed(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error: %s' % err
            raise APICallFailed(msg, err.faultCode)
        except TypeError as err:
            msg = 'An unknown error as occured: %s' % err
            raise APICallFailed(msg)
