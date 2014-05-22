
import time

from gandi.conf import GandiModule


class Vhost(GandiModule):

    @classmethod
    def list(cls, options=None):
        """list virtual hosts"""

        if not options:
            options = {}

        return cls.call('paas.vhost.list', options)


class Paas(GandiModule):

    @classmethod
    def list(cls, options):
        """list Paas instances"""

        return cls.call('paas.list', options)

    @classmethod
    def info(cls, id):
        """display information about a Paas instance"""

        return cls.call('paas.info', cls.usable_id(id))

    @classmethod
    def delete(cls, id):
        """delete a Paas instance"""

        return cls.call('paas.delete', cls.usable_id(id))

    @classmethod
    def create(cls, name, size, type, quantity, duration, datacenter_id, vhosts,
               password, snapshot_profile, interactive, ssh_key):
        """create a new PaaS instance.

        you can provide a ssh_key on command line calling this command as:

        >>> cat ~/.ssh/id_rsa.pub | gandi paas -

        or specify a configuration entry named 'ssh_key_path' containing
        path to your ssh_key file

        >>> gandi config ssh_key_path ~/.ssh/id_rsa.pub

        """

        if interactive and not cls.intty():
            interactive = False

        # priority to command line parameters
        # then env var
        # then local configuration
        # then global configuration
        if datacenter_id:
            datacenter_id_ = datacenter_id
        else:
            datacenter_id_ = int(cls.get('datacenter_id'))

        if name:
            name_ = name
        else:
            name_ = cls.get('name')

        if size:
            size_ = size
        else:
            size_ = cls.get('size')

        if type:
            type_ = type
        else:
            type_ = cls.get('type')

        if quantity:
            quantity_ = quantity
        else:
            quantity_ = int(cls.get('quantity', 0))

        if password:
            password_ = password
        else:
            password_ = cls.get('password')

        if duration:
            duration_ = duration
        else:
            duration_ = cls.get('duration')

        paas_params = {
            'name': name_,
            'size': size_,
            'type': type_,
            'password': password_,
            'duration': duration_,
            'datacenter_id': datacenter_id_,
        }
        if vhosts:
            vhosts_ = vhosts
        else:
            vhosts_ = cls.get('vhosts')
        if vhosts_ is not None:
            paas_params['vhosts'] = vhosts_

        if quantity:
            quantity_ = quantity
        else:
            quantity_ = cls.get('quantity')
        if quantity_ is not None:
            paas_params['quantity'] = quantity_

        if ssh_key:
            ssh_key_ = ssh_key
        else:
            ssh_key_ = cls.get('ssh_key')
        if ssh_key_ is not None:
            paas_params['ssh_key'] = ssh_key_

        result = cls.call('paas.create', paas_params)
        if not interactive:
            return result
        else:
            # interactive mode, run a progress bar
            from datetime import datetime
            start_crea = datetime.utcnow()

            cls.echo("We're creating your first PaaS with default settings.")
            # count number of operations, 3 steps per operation
            count_operations = len(result) * 3
            crea_done = False
            while not crea_done:
                op_score = 0
                for oper in result:
                    op_step = cls.call('operation.info', oper['id'])['step']
                    if op_step == 'WAIT':
                        op_score += 1
                    elif op_step == 'RUN':
                        op_score += 2
                    elif op_step == 'DONE':
                        op_score += 3
                    else:
                        msg = 'step %s unknown, exiting creation' % op_step
                        cls.error(msg)

                cls.update_progress(float(op_score) / count_operations,
                                    start_crea)

                if op_score == count_operations:
                    crea_done = True

                time.sleep(.5)

            cls.echo('')
            cls.echo('Your PaaS %s have been created.' % name_)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a vhost
            qry_id = cls.from_vhost(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def from_vhost(cls, vhost):
        """retrieve paas instance id associated to a vhost"""

        result = Vhost().list()
        paas_hosts = {}
        for host in result:
            paas_hosts[host['name']] = host['paas_id']

        return paas_hosts.get(vhost)
