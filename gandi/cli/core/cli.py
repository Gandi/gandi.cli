# -*- coding: utf-8 -*-
""" GandiCLI class declaration and initialization. """

import os
import os.path
import inspect
import platform
from functools import update_wrapper

import click

from .base import GandiContextHelper
from gandi.cli import __version__

try:
    use_man_epilog = platform.system() == 'Linux'
except:
    pass


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

    def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.

        Display custom help for all subcommands.
        """
        rows = []

        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:  # pragma: no cover
                continue

            if isinstance(cmd, click.core.Group):
                for sub_cmd in cmd.list_commands(ctx):
                    sub = cmd.get_command(ctx, sub_cmd)
                    help = sub.short_help or ''
                    rows.append(('%s %s' % (subcommand, sub_cmd), help))
            else:
                help = cmd.short_help or ''
                rows.append((subcommand, help))

        if rows:
            with formatter.section('Commands'):
                formatter.write_dl(rows)

    def list_sub_commmands(self, cmd_name, cmd):
        """Return all commands for a group"""
        ret = {}
        if isinstance(cmd, click.core.Group):
            for sub_cmd_name in cmd.commands:
                sub_cmd = cmd.commands[sub_cmd_name]
                sub = self.list_sub_commmands(sub_cmd_name, sub_cmd)
                if sub:
                    ret['%s %s' % (cmd_name, sub[0])] = sub[1]
        elif isinstance(cmd, click.core.Command):
            # XXX: patch each command with an epilog
            if cmd.epilog is None and use_man_epilog:
                cmd.epilog = 'For detailed documentation, use `man gandi`.'
            return (cmd.name, cmd)
        return ret

    def list_all_commands(self, ctx):
        ret = {}
        for cmd_name in self.commands:
            cmd = self.commands[cmd_name]
            sub = self.list_sub_commmands(cmd_name, cmd)
            if sub:
                if isinstance(sub, tuple):
                    ret[sub[0]] = sub[1]
                else:
                    ret.update(sub)
        return ret

    def resolve_command(self, ctx, args):
        cmd_name = args[0]
        all_cmds = self.list_all_commands(ctx)

        # Get the command
        cmd = click.Group.get_command(self, ctx, cmd_name)

        sub_cmd = False
        if len(args) > 1:
            ns_len = 1
            if isinstance(cmd, click.core.Group):
                ns_len = getattr(cmd, 'ns_len', 2)
            # XXX: dirty hack to handle namespaces by merging all args
            # i.e : paas + list = 'paas list'
            new_cmd_name = ' '.join(args[0:ns_len])
            cmd = all_cmds.get(new_cmd_name)
            if cmd is not None:
                sub_cmd = True
                cmd_name = new_cmd_name

        cmd = all_cmds.get(cmd_name)
        if cmd is not None and not isinstance(cmd, click.core.Group):
            if sub_cmd:
                del args[1]
            return cmd_name, cmd, args[1:]

        formatter = ctx.make_formatter()

        matches = [x for x in all_cmds if x.startswith(cmd_name)]
        if not matches:
            self.format_commands(ctx, formatter)
            print(formatter.getvalue().rstrip('\n'))
            ctx.exit()

        elif len(matches) == 1:
            if sub_cmd:
                del args[1]
            cmd = all_cmds[matches[0]]
            return cmd_name, cmd, args[1:]

        rows = []
        for matched in sorted(matches):
            cmd = all_cmds.get(matched)
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

    def group(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a group to
        the group.  This takes the same arguments as :func:`group` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        def decorator(f):
            ns_len = kwargs.pop('ns_len', 2)
            cmd = click.group(*args, **kwargs)(f)
            cmd.ns_len = ns_len
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
