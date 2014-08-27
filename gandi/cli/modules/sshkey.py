import os
from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class Sshkey(GandiModule):

    @classmethod
    def from_name(cls, name):
        '''retrieve a sshkey id associated to a name'''
        sshkeys = cls.list({'name': name})
        if len(sshkeys) == 1:
            return sshkeys[0]['id']
        elif not sshkeys:
            return

        raise DuplicateResults('sshkey name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
        try:
            # id is maybe a sshkey name
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


class SshkeyHelper(object):

    @classmethod
    def convert_sshkey(cls, sshkey):
        params = {}
        if sshkey:
            params['keys'] = []
            for ssh in sshkey:
                if os.path.exists(os.path.expanduser(ssh)):
                    if 'ssh_key' in params:
                        cls.echo("Can't have more than one sshkey file.")
                        continue
                    with open(ssh) as fdesc:
                        sshkey_ = fdesc.read()
                    if sshkey_:
                        params['ssh_key'] = sshkey_
                else:
                    sshkey_id = Sshkey.usable_id(ssh)
                    if sshkey_id:
                        params['keys'].append(sshkey_id)
                    else:
                        cls.echo('This is not a ssh key %s' % ssh)

            if not params['keys']:
                params.pop('keys')

        return params
