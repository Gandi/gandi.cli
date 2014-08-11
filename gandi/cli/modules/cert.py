import os
from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class Certificate(GandiModule):

    @classmethod
    def from_cn(cls, common_name):
        """ retrieve a certificate by it's common name """
        result = [(cert['id'], [cert['cn']] + cert['altnames'])
                  for cert in cls.list()]

        ret = {}
        for id_, fqdns in result:
            for fqdn in fqdns:
                ret.setdefault(fqdn, []).append(id_)

        cert_id = ret.get(common_name)
        if not cert_id:
            return

        return cert_id

    @classmethod
    def usable_ids(cls, id, accept_multi=True):
        try:
            qry_id = cls.from_cn(id)
            if not qry_id:
                qry_id = [int(id)]
        except Exception:
            qry_id = None

        if not qry_id or not accept_multi and len(qry_id) != 1:
           msg = 'unknown identifier %s' % id
           cls.error(msg)

        return qry_id if accept_multi else qry_id[0]

    @classmethod
    def usable_id(cls, id):
        return cls.usable_ids(id, False)

    @classmethod
    def package_list(cls, options=None):
        """ list possible certificate packages """
        options = options or {}
        return cls.safe_call('cert.package.list', options)

    @classmethod
    def list(cls, options=None):
        """ list certificates """
        options = options or {}
        return cls.call('cert.list', options)

    @classmethod
    def info(cls, id):
        """display information about a certificate"""
        return cls.call('cert.info', cls.usable_id(id))
