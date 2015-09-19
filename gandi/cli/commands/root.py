""" Main namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_service
from gandi.cli.core.params import pass_gandi


@cli.command()
@pass_gandi
def setup(gandi):
    """ Initialize Gandi CLI configuration.

    Create global configuration directory with API credentials
    """
    intro = """Welcome to GandiCLI, let's configure a few things before we \
start.
"""

    outro = """
Setup completed. You can now:
* use 'gandi' to see all command.
* use 'gandi vm create' to create and access a Virtual Machine.
* use 'gandi paas create' to create and access a SimpleHosting instance.
"""
    gandi.echo(intro)
    gandi.init_config()
    gandi.echo(outro)


@cli.command()
@pass_gandi
def api(gandi):
    """Display information about API used."""
    key_name = 'API version'

    result = gandi.api.info()
    result[key_name] = result.pop('api_version')
    output_generic(gandi, result, [key_name])

    return result


@cli.command()
@click.argument('command', required=False, nargs=-1)
@click.pass_context
def help(ctx, command):
    """Display help for a command."""
    command = ' '.join(command)
    if not command:
        click.echo(cli.get_help(ctx))
        return

    cmd = cli.get_command(ctx, command)
    if cmd:
        click.echo(cmd.get_help(ctx))
    else:
        click.echo(cli.get_help(ctx))


@cli.command()
@click.argument('service', required=False)
@pass_gandi
def status(gandi, service):
    """Display current status from status.gandi.net."""

    if not service:
        global_status = gandi.status.status()
        if global_status['status'] == 'FOGGY':
            # something is going on but not affecting services
            filters = {
                'category': 'Incident',
                'current': True,
            }
            events = gandi.status.events(filters)
            for event in events:
                if event['services']:
                    # do not process services
                    continue
                event_url = gandi.status.event_timeline(event)
                service_detail = '%s - %s' % (event['title'], event_url)
                gandi.echo(service_detail)

    # then check other services
    descs = gandi.status.descriptions()
    needed = services = gandi.status.services()
    if service:
        needed = [serv for serv in services
                  if serv['name'].lower() == service.lower()]

    for serv in needed:
        if serv['status'] != 'STORMY':
            output_service(gandi, serv['name'], descs[serv['status']])
            continue

        filters = {
            'category': 'Incident',
            'services': serv['name'],
            'current': True,
        }
        events = gandi.status.events(filters)
        for event in events:
            event_url = gandi.status.event_timeline(event)
            service_detail = '%s - %s' % (event['title'], event_url)
            output_service(gandi, serv['name'], service_detail)

    return services
