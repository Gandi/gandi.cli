"""
Security enhancements for xmlrpc.
"""

try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib

import requests

class RequestsTransport(xmlrpclib.Transport):
    """
    Drop in Transport for xmlrpclib that uses Requests instead of httplib
    # https://gist.github.com/chrisguitarguy/2354951
    # https://github.com/mardiros/pyshop/blob/master/pyshop/helpers/pypi.py
    """


    def request(self, host, handler, request_body, verbose):
        """
        Make an xmlrpc request.
        """
        headers = {'Accept': 'text/xml',
                   'Content-Type': 'text/xml'}
        url = 'https://%s%s' % (host, handler,)
        try:
            resp = requests.post(url, data=request_body, headers=headers)
        except ValueError:
            raise
        except Exception:
            raise # something went wrong
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
