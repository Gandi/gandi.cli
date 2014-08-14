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
    def create(cls, domain, login, options):
        """Create a mailbox"""

        return cls.call('domain.mailbox.create', domain, login, options)

    @classmethod
    def delete(cls, domain, login):
        """Delete a mailbox"""

        return cls.call('domain.mailbox.delete', domain, login)

    @classmethod
    def update(cls, domain, login, options):
        """Update a mailbox"""

        return cls.call('domain.mailbox.update', domain, login, options)

    @classmethod
    def purge(cls, domain, login, background=False):
        """Purge a mailbox"""

        oper = cls.call('domain.mailbox.purge', domain, login)
        if background:
            return oper
        else:
            cls.echo("Purge in progress")
            cls.display_progress(oper)

    @classmethod
    def set_alias(cls, domain, login, aliases):
        """Update aliases on a mailbox"""

        return cls.call('domain.mailbox.alias.set', domain, login, aliases)
