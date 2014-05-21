#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path

import click

from .conf import GandiContextHelper, pass_gandi


class GandiCLI(click.Group):
    """ Gandi command line utility."""

    def __init__(self, help=None):

        def set_debug(ctx, value):
            ctx.obj['verbose'] = value

        click.Group.__init__(self, help=help, params=[
            click.Option(['-v', '--verbose'],
                         help='Enable or disable verbose mode.',
                         is_flag=True,
                         default=False, callback=set_debug)
        ])

    def load_commands(self):
        command_folder = os.path.join(os.path.dirname(__file__), 'commands')
        for filename in os.listdir(command_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = __package__ + '.commands.' + submod
                __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        ctx.obj = GandiContextHelper(verbose=ctx.obj['verbose'])
        click.Group.invoke(self, ctx)


cli = GandiCLI()
cli.load_commands()


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
