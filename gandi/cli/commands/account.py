""" Account namespace commands. """

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_account
from gandi.cli.core.params import pass_gandi


@cli.command()
@pass_gandi
def info(gandi):
    """Display information about hosting account.
    """
    output_keys = ['handle', 'credit', 'prepaid']

    account = gandi.account.all()
    account['prepaid_info'] = gandi.contact.balance().get('prepaid', {})
    output_account(gandi, account, output_keys)
    return account
