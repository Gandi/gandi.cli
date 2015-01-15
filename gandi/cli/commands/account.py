""" Account namespace commands. """

from gandi.cli.core.cli import cli
from gandi.cli.core.utils import output_generic
from gandi.cli.core.params import pass_gandi


@cli.command()
@pass_gandi
def info(gandi):
    """Display infromation about hosting account.
    """
    output_keys = ['handle', 'credits']

    account = gandi.account.info()
    output_generic(gandi, account, output_keys)
    return account
