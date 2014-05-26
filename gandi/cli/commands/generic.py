
import click

from gandi.cli.core.cli import cli
from gandi.cli.core.conf import pass_gandi


@cli.command()
@pass_gandi
def setup(gandi):
    """ Initialize Gandi CLI configuration.

    Create global configuration directory with API credentials
    """
    gandi.echo("Welcome to GandiCLI, let's configure a few things "
               "before we start")
    gandi.init_config()


@cli.command()
@click.option('-g', help='edit global configuration (default=local)',
              is_flag=True, default=False)
@click.argument('key')
@click.argument('value')
@pass_gandi
def config(gandi, g, key, value):
    """Configure default values"""
    gandi.configure(global_=g, key=key, val=value)
