""" Docker namespace commands. """

import os

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.params import pass_gandi


@cli.command(root=True)
@click.option('--vm', help='Use given VM for docker connection')
@click.argument('args', nargs=-1)
@pass_gandi
def docker(gandi, vm, args):
    """
    Manage docker instance
    """
    if not [basedir for basedir in os.getenv('PATH', '.:/usr/bin').split(':')
            if os.path.exists('%s/docker' % basedir)]:
        gandi.echo("""'docker' not found in $PATH, required for this command \
to work
See https://docs.docker.com/installation/#installation to install, or use:
    # curl https://get.docker.io/ | sh""")
        return

    if vm:
        gandi.configure(True, 'dockervm', vm)
    else:
        vm = gandi.get('dockervm')

    if not vm:
        gandi.echo("""
No docker vm specified. You can create one:
    $ gandi vm create --hostname docker --image "Ubuntu 14.04 64 bits LTS (HVM)" \\
        --run 'wget -O - https://get.docker.io/ | sh'

Then configure it using:
    $ gandi docker --vm docker ps

Or to both change target vm and spawn a process (note the -- separator):
    $ gandi docker --vm myvm -- run -i -t debian bash
""")  # noqa
        return

    return gandi.docker.handle(vm, args)
