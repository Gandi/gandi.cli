import click
import re
from click.decorators import _param_memo

from gandi.cli.core.base import GandiContextHelper


class DatacenterParamType(click.Choice):
    """ Choice parameter to select a datacenter between available ones. """
    name = 'datacenter'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['iso'] for item in gandi.datacenter.list()]
        self.choices = choices

    def convert(self, value, param, ctx):
        value = value.upper()
        return click.Choice.convert(self, value, param, ctx)


class PaasTypeParamType(click.Choice):
    """ Choice parameter to select a PaaS type between available ones. """
    name = 'paas type'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['name'] for item in gandi.paas.type_list()]
        self.choices = choices


class IntChoice(click.Choice):
    """ Choice parameter to select an integer value in a set of int values"""
    name = 'integer choice'

    def convert(self, value, param, ctx):
        try:
            value = str(value)
        except Exception:
            pass
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class DiskImageParamType(click.Choice):
    """ Choice parameter to select a disk image between available ones. """
    name = 'images'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['label'] for item in gandi.image.list()]
        self.choices = choices

    def convert(self, value, param, ctx):
        # Exact match
        if value in self.choices:
            return value

        # Try to find 64 bits version
        new_value = '%s 64 bits' % value
        if new_value in self.choices:
            return new_value

        # Try to find without specific bits version
        p = re.compile(' (64|32) bits')
        new_value = p.sub('', value)
        if new_value in self.choices:
            return new_value

        self.fail('invalid choice: %s. (choose from %s)' %
                  (value, ', '.join(self.choices)), param, ctx)


class SnapshotParamType(click.Choice):
    """ Choice parameter to select a snapshot profile between available ones.
    """
    name = 'snapshot profile'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [str(item['id']) for item in gandi.snapshotprofile.list()]
        self.choices = choices

    def convert(self, value, param, ctx):
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class CertificatePackage(click.Choice):
    """ Choice parameter to select a certificate package between available
    ones.
    """
    name = 'certificate package'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['name'] for item in gandi.certificate.package_list()]
        self.choices = choices


class CertificateDcvMethod(click.Choice):
    """ Choice parameter to select a certificate dcv method.
        * 'email' will send you an email to check domain ownership
        * 'dns' will require you to add a TXT record in your domain zone
        * 'file' will require you to add a file on you server
        * 'auto' can only be used when your domain and it's zone are on the
          same gandi account you are currently using (gandi will add the TXT
          dns record).
    """
    name = 'certificate dcv method'
    choices = ['email', 'dns', 'file', 'auto']

    def __init__(self):
        pass


class EmailParamType(click.ParamType):
    """Check the email value and return a list ['login', 'domain']"""
    name = 'email'

    def convert(self, value, param, ctx):
        rxp = '^[^@]+?@[-.a-z0-9]+$'
        regex = re.compile(rxp, re.I)
        try:
            if regex.match(value):
                value = value.split("@")
                return value
            else:
                self.fail('%s is not a valid email address' % value, param,
                          ctx)
        except ValueError:
            self.fail('%s is not a valid email address' % value, param, ctx)


DATACENTER = DatacenterParamType()
PAAS_TYPE = PaasTypeParamType()
DISK_IMAGE = DiskImageParamType()
SNAPSHOTPROFILE = SnapshotParamType()
CERTIFICATE_PACKAGE = CertificatePackage()
CERTIFICATE_DCV_METHOD = CertificateDcvMethod()
EMAIL_TYPE = EmailParamType()


class GandiOption(click.Option):
    """ Custom command option class for handling configuration files

    When no value was found on command line, try to pull it from configuration
    Display default or configuration value when needed
    """

    def display_value(self, ctx, value):
        """ Display value to be used for this parameter """
        gandi = ctx.obj
        gandi.log('%s: %s' % (self.name, (value if value is not None
                                          else 'Not found')))

    def get_default(self, ctx):
        """ Retrieve default value and display it when prompt disabled """
        value = click.Option.get_default(self, ctx)
        if not self.prompt:
            # value found in default display it
            self.display_value(ctx, value)
        return value

    def consume_value(self, ctx, opts):
        """ Retrieve default value and display it when prompt is disabled """
        value = click.Option.consume_value(self, ctx, opts)
        if not value:
            # value not found by click on command line
            # now check using our context helper in order into
            # local configuration
            # global configuration
            gandi = ctx.obj
            value = gandi.get(self.name)
            if value is not None:
                # value found in configuration display it
                self.display_value(ctx, value)
            else:
                if self.default is None:
                    metavar = ''
                    if self.type.name not in ['integer', 'text']:
                        metavar = self.make_metavar()
                    prompt = '%s %s' % (self.help, metavar)
                    gandi.echo(prompt)
        return value

    def handle_parse_result(self, ctx, opts, args):
        """ Save value for this option in configuration """
        value, args = click.Option.handle_parse_result(self, ctx, opts, args)

        if value is not None:
            # save to gandi configuration
            gandi = ctx.obj
            gandi.configure(True, self.name, value)
        return value, args


def option(*param_decls, **attrs):
    """Attaches an option to the command.  All positional arguments are
    passed as parameter declarations to :class:`Option`, all keyword
    arguments are forwarded unchanged.  This is equivalent to creating an
    :class:`Option` instance manually and attaching it to the
    :attr:`Command.params` list.
    """
    def decorator(f):
        _param_memo(f, GandiOption(param_decls, **attrs))
        return f
    return decorator

# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper)
