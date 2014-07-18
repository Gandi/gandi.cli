import click
from click.exceptions import UsageError

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_sshkey
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--id', help='display ids', is_flag=True)
@click.option('--limit', help='limit number of results', default=100,
              show_default=True)
@pass_gandi
def list(gandi, id, limit):
    '''List ssh keys.'''
    options = {
        'items_per_page': limit,
    }

    output_keys = ['name', 'fingerprint']

    if id:
        output_keys.append('id')

    result = gandi.sshkey.list(options)
    for sshkey in result:
        gandi.separator_line()
        output_sshkey(gandi, sshkey, output_keys)

    return result


@cli.command()
@click.argument('resource', nargs=-1)
@click.option('--id', help='display ids', is_flag=True)
@click.option('--value', help='display value', is_flag=True)
@pass_gandi
def info(gandi, resource, id, value):
    '''Display information about an ssh key.

    Ressource can be a name or an ID
    '''
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
@click.option('--name', help='the ssh key name', required=True)
@click.option('--value', help='the content of the ssh key')
@click.option('--sshkey', type=click.File('r'), help='the ssh key file')
@pass_gandi
def create(gandi, name, value=None, sshkey=None):
    '''Create a new ssh key.'''
    if not value and not sshkey:
        raise UsageError('You must set value OR sshkey.')

    if value and sshkey:
        raise UsageError('You must not set value AND sshkey.')

    if sshkey:
        value = sshkey.read()

    ret = gandi.sshkey.create(name, value)
    if not ret:
        return

    output_keys = ['id', 'name', 'fingerprint']
    return output_sshkey(gandi, ret, output_keys)


@cli.command()
@click.argument('resource', nargs=-1)
@pass_gandi
def delete(gandi, resource):
    '''Delete thoses ssh keys.

    Ressource can be a name or an ID
    '''
    for item in resource:
        gandi.sshkey.delete(item)
