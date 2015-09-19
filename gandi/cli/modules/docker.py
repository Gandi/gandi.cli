import os
import subprocess

from gandi.cli.core.base import GandiModule
from gandi.cli.modules.iaas import Iaas
from gandi.cli.core.utils import unixpipe


class Docker(GandiModule):
    """
    Module to handle docker vms.

    $ gandi docker create
    $ gandi docker help
    $ gandi docker ps
    $ gandi docker <docker_cmd>

    Note that you can use a per-project docker vm by using
    a local directory gandi configuration using:

    $ gandi config set dockervm foobar

    Or override the current global vm using:

    $ gandi docker --vm bar ps
    """

    @classmethod
    def handle(cls, vm, args):
        """
        Setup forwarding connection to given VM and pipe docker cmds over SSH.
        """
        docker = Iaas.info(vm)
        if not docker:
            raise Exception('docker vm %s not found' % vm)

        if docker['state'] != 'running':
            Iaas.start(vm)

        # XXX
        remote_addr = docker['ifaces'][0]['ips'][0]['ip']

        port = unixpipe.setup(remote_addr, 'root', '/var/run/docker.sock')

        os.environ['DOCKER_HOST'] = 'tcp://localhost:%d' % port
        cls.echo('using DOCKER_HOST=%s' % os.environ['DOCKER_HOST'])

        subprocess.call(['docker'] + list(args))
