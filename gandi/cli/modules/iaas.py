
import time

from gandi.cli.core.conf import GandiModule
from gandi.cli.modules.datacenter import Datacenter


class Iaas(GandiModule):
    _op_scores = {'BILL': 0, 'WAIT': 1, 'RUN': 2, 'DONE': 3}

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
    def update(cls, id, memory, cores, console, interactive):
        """update a virtual machine"""

        if interactive and not cls.intty():
            interactive = False

        vm_params = {}

        if memory is not None:
            vm_params['memory'] = memory

        if cores is not None:
            vm_params['cores'] = cores

        if console is not None:
            vm_params['console'] = console

        result = cls.call('vm.update', cls.usable_id(id), vm_params)
        if not interactive:
            return result

        # interactive mode, run a progress bar
        from datetime import datetime
        start_crea = datetime.utcnow()

        cls.echo("We're updating your Virtual Machine.")
        # count number of operations, 3 steps per operation
        if not isinstance(result, list):
            result = [result]
        count_operations = len(result) * 3
        updating_done = False
        while not updating_done:
            op_score = 0
            for oper in result:
                op_step = cls.call('operation.info', oper['id'])['step']
                if op_step in cls._op_scores:
                    op_score += cls._op_scores[op_step]
                else:
                    msg = 'step %s unknown, exiting creation' % op_step
                    cls.error(msg)

            cls.update_progress(float(op_score) / count_operations,
                                start_crea)

            if op_score == count_operations:
                updating_done = True

            time.sleep(.5)

        cls.echo('')

    @classmethod
    def create(cls, datacenter, memory, cores, ip_version, bandwidth,
               login, password, hostname, image, run, interactive,
               ssh_key):
        """create a new virtual machine.

        you can specify a configuration entry named 'ssh_key' containing
        path to your ssh_key file

        >>> gandi config ssh_key ~/.ssh/id_rsa.pub

        to know which disk image label (or id) to use as image

        >>> gandi images

        to know which datacenter name|iso|country|id to use as datacenter

        >>> gandi datacenters

        """

        if interactive and not cls.intty():
            interactive = False

        # priority to command line parameters
        # then env var
        # then local configuration
        # then global configuration
        memory_ = memory or int(cls.get('iaas.memory'))
        cores_ = cores or int(cls.get('iaas.cores'))
        ip_version_ = ip_version or int(cls.get('iaas.ip_version'))
        bandwidth_ = bandwidth or int(cls.get('iaas.bandwidth'))
        login_ = login or cls.get('iaas.login')
        password_ = password or cls.get('iaas.password')
        hostname_ = hostname or cls.get('iaas.hostname')

        if datacenter:
            datacenter_id_ = int(Datacenter.usable_id(datacenter))
        else:
            datacenter_id_ = int(Datacenter.usable_id(cls.get('iaas.datacenter')))

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

        run_ = run or cls.get('iaas.run', mandatory=False)
        if run_ is not None:
            vm_params['run'] = run_

        ssh_key_ = ssh_key or cls.get('ssh_key', mandatory=False)
        if ssh_key_ is not None:
            with open(ssh_key_) as fdesc:
                ssh_key_ = fdesc.read()
            if ssh_key_ is not None:
                vm_params['ssh_key'] = ssh_key_

        # XXX: name of disk is limited to 15 chars in ext2fs, ext3fs
        # but api allow 255, so we limit to 15 for now
        disk_params = {'datacenter_id': vm_params['datacenter_id'],
                       'name': ('sys_%s' % hostname_)[:15]}

        if image:
            sys_disk_id_ = int(Image.usable_id(image))
        else:
            sys_disk_id_ = int(Image.usable_id(cls.get('iaas.image')))

        result = cls.call('vm.create_from', vm_params, disk_params,
                          sys_disk_id_)
        if not interactive:
            return result

        # interactive mode, run a progress bar
        from datetime import datetime
        start_crea = datetime.utcnow()

        cls.echo("We're creating your first Virtual Machine with default settings.")
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

        cls.echo('')
        vm_info = cls.call('vm.info', vm_id)
        for iface in vm_info['ifaces']:
            for ip in iface['ips']:
                if ip['version'] == 4:
                    access = 'ssh %s@%s' % (login_, ip['ip'])
                    ip_addr = ip['ip']
                else:
                    access = 'ssh -6 %s@%s' % (login_, ip['ip'])
                    ip_addr = ip['ip']
                # stop on first access found
                break

        cls.echo('Your VM %s have been created.' % hostname_)
        cls.echo('Requesting access using: %s ...' % access)
        # XXX: we must remove ssh key entry in case we use the same ip
        # as it's recyclable
        cls.shell('ssh-keygen -R "%s"' % ip_addr)
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

    @classmethod
    def console(cls, id):
        """open a console to virtual machine"""

        vm_info = cls.info(id)
        if not vm_info['console']:
            # first activate console
            cls.update(id, memory=None, cores=None, console=True,
                       interactive=True)
        # now we can connect
        # retrieve ip of vm
        vm_info = cls.info(id)
        for iface in vm_info['ifaces']:
            for ip in iface['ips']:
                if ip['version'] == 4:
                    ip_addr = ip['ip']
                else:
                    ip_addr = ip['ip']
                # stop on first access found
                break

        # hack for dev
        # console_url = 'console1-d.dev.gandi.net'
        console_url = 'console.gandi.net'
        access = 'ssh %s@%s' % (ip_addr, console_url)
        cls.shell(access)


class Image(GandiModule):

    @classmethod
    def list(cls, datacenter_id=None):
        """list available images for vm creation"""

        options = {}
        if datacenter_id:
            options = {'datacenter_id': datacenter_id}

        return cls.call('hosting.image.list', options)

    @classmethod
    def from_label(cls, label):
        """retrieve disk image id associated to a label"""

        result = cls.list()
        image_labels = {}
        for image in result:
            image_labels[image['label']] = image['disk_id']

        return image_labels.get(label)

    @classmethod
    def usable_id(cls, id):
        try:
            qry_id = int(id)
        except:
            # id is maybe a label
            qry_id = cls.from_label(id)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
