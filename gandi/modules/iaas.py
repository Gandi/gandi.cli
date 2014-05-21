
import time

from gandi.conf import GandiModule


class Iaas(GandiModule):
    _op_scores = {'WAIT': 1, 'RUN': 2, 'DONE': 3}

    @classmethod
    def list(cls, options=None):
        """list virtual machines"""

        if not options:
            options = {}

        return cls.call('vm.list', options)

    @classmethod
    def info(cls, id):
        """display information about a virtual machine"""

        return cls.call('vm.info', cls.usable_id(id))

    @classmethod
    def stop(cls, id):
        """stop a virtual machine"""

        return cls.call('vm.stop', cls.usable_id(id))

    @classmethod
    def start(cls, id):
        """start a virtual machine"""

        return cls.call('vm.start', cls.usable_id(id))

    @classmethod
    def reboot(cls, id):
        """reboot a virtual machine"""

        return cls.call('vm.reboot', cls.usable_id(id))

    @classmethod
    def delete(cls, id):
        """delete a virtual machine"""

        return cls.call('vm.delete', cls.usable_id(id))

    @classmethod
    def create(cls, datacenter_id, memory, cores, ip_version, bandwidth,
               login, password, hostname, sys_disk_id, run, interactive,
               ssh_key):
        """create a new virtual machine.

        you can provide a ssh_key on command line calling this command as:

        >>> cat ~/.ssh/id_rsa.pub | gandi vm -

        """

        # priority to command line parameters
        # then env var
        # then local configuration
        # then global configuration
        if datacenter_id:
            datacenter_id_ = datacenter_id
        else:
            datacenter_id_ = int(cls.get('datacenter_id'))

        if memory:
            memory_ = memory
        else:
            memory_ = int(cls.get('memory'))

        if cores:
            cores_ = cores
        else:
            cores_ = int(cls.get('cores'))

        if ip_version:
            ip_version_ = ip_version
        else:
            ip_version_ = int(cls.get('ip_version'))

        if bandwidth:
            bandwidth_ = bandwidth
        else:
            bandwidth_ = int(cls.get('bandwidth'))

        if login:
            login_ = login
        else:
            login_ = cls.get('login')

        if password:
            password_ = password
        else:
            password_ = cls.get('password')

        if hostname:
            hostname_ = hostname
        else:
            hostname_ = cls.get('hostname')

        vm_params = {
            'hostname': hostname_,
            'datacenter_id': datacenter_id_,
            'memory': memory_,
            'cores': cores_,
            'ip_version': ip_version_,
            'bandwidth': bandwidth_,
            'login': login_,
            'password': password_,
        }
        if run:
            run_ = run
        else:
            run_ = cls.get('run')
        if run_ is not None:
            vm_params['run'] = run_

        if ssh_key:
            ssh_key_ = ssh_key
        else:
            ssh_key_ = cls.get('ssh_key')
        if ssh_key_ is not None:
            vm_params['ssh_key'] = ssh_key_
        else:
            ssh_key_path = cls.get('ssh_key_path')
            if ssh_key_path:
                with open(ssh_key_path) as fdesc:
                    ssh_key_ = fdesc.read()
                if ssh_key_ is not None:
                    vm_params['ssh_key'] = ssh_key_

        # XXX: name of disk is limited to 15 chars in ext2fs, ext3fs
        # but api allow 255, so we limit to 15 for now
        disk_params = {'datacenter_id': int(cls.get('datacenter_id')),
                       'name': ('sys_%s' % hostname_)[:15]}

        if sys_disk_id:
            sys_disk_id_ = int(sys_disk_id)
        else:
            sys_disk_id_ = int(cls.get('sys_disk_id'))

        result = cls.call('vm.create_from', vm_params, disk_params,
                          sys_disk_id_)
        if not interactive:
            return result
        else:
            # interactive mode, run a progress bar
            from datetime import datetime
            start_crea = datetime.utcnow()

            print "We're creating your first Virtual Machine with default settings."
            # count number of operations, 3 steps per operation
            count_operations = len(result) * 3
            crea_done = False
            vm_id = None
            while not crea_done:
                op_score = 0
                for oper in result:
                    op_step = cls.call('operation.info', oper['id'])['step']
                    if op_step in cls._op_scores:
                        op_score += cls._op_scores[op_step]
                    else:
                        msg = 'step %s unknown, exiting creation' % op_step
                        cls.error(msg)

                    if 'vm_id' in oper and oper['vm_id'] is not None:
                        vm_id = oper['vm_id']

                cls.update_progress(float(op_score) / count_operations,
                                    start_crea)

                if op_score == count_operations:
                    crea_done = True

                time.sleep(.5)

            print
            vm_info = cls.call('vm.info', vm_id)
            for iface in vm_info['ifaces']:
                for ip in iface['ips']:
                    if ip['version'] == 4:
                        access = 'ssh %s@%s' % (login_, ip['ip'])
                    else:
                        access = 'ssh -6 %s@%s' % (login_, ip['ip'])
                    # stop on first access found
                    break

            print 'Your VM %s have been created.' % hostname_
            print 'Requesting access using: %s ...' % access
            # XXX: we must remove ssh key entry in case we use the same ip
            # as it's recyclable
            cls.shell('ssh-keygen -R -H "%s"' % hostname_)
            time.sleep(5)
            cls.shell(access)

    @classmethod
    def from_hostname(cls, hostname):
        """retrieve virtual machine id associated to a hostname"""

        result = cls.list()
        vm_hosts = {}
        for host in result:
            vm_hosts[host['hostname']] = host['id']

        return vm_hosts.get(hostname)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a hostname
            qry_id = cls.from_hostname(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id


class Image(GandiModule):

    @classmethod
    def list(cls, datacenter_id=None):
        """list available images for vm creation"""

        options = {}
        if datacenter_id:
            options = {'datacenter_id': datacenter_id}

        return cls.call('hosting.image.list', options)
