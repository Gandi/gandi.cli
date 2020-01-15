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

    summary = gandi.status.summary()

    # * create a dict with service id as key
    # * collect leaf services
    serv_by_id = {}
    leaf_serv = []
    for serv in summary[u"components"]:
        serv_by_id[serv[u"id"]] = serv

        if not serv[u"group"]:
            leaf_serv.append(serv)

    # * compute long service name (parent groupe name + service name)
    # * filter wanted service
    serv_by_name = {}
    for serv in leaf_serv:
        if serv[u"group_id"] is None:
            group_name = None
            service_name = serv['name']
        else:
            group_name = serv_by_id[serv[u"group_id"]][u"name"]
            service_name = '%s - %s' % (group_name, serv['name'],)

        # does the user picked a specific services ?
        if service is not None:
            if service not in (serv['name'], group_name, service_name):
                continue

        serv_by_name[service_name] = serv

    # process each service leaf
    services_report = []
    for service_name in sorted(serv_by_name.keys()):
        serv = serv_by_name[service_name]

        # this is a relevant service, add it to report
        services_report.append({
            u'name': serv[u'name'],
            u'status': serv[u'status'],
            u'description': serv[u'description'],
        })

        # no major outage for this service, just print service status
        if serv[u'status'] != 'major_outage':
            output_service(gandi, service_name, serv['status'], justify=30)
            continue

        # a major outage is in progress for that service
        # print every related incidents
        for incident in summary[u'incidents']:
            for incident_component in incident[u"components"]:
                if serv[u"id"] == incident_component[u"id"]:
                    break
            else:
                continue

            service_detail = '%s - %s'
            service_detail %= (incident[u'name'], incident[u'shortlink'])
            output_service(gandi, service_name, service_detail, justify=30)

    return services_report
