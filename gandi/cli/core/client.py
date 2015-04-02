# -*- coding: utf-8 -*-
""" XML-RPC connection helper. """

from __future__ import print_function

import sys
import json
import socket

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

try:
    import requests
except ImportError:
    print('python requests is required, please reinstall.', file=sys.stderr)
    sys.exit(1)

from gandi.cli import __version__
from gandi.cli.core.utils.xmlrpc import RequestsTransport


class APICallFailed(Exception):

    """ Raise when an error occurred during an API call. """

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
        self.host = host
        self.endpoint = xmlrpclib.ServerProxy(
            host, allow_none=True, use_datetime=True,
            transport=GandiTransport(use_datetime=True, host=host))

    def request(self, method, apikey, *args, **kwargs):
        """ Make a xml-rpc call to remote API. """
        dry_run = kwargs.get('dry_run', False)
        return_dry_run = kwargs.get('return_dry_run', False)
        if return_dry_run:
            args[-1]['--dry-run'] = True

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
            msg = 'An unknown error has occurred: %s' % err
            raise APICallFailed(msg)


class JsonClient(object):

    """ Class wrapper for JSON calls. """

    @classmethod
    def request(cls, url, data=None):
        """ Make a json call to remote API. """
        user_agent = 'gandi.cli/%s' % __version__

        headers = {'User-Agent': user_agent,
                   'Content-Type': 'application/json; charset=utf-8'}
        try:
            response = requests.get(url, data=json.dumps(data),
                                    headers=headers)
            response.raise_for_status()
            return json.loads(response.content.decode())
        except (socket.error, requests.exceptions.ConnectionError):
            msg = 'Remote API service is unreachable'
            raise APICallFailed(msg)
        except Exception as err:
            msg = 'An unknown error has occurred: %s' % err
            raise APICallFailed(msg)
