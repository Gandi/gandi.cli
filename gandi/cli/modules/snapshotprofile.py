""" Snapshot profile commands module. """

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class SnapshotProfile(GandiModule):

    """ Module to handle CLI commands.

    $ gandi snapshotprofile info
    $ gandi snapshotprofile list

    """

    @classmethod
    def from_name(cls, name):
        """ Retrieve a snapshot profile accsociated to a name."""
        snps = cls.list({'name': name})
        if len(snps) == 1:
            return snps[0]['id']
        elif not snps:
            return

        raise DuplicateResults('snapshot profile name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be name or id."""
        try:
            qry_id = cls.from_name(id)
            if not qry_id:
                qry_id = int(id)
        except DuplicateResults as exc:
            cls.error(exc.errors)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def list(cls, options=None, target=None):
        """ List all snapshot profiles."""
        options = options or {}

        result = []
        if not target or target == 'paas':
            for profile in cls.safe_call('paas.snapshotprofile.list', options):
                profile['target'] = 'paas'
                result.append((profile['id'], profile))

        if not target or target == 'vm':
            for profile in cls.safe_call('hosting.snapshotprofile.list',
                                         options):
                profile['target'] = 'vm'
                result.append((profile['id'], profile))

        result = sorted(result, key=lambda item: item[0])
        return [profile for id_, profile in result]

    @classmethod
    def info(cls, resource):
        """Display information about a snapshot profile."""
        snps = cls.list({'id': cls.usable_id(resource)})
        if len(snps) == 1:
            return snps[0]
        elif not snps:
            return

        raise DuplicateResults('snapshot profile %s is ambiguous.' % resource)
