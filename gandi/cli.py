#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path

import click

from .conf import GandiContextHelper


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


def main():
    cli(obj={})


if __name__ == "__main__":
    main()

