#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path

import click

from .conf import GandiContextHelper, pass_gandi


class GandiCLI(click.Group):
    """ Gandi command line utility."""

    def load_plugins(self):
        plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = __package__ + '.commands.' + submod
                __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        ctx.obj = GandiContextHelper()
        click.Group.invoke(self, ctx)


cli = GandiCLI()
cli.load_plugins()


@cli.command()
@click.option('-g', help='edit global configuration (default=local)',
              is_flag=True, default=False)
@click.argument('key')
@click.argument('value')
@pass_gandi
def config(gandi, g, key, value):
    """Configure default values"""
    gandi.configure(global_=g, key=key, val=value)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()

