
import click
from gandi.cli import cli
from gandi.conf import pass_gandi


@cli.command()
@click.option('--state', default=None, help='filter results by state')
@click.option('--id', help='display ids', is_flag=True)
@pass_gandi
def list(gandi, state, id):
    """list virtual machines"""

    options = {}
    if state:
        options['state'] = state

    result = gandi.call('vm.list', options)
    for vm in result:
        if id:
            print '#%d - %s - %s' % (vm['id'], vm['hostname'], vm['state'])
        else:
            print '%s - %s' % (vm['hostname'], vm['state'])


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def info(gandi, id):
    """display information for a virtual machine"""

    result = gandi.call('vm.info', id)
    from pprint import pprint
    pprint(result)


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def stop(gandi, id):
    """stop a virtual machine"""

    result = gandi.call('vm.stop', id)
    from pprint import pprint
    pprint(result)


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def start(gandi, id):
    """start a virtual machine"""

    result = gandi.call('vm.start', id)
    from pprint import pprint
    pprint(result)


@cli.command()
@click.argument('id', type=click.INT)
@pass_gandi
def reboot(gandi, id):
    """reboot a virtual machine"""

    result = gandi.call('vm.reboot', id)
    from pprint import pprint
    pprint(result)
