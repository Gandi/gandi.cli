""" Operation namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi

@cli.command(root=True)
@click.option('--vm', help='use given VM for docker connection')
@click.argument('args', nargs=-1)
@pass_gandi
def docker(gandi, vm, args):
    """Manage docker instance"""
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
