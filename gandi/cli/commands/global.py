""" Main namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi


@cli.command(options_metavar='')
@pass_gandi
def setup(gandi):
    """ Initialize Gandi CLI configuration.

    Create global configuration directory with API credentials
    """
    intro = """Welcome to GandiCLI, let's configure a few things before we \
start.
"""

    outro = """
Setup completed. You can now:
* use 'gandi' to see all command.
* use 'gandi vm create' to create and access a Virtual Machine.
* use 'gandi paas create' to create and access a SimpleHosting instance.
"""
    gandi.echo(intro)
    gandi.init_config()
    gandi.echo(outro)


@cli.command()
@click.option('-g', help='Edit global configuration (default=local).',
              is_flag=True, default=False)
@click.argument('key')
@click.argument('value')
@pass_gandi
def config(gandi, g, key, value):
    """Configure default values."""
    gandi.configure(global_=g, key=key, val=value)


@cli.command(options_metavar='')
@pass_gandi
def api(gandi):
    """Display information about API used."""
    output_keys = ['api_version']

    result = gandi.api.info()
    output_generic(gandi, result, output_keys)

    return result


@cli.command()
@click.argument('command', required=False, nargs=-1)
@click.pass_context
def help(ctx, command):
    """Display help for a command."""
    command = ' '.join(command)
    if not command:
        click.echo(cli.get_help(ctx))
        return

    cmd = cli.get_command(ctx, command)
    if cmd:
        click.echo(cmd.get_help(ctx))
    else:
        click.echo(cli.get_help(ctx))
