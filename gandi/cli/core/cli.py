# -*- coding: utf-8 -*-
import os
import os.path
import inspect

import click

from .conf import GandiContextHelper


class GandiCLI(click.Group):
    """ Gandi command line utility.

    All CLI commands have a documented help

    >>> gandi <command> --help

    """

    def __init__(self, help=None):

        def set_debug(ctx, value):
            ctx.obj['verbose'] = value

        if help is None:
            help = inspect.getdoc(self)

        click.Group.__init__(self, help=help, params=[
            click.Option(['-v'],
                         help='Enable or disable verbose mode.',
                         count=True,
                         default=False, callback=set_debug)
        ])

    def load_commands(self):
        """ Load cli commands from submodules """
        command_folder = os.path.join(os.path.dirname(__file__),
                                      '..', 'commands')
        for filename in sorted(os.listdir(command_folder)):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = 'gandi.cli.commands.' + submod
                __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        ctx.obj = GandiContextHelper(verbose=ctx.obj['verbose'])
        click.Group.invoke(self, ctx)


cli = GandiCLI()
cli.load_commands()
