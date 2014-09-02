# -*- coding: utf-8 -*-
""" XML-RPC connection helper. """

import socket
import xmlrpclib

from gandi.cli import __version__


class APICallFailed(Exception):

    """ Raise when an error occured during an API call. """

    def __init__(self, errors, code=None):
        """ Initialize exception. """
        self.errors = errors
        self.code = code


class GandiTransport(xmlrpclib.SafeTransport):

    """ Mixin to send custom User-Agent in requests."""

    _user_agent = None

    def send_user_agent(self, connection):
        """ Add User-Agent header to request if not already existing."""
        if not self._user_agent:
            self._user_agent = '%s %s' % (xmlrpclib.Transport.user_agent,
                                          'gandi.cli/%s' % __version__)
        connection.putheader('User-Agent', self._user_agent)


class XMLRPCClient(object):

    """ Class wrapper for xmlrpc calls to Gandi public API. """

    def __init__(self, host, debug=False):
        """ Initialize xml-rpc endpoint connector. """
        self.debug = debug
        self.endpoint = xmlrpclib.ServerProxy(host, allow_none=True,
                                              use_datetime=True)

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
