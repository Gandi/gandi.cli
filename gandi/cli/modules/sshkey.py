from gandi.cli.core.base import GandiModule


class Sshkey(GandiModule):

    @classmethod
    def from_name(cls, name):
        '''retrieve a sshkey id associated to a name'''
        sshkeys = cls.list({'name': name})
        if len(sshkeys) == 1:
            return sshkeys[0]['id']

        if not sshkeys:
            cls.error('unable to find sshkey named %r' % name)

        cls.error('sshkey name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
        try:
            # id is maybe a sshkey name
            qry_id = cls.from_name(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def list(cls, options=None):
        '''list ssh keys'''
        options = options if options else {}
        return cls.call('hosting.ssh.list', options)

    @classmethod
    def info(cls, id):
        '''display information about an ssh key'''
        return cls.call('hosting.ssh.info', cls.usable_id(id))

    @classmethod
    def create(cls, name, value):
        '''create a new ssh key'''
        sshkey_params = {
            'name': name,
            'value': value,
        }

        result = cls.call('hosting.ssh.create', sshkey_params)
        return result

    @classmethod
    def delete(cls, id):
        '''delete this ssh key'''
        return cls.call('hosting.ssh.delete', cls.usable_id(id))
