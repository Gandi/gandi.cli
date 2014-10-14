""" VM commands module. """

import math
import time

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import randomstring
from gandi.cli.modules.datacenter import Datacenter
from gandi.cli.modules.sshkey import SshkeyHelper


class Iaas(GandiModule, SshkeyHelper):

    """ Module to handle CLI commands.

    $ gandi vm console
    $ gandi vm create
    $ gandi vm delete
    $ gandi vm info
    $ gandi vm list
    $ gandi vm reboot
    $ gandi vm ssh
    $ gandi vm start
    $ gandi vm stop
    $ gandi vm update

    """

    @classmethod
    def list(cls, options=None):
        """List virtual machines."""
        if not options:
            options = {}

        return cls.call('hosting.vm.list', options)

    @classmethod
    def resource_list(cls):
        """ Get the possible list of resources (hostname, id). """
        items = cls.list()
        ret = [vm['hostname'] for vm in items]
        ret.extend([str(vm['id']) for vm in items])
        return ret

    @classmethod
    def info(cls, id):
        """Display information about a virtual machine."""
        return cls.call('hosting.vm.info', cls.usable_id(id))

    @classmethod
    def stop(cls, resources, background=False):
        """Stop a virtual machine."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.vm.stop', cls.usable_id(item))
            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Stopping your Virtual Machine %s.' % item)
        cls.display_progress(opers)

    @classmethod
    def start(cls, resources, background=False):
        """Start a virtual machine."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.vm.start', cls.usable_id(item))
            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Starting your Virtual Machine %s.' % item)
        cls.display_progress(opers)

    @classmethod
    def reboot(cls, resources, background=False):
        """Reboot a virtual machine."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.vm.reboot', cls.usable_id(item))
            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Rebooting your Virtual Machine %s.' % item)
        cls.display_progress(opers)

    @classmethod
    def delete(cls, resources, background=False):
        """Delete a virtual machine."""
        if not isinstance(resources, (list, tuple)):
            resources = [resources]

        opers = []
        for item in resources:
            oper = cls.call('hosting.vm.delete', cls.usable_id(item))
            if not oper:
                continue

            if isinstance(oper, list):
                opers.extend(oper)
            else:
                opers.append(oper)

        if background:
            return opers

        # interactive mode, run a progress bar
        cls.echo('Deleting your Virtual Machine %s.' % item)
        if opers:
            cls.display_progress(opers)

    @classmethod
    def required_max_memory(cls, id, memory):
        """
        Recommend a max_memory setting for this vm given memory. If the
        VM already has a nice setting, return None. The max_memory
        param cannot be fixed too high, because page table allocation
        would cost too much for small memory profile. Use a range as below.
        """
        best = int(max(2 ** math.ceil(math.log(memory, 2)), 2048))

        actual_vm = cls.info(id)

        if (actual_vm['state'] == 'running'
                and actual_vm['vm_max_memory'] != best):
            return best

    @classmethod
    def update(cls, id, memory, cores, console, password, background,
               max_memory):
        """Update a virtual machine."""
        if not background and not cls.intty():
            background = True

        vm_params = {}

        if memory:
            vm_params['memory'] = memory

        if cores:
            vm_params['cores'] = cores

        if console:
            vm_params['console'] = console

        if password:
            vm_params['password'] = password

        if max_memory:
            vm_params['vm_max_memory'] = max_memory

        result = cls.call('hosting.vm.update', cls.usable_id(id), vm_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Updating your Virtual Machine %s.' % id)
        cls.display_progress(result)

    @classmethod
    def create(cls, datacenter, memory, cores, ip_version, bandwidth,
               login, password, hostname, image, run, background, sshkey,
               size):
        """Create a new virtual machine."""
        if not background and not cls.intty():
            background = True

        datacenter_id_ = int(Datacenter.usable_id(datacenter))

        if not hostname:
            hostname = randomstring()
            disk_name = 'sys_%s' % hostname[4:]
        else:
            disk_name = 'sys_%s' % hostname.replace('.', '')

        vm_params = {
            'hostname': hostname,
            'datacenter_id': datacenter_id_,
            'memory': memory,
            'cores': cores,
            'ip_version': ip_version,
            'bandwidth': bandwidth,
        }

        if login:
            vm_params['login'] = login

        if run:
            vm_params['run'] = run

        if password:
            vm_params['password'] = password

        vm_params.update(cls.convert_sshkey(sshkey))

        # XXX: name of disk is limited to 15 chars in ext2fs, ext3fs
        # but api allow 255, so we limit to 15 for now
        disk_params = {'datacenter_id': vm_params['datacenter_id'],
                       'name': disk_name[:15]}

        if size:
            disk_params['size'] = size

        sys_disk_id_ = int(Image.usable_id(image, datacenter_id_))

        result = cls.call('hosting.vm.create_from', vm_params, disk_params,
                          sys_disk_id_)

        if ip_version == 4:
            ip_summary = 'ip v4+v6'
        else:
            ip_summary = 'ip v6'
        cls.echo('* Configuration used: %d cores, %dMb memory, %s, '
                 'image %s, hostname: %s' % (cores, memory, ip_summary, image,
                                             hostname))
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo('Creating your Virtual Machine %s.' % hostname)
        cls.display_progress(result)
        cls.echo('Your Virtual Machine %s has been created.' % hostname)

        if 'ssh_key' not in vm_params and 'keys' not in vm_params:
            return

        vm_id = None
        for oper in result:
            if oper.get('vm_id'):
                vm_id = oper.get('vm_id')
                break

        if vm_id:
            time.sleep(5)
            cls.ssh(oper['vm_id'], login='root', identity=None, wipe_key=True)

    @classmethod
    def from_hostname(cls, hostname):
        """Retrieve virtual machine id associated to a hostname."""
        result = cls.list()
        vm_hosts = {}
        for host in result:
            vm_hosts[host['hostname']] = host['id']

        return vm_hosts.get(hostname)

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from input which can be hostname or id."""
        try:
            # id is maybe a hostname
            qry_id = cls.from_hostname(id)
            if not qry_id:
                qry_id = int(id)
        except Exception:
            qry_id = None

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id

    @classmethod
    def ssh(cls, vm_id, login, identity, wipe_key=False):
        """Spawn an ssh session to virtual machine."""
        vm_info = cls.info(vm_id)

        cmd = ['ssh']
        if identity:
            cmd.extend(('-i', identity,))

        for iface in vm_info['ifaces']:
            for ip in iface['ips']:
                ip_addr = ip['ip']
                if ip['version'] == 6:
                    cmd.append('-6')
                # stop on first access found
                break

        cmd.append('%s@%s' % (login, ip_addr,))

        cls.echo('Requesting access using: %s ...' % ' '.join(cmd))
        # XXX: we must remove ssh key entry in case we use the same ip
        # as it's recyclable
        if wipe_key:
            cls.execute('ssh-keygen -R "%s"' % ip_addr)

        cls.execute(cmd, False)

    @classmethod
    def console(cls, id):
        """Open a console to virtual machine."""
        vm_info = cls.info(id)
        if not vm_info['console']:
            # first activate console
            cls.update(id, memory=None, cores=None, console=True,
                       password=None, background=False)
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

        console_url = vm_info.get('console_url', 'console.gandi.net')
        access = 'ssh %s@%s' % (ip_addr, console_url)
        cls.execute(access)


class Image(GandiModule):

    """ Module to handle CLI commands.

    $ gandi vm images

    """

    @classmethod
    def list(cls, datacenter=None, label=None):
        """List available images for vm creation."""
        options = {}
        if datacenter:
            datacenter_id = int(Datacenter.usable_id(datacenter))
            options['datacenter_id'] = datacenter_id

        # implement a filter by label as API doesn't handle it
        images = cls.safe_call('hosting.image.list', options)
        if not label:
            return images
        return [img for img in images
                if label.lower() in img['label'].lower()]

    @classmethod
    def from_label(cls, label, datacenter=None):
        """Retrieve disk image id associated to a label."""
        result = cls.list(datacenter=datacenter)
        image_labels = dict([(image['label'], image['disk_id'])
                            for image in result])

        return image_labels.get(label)

    @classmethod
    def from_sysdisk(cls, label):
        """Retrieve disk id from available system disks"""
        disks = cls.safe_call('hosting.disk.list', {'name': label})
        if len(disks):
            return disks[0]['id']

    @classmethod
    def usable_id(cls, id, datacenter=None):
        """ Retrieve id from input which can be label or id."""
        try:
            qry_id = int(id)
        except:
            # if id is a string, prefer a system disk then a label
            qry_id = cls.from_sysdisk(id) or cls.from_label(id, datacenter)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id


class Kernel(GandiModule):

    """ Module to handle Gandi Kernels. """

    @classmethod
    def list(cls, datacenter, flavor=None, match=''):
        """ List available kernels for datacenter."""
        dc_id = Datacenter.usable_id(datacenter)
        kmap = cls.safe_call('hosting.disk.list_kernels', dc_id)

        if match:
            for flav in kmap:
                kmap[flav] = [x for x in kmap[flav] if match in x]

        if flavor:
            if flavor not in kmap:
                cls.error('flavor %s not supported here' % flavor)
            return kmap[flavor]

        return kmap
