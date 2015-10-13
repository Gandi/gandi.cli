""" Configuration namespace commands. """

import sys
import os
import subprocess

import click
from click.exceptions import Abort

from gandi.cli.core.cli import cli
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('-g', help='Get from global configuration only '
                         '(default=env -> local -> global).',
              is_flag=True, default=False)
@click.argument('key')
@pass_gandi
def get(gandi, g, key):
    """Display value of a given config key."""
    val = gandi.get(key=key, global_=g)
    if not val:
        gandi.echo("No value found.")
        sys.exit(1)
    gandi.echo(val)


@cli.command()
@click.option('-g', help='Edit global configuration (default=local).',
              is_flag=True, default=False)
@click.argument('key')
@click.argument('value')
@pass_gandi
def set(gandi, g, key, value):
    """Update or create config key/value."""
    gandi.configure(global_=g, key=key, val=value)


@cli.command()
@click.option('-g', help='Edit global configuration (default=local).',
              is_flag=True, default=False)
@pass_gandi
def edit(gandi, g):
    """Edit config file with prefered text editor"""
    config_file = gandi.home_config if g else gandi.local_config
    path = os.path.expanduser(config_file)
    editor = gandi.get('editor')
    if not editor:
        try:
            editor = click.prompt("Please enter the path of your prefered "
                                  "editor. eg: '/usr/bin/vi' or 'vi'")
        except Abort:
            gandi.echo("""
Warning: editor is not configured.
You can use both 'gandi config set [-g] editor <value>'
or the $EDITOR environment variable to configure it.""")
            sys.exit(1)

    subprocess.call([editor, path])


@cli.command()
@click.option('-g', help='Delete on global configuration (default=local).',
              is_flag=True, default=False)
@click.argument('key')
@pass_gandi
def delete(gandi, g, key):
    """Delete a key/value pair from configuration"""
    gandi.delete(global_=g, key=key)


@cli.command()
@click.option('-g', help='Display global configuration (default=local).',
              is_flag=True, default=False)
@pass_gandi
def list(gandi, g):
    """Display config file content"""
    gandi.pretty_echo(gandi.list(global_=g))
