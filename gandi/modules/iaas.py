
import time

from gandi.conf import GandiModule


class Iaas(GandiModule):

    def list(self, options=None):
        """list virtual machines"""

        if not options:
            options = {}

        return self.call('vm.list', options)

    def info(self, id):
        """display information about a virtual machine"""

        return self.call('vm.info', self.usable_id(id))

    def stop(self, id):
        """stop a virtual machine"""

        return self.call('vm.stop', self.usable_id(id))

    def start(self, id):
        """start a virtual machine"""

        return self.call('vm.start', self.usable_id(id))

    def reboot(self, id):
        """reboot a virtual machine"""

        return self.call('vm.reboot', self.usable_id(id))

    def delete(self, id):
        """delete a virtual machine"""

        return self.call('vm.delete', self.usable_id(id))

    def create(self, datacenter_id, memory, cores, ip_version, bandwidth,
               login, password, run, interactive, ssh_key):
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
            datacenter_id_ = int(self.get('datacenter_id'))

        if memory:
            memory_ = memory
        else:
            memory_ = int(self.get('memory'))

        if cores:
            cores_ = cores
        else:
            cores_ = int(self.get('cores'))

        if ip_version:
            ip_version_ = ip_version
        else:
            ip_version_ = int(self.get('ip_version'))

        if bandwidth:
            bandwidth_ = bandwidth
        else:
            bandwidth_ = int(self.get('bandwidth'))

        if login:
            login_ = login
        else:
            login_ = self.get('login')

        if password:
            password_ = password
        else:
            password_ = self.get('password')

        vm_params = {
            'hostname': 'tempo',
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
            run_ = self.get('run')
        if run_ is not None:
            vm_params['run'] = run_

        if ssh_key:
            ssh_key_ = ssh_key
        else:
            ssh_key_ = self.get('ssh_key')
        if ssh_key_ is not None:
            vm_params['ssh_key'] = ssh_key_

        disk_params = {'datacenter_id': int(self.get('datacenter_id')),
                       'name': 'sysdisktempo'}
        sys_disk_id = int(self.get('sys_disk_id'))

        result = self.call('vm.create_from', vm_params, disk_params,
                           sys_disk_id)
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
                    op_step = self.call('operation.info', oper['id'])['step']
                    if op_step == 'WAIT':
                        op_score += 1
                    elif op_step == 'RUN':
                        op_score += 2
                    elif op_step == 'DONE':
                        op_score += 3
                    else:
                        msg = 'step %s unknown, exiting creation' % op_step
                        self.error(msg)

                    if 'vm_id' in oper and oper['vm_id'] is not None:
                        vm_id = oper['vm_id']

                self.update_progress(float(op_score) / count_operations,
                                     start_crea)

                if op_score == count_operations:
                    crea_done = True

                time.sleep(.5)

            print
            vm_info = self.call('vm.info', vm_id)
            for iface in vm_info['ifaces']:
                for ip in iface['ips']:
                    if ip['version'] == 4:
                        access = 'ssh %s@%s' % (login_, ip['ip'])
                    else:
                        access = 'ssh -6 %s@%s' % (login_, ip['ip'])
                    # stop on first access found
                    break

            print 'Your VM have been created, requesting access using: %s' % access
            time.sleep(5)
            self.shell(access)

    def from_hostname(self, hostname):
        """retrieve virtual machine id associated to a hostname"""

        result = self.list()
        vm_hosts = {}
        for host in result:
            vm_hosts[host['hostname']] = host['id']

        return vm_hosts.get(hostname)

    def usable_id(self, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a hostname
            qry_id = self.from_hostname(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            self.error(msg)

        return qry_id
