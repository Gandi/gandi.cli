"""
Security enhancements for xmlrpc.
"""
from __future__ import print_function

import sys

try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib

try:
    import requests
except ImportError:
    print('python requests is required, please reinstall.', file=sys.stderr)
    sys.exit(1)


class RequestsTransport(xmlrpclib.Transport):
    """
    Drop in Transport for xmlrpclib that uses Requests instead of httplib
    # https://gist.github.com/chrisguitarguy/2354951
    # https://github.com/mardiros/pyshop/blob/master/pyshop/helpers/pypi.py
    """

    use_https = True

    def __init__(self, use_datetime=0, host=None):
        xmlrpclib.Transport.__init__(self, use_datetime)
        if host:
            self.use_https = 'https' in host

    def request(self, host, handler, request_body, verbose):
        """
        Make an xmlrpc request.
        """
        headers = {'User-Agent': self.user_agent,
                   'Accept': 'text/xml',
                   'Content-Type': 'text/xml'}

        url = self._build_url(host, handler)
        try:
            resp = requests.post(url, data=request_body, headers=headers)
        except ValueError:
            raise
        except Exception:
            raise  # something went wrong
        else:
            try:
                resp.raise_for_status()
            except requests.RequestException as e:
                raise xmlrpclib.ProtocolError(url, resp.status_code,
                                              str(e), resp.headers)
            else:
                return self.parse_response(resp)

    def parse_response(self, resp):
        """
        Parse the xmlrpc response.
        """
        p, u = self.getparser()
        p.feed(resp.content)
        p.close()
        return u.close()

    def _build_url(self, host, handler):
        """
        Build a url for our request based on the host, handler and use_https
        property
        """
        scheme = 'https' if self.use_https else 'http'
        return '%s://%s%s' % (scheme, host, handler)
