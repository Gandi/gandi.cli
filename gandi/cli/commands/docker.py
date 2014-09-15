""" Docker namespace commands. """

import os

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi

@cli.command(root=True)
@click.option('--vm', help='Use given VM for docker connection')
@click.argument('args', nargs=-1)
@pass_gandi
def docker(gandi, vm, args):
    """Manage docker instance"""
    for basedir in os.getenv('PATH', '.:/usr/bin').split(':'):
        if os.path.exists('%s/docker' % basedir):
            break
    else:
        print """'docker' not found in $PATH, required for this command to work
See https://docs.docker.com/installation/#installation to install, or use:
    # curl https://get.docker.io/ | sh"""
        return
        
    if vm:
        gandi.configure(True, 'dockervm', vm)
    else:
        vm = gandi.get('dockervm')

    if not vm:
        print """
No docker vm specified. You can create one:
    $ gandi vm create --hostname docker --image "Ubuntu 14.04 64 bits LTS" \\
        --run 'wget -O - https://get.docker.io/ | sh'

Then configure it using:
    $ gandi docker --vm docker ps
"""
        return

    return gandi.docker.handle(vm, args)
