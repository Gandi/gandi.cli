import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_list
from gandi.cli.core.params import pass_gandi, EMAIL_TYPE


@cli.command(options_metavar='')
@click.option('--limit', help='limit number of results',
              default=100, show_default=True)
@click.argument('domain', metavar='domain.tld')
@pass_gandi
def list(gandi, domain, limit):
    """List mailboxes created on a domain."""

    options = {'items_per_page': limit}
    mailboxes = gandi.mail.list(domain, options)
    for mailbox in mailboxes:
        gandi.echo(mailbox['login'])

    return mailboxes


@cli.command(options_metavar='')
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def info(gandi, email):
    """Display information about a mailbox."""

    login, domain = email

    output_keys = ['login', 'aliases', 'fallback_email', 'quota', 'responder']
    mailbox = gandi.mail.info(domain, login)
    output_generic(gandi, mailbox, output_keys, justify=12)

    return mailbox


@cli.command(options_metavar='')
@click.option('--quota', '-q', help='set a quota on a mailbox. 0 is unlimited',
              default=None, type=click.INT)
@click.option('--fallback', '-f', help='add an address of fallback',
              default=None)
@click.option('--alias', '-a', help='add aliases on a mailbox',
              multiple=True, required=False)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def create(gandi, email, quota, fallback, alias):
    """Create a mailbox."""
    login, domain = email
    options = {}
    if alias:
        aliases = gandi.mail.info(domain, login)['aliases']
        for element in alias:
            aliases.append(element)

        result = gandi.mail.set_alias(domain, login, aliases)
    else:
        password = click.prompt('password', hide_input=True,
                                confirmation_prompt=True)
        options['password'] = password
        if quota is not None:
            options['quota'] = quota
        if fallback is not None:
            options['fallback_email'] = fallback
        options['password'] = password

        result = gandi.mail.create(domain, login, options)

    return result


@cli.command(options_metavar='')
@click.option('--force', '-f', help='Force the deletion of the mailbox',
              is_flag=True)
@click.option('--alias', '-a', help='Remove aliases on a mailbox',
              multiple=True)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def delete(gandi, email, force, alias):
    """Delete a mailbox."""

    login, domain = email

    if alias:
        aliases = gandi.mail.info(domain, login)['aliases']
        for element in alias:
            aliases.remove(element)
        result = gandi.mail.set_alias(domain, login, aliases)
    else:
        if not force:
            proceed = click.confirm('Are you sure to delete the'
                                    'mailbox %s@%s ?' % (login, domain))

            if not proceed:
                return

        result = gandi.mail.delete(domain, login)

    return result


@cli.command()
@click.option('--password', '-p', help='prompt a password to set a mailbox',
              is_flag=True)
@click.option('--quota', '-q', help='set a quota on a mailbox. 0 is unlimited',
              default=None, type=click.INT)
@click.option('--fallback', '-f', help='add an address of fallback',
              default=None, show_default=True)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def update(gandi, email, password, quota, fallback):
    """Update a mailbox."""

    options = {}

    if password:
        password = click.prompt('password', hide_input=True,
                                confirmation_prompt=True)
        options['password'] = password

    if quota is not None:
        options['quota'] = quota

    if fallback is not None:
        options['fallback_email'] = fallback

    login, domain = email

    result = gandi.mail.update(domain, login, options)

    return result


@cli.command(options_metavar='')
@click.option('--bg', '--background', default=False, is_flag=True,
              help='run command in background mode (default=False)')
@click.option('--force', '-f', help='Force the deletion of the mailbox',
              is_flag=True)
@click.option('--alias', '-a', help='Purge all aliases', default=False,
              is_flag=True)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def purge(gandi, email, background, force, alias):
    """Purge a mailbox."""

    login, domain = email
    if alias:
        if not force:
            proceed = click.confirm('Are you sure to purge the aliases on the'
                                    'mailbox %s@%s ?' % (login, domain))
            if not proceed:
                return
        result = gandi.mail.set_alias(domain, login, [])
    else:
        if not force:
            proceed = click.confirm('Are you sure to purge the '
                                    'mailbox %s@%s ?' % (login, domain))
            if not proceed:
                return
        result = gandi.mail.purge(domain, login, background)

    return result
