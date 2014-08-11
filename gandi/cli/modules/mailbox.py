from gandi.cli.core.base import GandiModule

class Mailbox(GandiModule):

  @classmethod
  def list(cls, domain, options):
    """list mailboxes for a given domain name"""

    return cls.call('domain.mailbox.list', domain, options)

  @classmethod
  def info(cls, domain, login):
    """Display information about a mailbox"""

    return cls.call('domain.mailbox.info', domain, login)
  
  @classmethod
  def set_alias(cls, domain, login, aliases):
    """Add an alias on a mailbox"""

    return cls.call('domain.mailbox.alias.set', domain, login, aliases)