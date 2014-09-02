""" SSH key commands module. """

import os
from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import DuplicateResults


class Sshkey(GandiModule):

    """ Module to handle CLI commands.

    $ gandi sshkey create
    $ gandi sshkey delete
    $ gandi sshkey info
    $ gandi sshkey list

    """

    @classmethod
    def from_name(cls, name):
        """Retrieve a sshkey id associated to a name."""
        sshkeys = cls.list({'name': name})
        if len(sshkeys) == 1:
            return sshkeys[0]['id']
        elif not sshkeys:
            return

        raise DuplicateResults('sshkey name %s is ambiguous.' % name)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be name or id."""
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
        """ List ssh keys."""
        options = options if options else {}
        return cls.call('hosting.ssh.list', options)

    @classmethod
    def info(cls, id):
        """ Display information about an ssh key. """
        return cls.call('hosting.ssh.info', cls.usable_id(id))

    @classmethod
    def create(cls, name, value):
        """ Create a new ssh key."""
        sshkey_params = {
            'name': name,
            'value': value,
        }

        result = cls.call('hosting.ssh.create', sshkey_params)
        return result

    @classmethod
    def delete(cls, id):
        """Delete this ssh key."""
        return cls.call('hosting.ssh.delete', cls.usable_id(id))


class SshkeyHelper(object):

    """ Helper class to handle sshkey configuration entry. """

    @classmethod
    def convert_sshkey(cls, sshkey):
        """ Return dict param with valid entries for vm/paas methods. """
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
