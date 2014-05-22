# -*- coding: utf-8 -*-
import socket
import xmlrpclib


class APICallFailed(Exception):
    """ Raise when an error occured during an api call"""

    def __init__(self, errors):
        self.errors = errors


class XMLRPCClient(object):
    """ Class wrapper for xmlrpc calls to Gandi public API """

    def __init__(self, host, debug=False):
        self.debug = debug
        self.endpoint = xmlrpclib.ServerProxy(host)

    def request(self, apikey, method, *args):
        try:
            func = getattr(self.endpoint, method)
            return func(apikey, *args)
        except socket.error:
            msg = 'Gandi API service is unreachable'
            raise APICallFailed(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error: %s' % err
            raise APICallFailed(msg)
        except TypeError as err:
            msg = 'An unknown error as occured: %s' % err
            raise APICallFailed(msg)
