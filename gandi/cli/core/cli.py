# -*- coding: utf-8 -*-
""" GandiCLI class declaration and initialization. """

import os
import os.path
import inspect
from functools import update_wrapper

import click

from .base import GandiContextHelper
from gandi.cli import __version__


# XXX: dirty hack of click help command to allow short help -h
def add_help_option(self):
    """Add a help option to the command."""
    click.help_option(*('--help', '-h'))(self)

click.Command.add_help_option = add_help_option


def compatcallback(f):
    """ Compatibility callback decorator for older click version.

    Click 1.0 does not have a version string stored, so we need to
    use getattr here to be safe.
    """
    if getattr(click, '__version__', '0.0') >= '2.0':
        return f
    return update_wrapper(lambda ctx, value: f(ctx, None, value), f)


class GandiCLI(click.Group):

    """ Gandi command line utility.

    All CLI commands have a documented help

    $ gandi <command> --help

    """

    def __init__(self, help=None):
        """ Initialize CLI command line."""
        @compatcallback
        def set_debug(ctx, param, value):
            ctx.obj['verbose'] = value

        @compatcallback
        def get_version(ctx, param, value):
            if value:
                print(('Gandi CLI %s\n\n'
                       'Copyright: © 2014-2017 Gandi S.A.S.\n'
                       'License: GPL-3' % __version__))
                ctx.exit()

        if help is None:
            help = inspect.getdoc(self)

        click.Group.__init__(self, help=help, params=[
            click.Option(['-v'],
                         help='Enable or disable verbose mode. Use multiple '
                              'time for higher level of verbosity: -v, -vv',
                         count=True, metavar='',
                         default=0, callback=set_debug),
            click.Option(['--version'],
                         help='Display version.',
                         is_flag=True,
                         default=False, callback=get_version)

        ])

    def resolve_command(self, ctx, args):
        cmd_name = args[0]

        sub_cmd = False
        if len(args) > 1:
            # XXX: dirty hack to handle namespaces by merging the first 2 args
            # i.e : paas + list = 'paas list'
            new_cmd_name = ' '.join(args[0:2])
            cmd = click.Group.get_command(self, ctx, new_cmd_name)
            if cmd is not None:
                sub_cmd = True
                cmd_name = new_cmd_name

        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd is not None:
            if sub_cmd:
                del args[1]
            return cmd_name, cmd, args[1:]

        formatter = ctx.make_formatter()

        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            self.format_commands(ctx, formatter)
            print(formatter.getvalue().rstrip('\n'))
            ctx.exit()

        elif len(matches) == 1:
            if sub_cmd:
                del args[1]
            cmd = click.Group.get_command(self, ctx, matches[0])
            return cmd_name, cmd, args[1:]

        rows = []
        for matched in sorted(matches):
            cmd = click.Group.get_command(self, ctx, matched)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue

            help = cmd.short_help or ''
            rows.append((matched, help))

        if rows:
            formatter.write_dl(rows)

        print(formatter.getvalue().rstrip('\n'))
        ctx.exit()

        if click.parser.split_opt(cmd_name)[0]:
            click.Group.parse_args(ctx, ctx.args)

    def get_command(self, ctx, cmd_name):
        """ Retrieve command from internal list.

        Handle custom namespace commands.
        Display custom help when no command was found in a namespace.
        """
        sub_cmd = False
        if len(ctx.args) > 1:
            # XXX: dirty hack to handle namespaces by merging the first 2 args
            # i.e : paas + list = 'paas list'
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

        formatter = ctx.make_formatter()
        rows = []
        for matched in sorted(matches):
            rv = click.Group.get_command(self, ctx, matched)
            # What is this, the tool lied about a command.  Ignore it
            if rv is None:
                continue

            help = rv.short_help or ''
            rows.append((matched, help))

        if rows:
            formatter.write_dl(rows)

        print(formatter.getvalue().rstrip('\n'))
        ctx.exit()

    def command(self, *args, **kwargs):
        """Decorator for declaring and attaching a command to the group.

        This takes the same arguments as :func:`command` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        def decorator(f):
            namespace = f.__module__.rsplit('.', 1)[1]
            name = args[0] if args else kwargs.get('name', f.__name__.lower())
            # XXX: hack for handling commands without namespaces (root)
            if namespace == 'root' or 'root' in kwargs:
                new_name = '%s' % name
                kwargs.pop('root', None)
            else:
                new_name = '%s %s' % (namespace, name)
            kwargs['name'] = new_name
            _args = args[1:] if args else args
            cmd = click.command(*_args, **kwargs)(f)
            self.add_command(cmd)
            return cmd
        return decorator

    def load_commands(self):
        """ Load cli commands from submodules. """
        command_folder = os.path.join(os.path.dirname(__file__),
                                      '..', 'commands')
        command_dirs = {
            'gandi.cli': command_folder
        }

        if 'GANDICLI_PATH' in os.environ:
            for _path in os.environ.get('GANDICLI_PATH').split(':'):
                # remove trailing separator if any
                path = _path.rstrip(os.sep)
                command_dirs[os.path.basename(path)] = os.path.join(path,
                                                                    'commands')

        for module_basename, dir in list(command_dirs.items()):
            for filename in sorted(os.listdir(dir)):
                if filename.endswith('.py') and '__init__' not in filename:
                    submod = filename[:-3]
                    module_name = module_basename + '.commands.' + submod
                    __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        """ Invoke command in context. """
        ctx.obj = GandiContextHelper(verbose=ctx.obj['verbose'])
        click.Group.invoke(self, ctx)


cli = GandiCLI()
cli.load_commands()
