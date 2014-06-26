# -*- coding: utf-8 -*-
import os
import os.path
import inspect

import click

from .base import GandiContextHelper
from gandi.cli import __version__


# XXX: dirty hack of click help command to allow short help -h
def add_help_option(self):
    """Adds a help option to the command."""
    click.help_option(*('--help', '-h'))(self)

click.Command.add_help_option = add_help_option


class GandiCLI(click.Group):
    """ Gandi command line utility.

    All CLI commands have a documented help

    >>> gandi <command> --help

    """

    def __init__(self, help=None):

        def set_debug(ctx, value):
            ctx.obj['verbose'] = value

        def get_version(ctx, value):
            if value:
                print ('Gandi CLI %s\n\n'
                       'Copyright: © 2014 Gandi S.A.S.\n'
                       'License: LGPL-3' % __version__)
                ctx.exit()

        if help is None:
            help = inspect.getdoc(self)

        click.Group.__init__(self, help=help, params=[
            click.Option(['-v'],
                         help='Enable or disable verbose mode.',
                         count=True, metavar='',
                         default=False, callback=set_debug),
            click.Option(['--version'],
                         help='Display version.',
                         is_flag=True,
                         default=False, callback=get_version)

        ])

    def get_command(self, ctx, cmd_name):
        sub_cmd = False
        if len(ctx.args) > 1:
            new_cmd_name = ' '.join(ctx.args[0:2])
            rv = click.Group.get_command(self, ctx, new_cmd_name)
            if rv is not None:
                sub_cmd = True
                cmd_name = new_cmd_name
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            if sub_cmd:
                del ctx.args[1]
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            if sub_cmd:
                del ctx.args[1]
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

    def command(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a command to
        the group.  This takes the same arguments as :func:`command` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        def decorator(f):
            namespace = f.__module__.rsplit('.', 1)[1]
            if namespace == 'global' or 'root' in kwargs:
                new_name = '%s' % f.__name__.lower()
                kwargs.pop('root', None)
            else:
                new_name = '%s %s' % (namespace, f.__name__.lower())
            kwargs['name'] = new_name
            cmd = click.command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd
        return decorator

    def load_commands(self):
        """ Load cli commands from submodules """
        command_folder = os.path.join(os.path.dirname(__file__),
                                      '..', 'commands')
        for filename in sorted(os.listdir(command_folder)):
            if filename.endswith('.py'):
                submod = filename[:-3]
                module_name = 'gandi.cli.commands.' + submod
                __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        ctx.obj = GandiContextHelper(verbose=ctx.obj['verbose'])

        if not ctx.args:
            if self.invoke_without_command:
                return click.Command.invoke(self, ctx)
            ctx.fail('Missing command.')

        cmd_name = click.utils.make_str(ctx.args[0])
        cmd = self.get_command(ctx, cmd_name)
        if cmd:
            cmd_name = cmd.name

        # If we don't find the command we want to show an error message
        # to the user that it was not provided.  However there is
        # something else we should do: if the first argument looks like
        # an option we want to kick off parsing again for arguments to
        # resolve things like --help which now should go to the main
        # place.
        if cmd is None:
            if click.parser.split_opt(cmd_name)[0]:
                self.parse_args(ctx, ctx.args)
            ctx.fail('No such command "%s".' % cmd_name)

        return self.invoke_subcommand(ctx, cmd, cmd_name, ctx.args[1:])


cli = GandiCLI()
cli.load_commands()
