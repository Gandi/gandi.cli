import subprocess

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.iaas import Iaas
from gandi.cli.core.utils import unixpipe


class Docker(GandiModule):
    """ Module to handle docker vms.

    $ gandi docker create
    $ gandi docker help
    $ gandi docker ps
    $ gandi docker <docker_cmd>

    Note that you can use a per-project docker vm by using
    a local directory gandi configuration using:

    $ gandi config dockervm foobar

    Or override the current global vm using:

    $ gandi docker --vm bar ps
    """

    @classmethod
    def handle(cls, vm, args):
        """Setup forwarding connection to the given VM and pipe docker cmds over SSH."""
        docker = Iaas.info(vm)
        if not docker:
            raise Exception('docker vm %s not found' % vm)

        if docker['state'] != 'running':
            Iaas.start(vm)

        # XXX
        remote_addr = None
        for iface in docker['ifaces']:
            for ip in iface['ips']:
                if ip['version'] == 4:
                    remote_addr = ip['ip']

        unixpipe.setup(remote_addr, 'root', '/var/run/docker.sock')
        subprocess.call(['docker', '-H',
            'tcp://localhost:%d' % unixpipe.service_port] + list(args))
