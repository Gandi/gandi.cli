""" Mail commands module. """

from gandi.cli.core.base import GandiModule


class Mail(GandiModule):

    """ Module to handle CLI commands.

    $ gandi mail create
    $ gandi mail delete
    $ gandi mail info
    $ gandi mail list
    $ gandi mail purge
    $ gandi mail update

    """

    @classmethod
    def list(cls, domain, options):
        """List mailboxes for a given domain name."""
        return cls.call('domain.mailbox.list', domain, options)

    @classmethod
    def info(cls, domain, login):
        """Display information about a mailbox."""
        return cls.call('domain.mailbox.info', domain, login)

    @classmethod
    def create(cls, domain, login, options, alias):
        """Create a mailbox."""
        cls.echo('Creating your mailbox.')
        result = cls.call('domain.mailbox.create', domain, login, options)

        if alias:
            cls.echo('Creating aliases.')
            result = cls.set_alias(domain, login, list(alias))

        return result

    @classmethod
    def delete(cls, domain, login):
        """Delete a mailbox."""
        return cls.call('domain.mailbox.delete', domain, login)

    @classmethod
    def update(cls, domain, login, options, alias_add, alias_del):
        """Update a mailbox."""
        cls.echo('Updating your mailbox.')
        result = cls.call('domain.mailbox.update', domain, login, options)

        if alias_add or alias_del:
            current_aliases = cls.info(domain, login)['aliases']
            aliases = current_aliases[:]
            if alias_add:
                for alias in alias_add:
                    if alias not in aliases:
                        aliases.append(alias)
            if alias_del:
                for alias in alias_del:
                    if alias in aliases:
                        aliases.remove(alias)

            if ((len(current_aliases) != len(aliases))
                    or (current_aliases != aliases)):
                cls.echo('Updating aliases.')
                result = cls.set_alias(domain, login, aliases)

        return result

    @classmethod
    def purge(cls, domain, login, background=False):
        """Purge a mailbox."""
        oper = cls.call('domain.mailbox.purge', domain, login)
        if background:
            return oper
        else:
            cls.echo('Purging in progress')
            cls.display_progress(oper)

    @classmethod
    def set_alias(cls, domain, login, aliases):
        """Update aliases on a mailbox."""
        return cls.call('domain.mailbox.alias.set', domain, login, aliases)
