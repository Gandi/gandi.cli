""" Mail namespace commands. """

import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_mailbox, output_list
from gandi.cli.core.params import pass_gandi, EMAIL_TYPE


@cli.command()
@click.option('--limit', help='Limit number of results.',
              default=100, show_default=True)
@click.argument('domain', metavar='domain.tld')
@pass_gandi
def list(gandi, domain, limit):
    """List mailboxes created on a domain."""
    options = {'items_per_page': limit}
    mailboxes = gandi.mail.list(domain, options)
    output_list(gandi, [mbox['login'] for mbox in mailboxes])
    return mailboxes


@cli.command()
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def info(gandi, email):
    """Display information about a mailbox."""
    login, domain = email

    output_keys = ['login', 'aliases', 'fallback', 'quota', 'responder']
    mailbox = gandi.mail.info(domain, login)
    output_mailbox(gandi, mailbox, output_keys)

    return mailbox


@cli.command()
@click.option('--quota', '-q', help='Set quota on mailbox. 0 is unlimited.',
              default=None, type=click.INT)
@click.option('--fallback', '-f', help='Add fallback address.',
              default=None)
@click.option('--alias', '-a', help='Add mailbox alias.',
              multiple=True, required=False)
@click.option('--password', '-p', default=None, type=click.STRING,
              required=False, help='Prompt a password to create a mailbox.')
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def create(gandi, email, quota, fallback, alias, password):
    """Create a mailbox."""
    login, domain = email
    options = {}

    if not password:
        password = click.prompt('password', hide_input=True,
                                confirmation_prompt=True)
    options['password'] = password
    if quota is not None:
        options['quota'] = quota
    if fallback is not None:
        options['fallback_email'] = fallback

    result = gandi.mail.create(domain, login, options, alias)

    return result


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def delete(gandi, email, force):
    """Delete a mailbox."""
    login, domain = email

    if not force:
        proceed = click.confirm('Are you sure to delete the '
                                'mailbox %s@%s ?' % (login, domain))

        if not proceed:
            return

    result = gandi.mail.delete(domain, login)

    return result


@cli.command()
@click.option('--password', '-p', help='Prompt a password to set a mailbox.',
              is_flag=True)
@click.option('--quota', '-q', help='Set quota on mailbox. 0 is unlimited.',
              default=None, type=click.INT)
@click.option('--fallback', '-f', help='Add fallback address.',
              default=None, show_default=True)
@click.option('--alias-add', '-a', help='Add mailbox alias.',
              multiple=True, required=False)
@click.option('--alias-del', '-d', help='Delete mailbox alias.',
              multiple=True, required=False)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def update(gandi, email, password, quota, fallback, alias_add, alias_del):
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

    result = gandi.mail.update(domain, login, options, alias_add, alias_del)

    return result


@cli.command()
@click.option('--bg', '--background', default=False, is_flag=True,
              help='Run command in background mode (default=False).')
@click.option('--force', '-f', is_flag=True,
              help='This is a dangerous option that will cause CLI to continue'
                   ' without prompting. (default=False).')
@click.option('--alias', '-a', help='Purge all aliases.', default=False,
              is_flag=True)
@click.argument('email', type=EMAIL_TYPE, metavar='login@domain.tld')
@pass_gandi
def purge(gandi, email, background, force, alias):
    """Purge a mailbox."""
    login, domain = email
    if alias:
        if not force:
            proceed = click.confirm('Are you sure to purge all aliases for '
                                    'mailbox %s@%s ?' % (login, domain))
            if not proceed:
                return
        result = gandi.mail.set_alias(domain, login, [])
    else:
        if not force:
            proceed = click.confirm('Are you sure to purge mailbox %s@%s ?'
                                    % (login, domain))
            if not proceed:
                return
        result = gandi.mail.purge(domain, login, background)

    return result
