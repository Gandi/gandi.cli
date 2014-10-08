""" Iface commands module. """

from gandi.cli.core.base import GandiModule


class Iface(GandiModule):

    """ Module to handle CLI commands.

    $ gandi iface list
    $ gandi iface info

    """

    @classmethod
    def list(cls, options=None):
        """ List all ifaces."""
        options = options or {}
        return cls.call('hosting.iface.list', options)

    @classmethod
    def _info(cls, iface_id):
        """ Get information about an iface."""
        return cls.call('hosting.iface.info', iface_id)

    @classmethod
    def info(cls, num):
        """ Get information about an iface."""
        return cls._info(cls.usable_id(num))

    @classmethod
    def from_num(cls, num):
        """Retrieve iface id associated to a num."""
        result = cls.list()
        ifaces = {}
        for iface in result:
            ifaces[iface['num']] = iface['id']

        return ifaces.get(int(num))

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be num or id."""
        try:
            # id is maybe a num
            qry_id = cls.from_num(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
