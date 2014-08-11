import click

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic, output_list
from gandi.cli.core.params import pass_gandi


@cli.command()
@click.option('--limit', help='limit number of results', default=100, 
        show_default=True)
@click.argument('domain')
@pass_gandi
def list(gandi, domain, limit):
  """List mailboxes created on a domain"""

  options = {'items_per_page': limit}
  mailboxes = gandi.mailbox.list(domain, options)
  for mailbox in mailboxes:
      gandi.echo(mailbox['login'])

  return mailboxes

@cli.command()
@click.argument('domain')
@click.argument('login')
@pass_gandi
def info(gandi, domain, login):
  """Display information about a mailbox"""
  
  output_keys = ['login', 'aliases', 'fallback_email', 'quota', 'responder']  
  mailbox = gandi.mailbox.info(domain, login)
  
  output_generic(gandi, mailbox, output_keys, justify=8)
  
  return mailbox

@cli.command()
@click.argument('domain')
@click.argument('login')
@click.argument('alias')
@pass_gandi
def add_alias(gandi, domain, login, alias):
  """Add an alias on a mailbox"""

  aliases = gandi.mailbox.info(domain, login)['aliases']
  aliases.append(alias)
  gandi.mailbox.set_alias(domain, login, aliases)
  output_list(gandi, aliases)

  return aliases

@cli.command()
@click.argument('domain')
@click.argument('login')
@click.argument('alias')
@pass_gandi
def delete_alias(gandi, domain, login, alias):
  """Remove an alias on a mailbox"""

  aliases = gandi.mailbox.info(domain, login)['aliases']
  aliases.remove(alias)
  gandi.mailbox.set_alias(domain, login, aliases)
  output_list(gandi, aliases)

  return aliases