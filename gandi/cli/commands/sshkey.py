""" SSH keys namespace commands. """

import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_sshkey
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--limit', help='Limit number of results.', default=100,
              show_default=True)
@pass_gandi
def list(gandi, id, limit):
    """ List SSH keys. """
    options = {
        'items_per_page': limit,
    }

    output_keys = ['name', 'fingerprint']

    if id:
        output_keys.append('id')

    result = gandi.sshkey.list(options)
    for num, sshkey in enumerate(result):
        if num:
            gandi.separator_line()
        output_sshkey(gandi, sshkey, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@click.option('--id', help='Display ids.', is_flag=True)
@click.option('--value', help='Display value.', is_flag=True)
@pass_gandi
def info(gandi, resource, id, value):
    """Display information about an SSH key.

    Resource can be a name or an ID
    """
    output_keys = ['name', 'fingerprint']
    if id:
        output_keys.append('id')

    if value:
        output_keys.append('value')

    ret = []
    for item in resource:
        sshkey = gandi.sshkey.info(item)
        ret.append(output_sshkey(gandi, sshkey, output_keys))

    return ret


@cli.command()
@click.option('--name', help='SSH key name.', required=True)
@click.option('--value', help='Content of the SSH key.')
@click.option('--filename', type=click.File('r'), help='SSH key file.')
@pass_gandi
def create(gandi, name, value=None, filename=None):
    """ Create a new SSH key. """
    if not value and not filename:
        raise UsageError('You must set value OR filename.')

    if value and filename:
        raise UsageError('You must not set value AND filename.')

    if filename:
        value = filename.read()

    ret = gandi.sshkey.create(name, value)

    output_keys = ['id', 'name', 'fingerprint']
    return output_sshkey(gandi, ret, output_keys)


@cli.command()
@click.argument('resource', nargs=-1, required=True)
@pass_gandi
def delete(gandi, resource):
    """Delete SSH keys.

    Resource can be a name or an ID
    """
    for item in resource:
        gandi.sshkey.delete(item)
