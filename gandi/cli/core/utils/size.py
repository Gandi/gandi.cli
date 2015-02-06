"""Size related methods."""

import click
from gandi.cli.core.cli import compatcallback


@compatcallback
def disk_check_size(ctx, param, value):
    """ Validation callback for disk size parameter."""
    if value and value % 1024:
        raise click.ClickException('Size must be a multiple of 1024.')
    return value
