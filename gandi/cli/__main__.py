#!/usr/bin/python
# -*- coding: utf-8 -*-

from .core.cli import GandiCLI

cli = GandiCLI()
cli.load_commands()


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
