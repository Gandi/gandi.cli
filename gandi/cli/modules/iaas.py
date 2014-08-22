import os
import time

from gandi.cli.core.base import GandiModule
from gandi.cli.core.utils import randomstring
from gandi.cli.modules.datacenter import Datacenter
from gandi.cli.modules.paas import Paas


class Iaas(GandiModule):

    @classmethod
    def list(cls, options=None):
        """list virtual machines"""

        if not options:
            options = {}

        return cls.call('hosting.vm.list', options)

    @classmethod
    def info(cls, id):
        """display information about a virtual machine"""

        return cls.call('hosting.vm.info', cls.usable_id(id))

    @classmethod
    def stop(cls, resources, background=False):
        """stop a virtual machine"""

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
        cls.echo("Stop your Virtual Machine.")
        cls.display_progress(opers)

    @classmethod
    def start(cls, resources, background=False):
        """start a virtual machine"""

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
        cls.echo("Start your Virtual Machine.")
        cls.display_progress(opers)

    @classmethod
    def reboot(cls, resources, background=False):
        """reboot a virtual machine"""

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
        cls.echo("Reboot your Virtual Machine.")
        cls.display_progress(opers)

    @classmethod
    def delete(cls, resources, background=False):
        """delete a virtual machine"""

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
        cls.echo("Deleting your Virtual Machine.")
        if opers:
            cls.display_progress(opers)

    @classmethod
    def update(cls, id, memory, cores, console, password, background):
        """update a virtual machine"""

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

        result = cls.call('hosting.vm.update', cls.usable_id(id), vm_params)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo("Updating your Virtual Machine.")
        cls.display_progress(result)

    @classmethod
    def create(cls, datacenter, memory, cores, ip_version, bandwidth,
               login, password, hostname, image, run, background, ssh_key):
        """create a new virtual machine.

        you can specify a configuration entry named 'ssh_key' containing
        path to your ssh_key file

        >>> gandi config -g ssh_key ~/.ssh/id_rsa.pub

        to know which disk image label (or id) to use as image

        >>> gandi images

        """

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
            'login': login,
        }

        if run:
            vm_params['run'] = run

        if password:
            vm_params['password'] = password

        vm_params.update(Paas.convert_ssh_key(ssh_key))

        # XXX: name of disk is limited to 15 chars in ext2fs, ext3fs
        # but api allow 255, so we limit to 15 for now
        disk_params = {'datacenter_id': vm_params['datacenter_id'],
                       'name': disk_name[:15]}

        sys_disk_id_ = int(Image.usable_id(image, datacenter_id_))

        result = cls.call('hosting.vm.create_from', vm_params, disk_params,
                          sys_disk_id_)
        if background:
            return result

        # interactive mode, run a progress bar
        cls.echo("Creating your Virtual Machine with default settings.")
        cls.display_progress(result)

        vm_id = None
        for oper in result:
            if oper.get('vm_id'):
                vm_id = oper.get('vm_id')
                break

        vm_info = cls.call('hosting.vm.info', vm_id)
        for iface in vm_info['ifaces']:
            for ip in iface['ips']:
                if ip['version'] == 4:
                    access = 'ssh %s@%s' % (login, ip['ip'])
                    ip_addr = ip['ip']
                else:
                    access = 'ssh -6 %s@%s' % (login, ip['ip'])
                    ip_addr = ip['ip']
                # stop on first access found
                break

        cls.echo('Your Virtual Machine %s have been created.' % hostname)
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
    def console(cls, id):
        """open a console to virtual machine"""

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
        cls.shell(access)


class Image(GandiModule):

    @classmethod
    def list(cls, datacenter=None, label=None):
        """list available images for vm creation"""

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
        """retrieve disk image id associated to a label"""

        result = cls.list(datacenter=datacenter)
        image_labels = dict([(image['label'], image['disk_id'])
                            for image in result])

        return image_labels.get(label)

    @classmethod
    def usable_id(cls, id, datacenter=None):
        try:
            qry_id = int(id)
        except:
            # id is maybe a label
            qry_id = cls.from_label(id, datacenter)

        if not qry_id:
            msg = 'unknown identifier %s' % id
            cls.error(msg)

        return qry_id
