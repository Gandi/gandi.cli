from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class SnapshotProfile(GandiModule):

    @classmethod
    def from_name(cls, name):
        """ retrieve a snapshot profile accsociated to a name """
        snps = cls.list({'name': name})
        if len(snps) == 1:
            return snps[0]['id']
        elif not snps:
            return

        raise DuplicateResults('snapshot profile name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
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
        """ list all snapshot profiles """
        options = options or {}

        result = []
        if not target or target == 'paas':
            for profile in cls.call('paas.snapshotprofile.list', options):
                profile['target'] = 'paas'
                result.append((profile['id'], profile))

        if not target or target == 'vm':
            for profile in cls.call('hosting.snapshotprofile.list', options):
                profile['target'] = 'vm'
                result.append((profile['id'], profile))

        result = sorted(result, key=lambda item: item[0])
        return [profile for id_, profile in result]

    @classmethod
    def info(cls, resource):
        """ """
        snps = cls.list({'id': cls.usable_id(resource)})
        if len(snps) == 1:
            return snps[0]
        elif not snps:
            return

        raise DuplicateResults('snapshot profile %s is ambiguous.' % resource)
