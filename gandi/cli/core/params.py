""" Custom command line validation parameters. """

import re
import sys

import click
from click.decorators import _param_memo

from gandi.cli.core.base import GandiContextHelper


class GandiChoice(click.Choice):

    """ Base class for custom Choice parameters. """

    gandi = None

    def __init__(self):
        """ Initialize choices list. """
        self._choices = []

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        raise NotImplementedError

    @property
    def choices(self):
        """ Retrieve choices from API if possible"""
        if not self._choices:
            gandi = self.gandi or GandiContextHelper()
            self._choices = self._get_choices(gandi)
            if not self._choices:
                api = self.gandi.get_api_connector()
                gandi.echo('Please check that you are connecting to the good '
                           "api '%s' and that it's running." % (api.host))
                sys.exit(1)

        return self._choices

    def convert(self, value, param, ctx):
        """ Internal method to use correct context. """
        self.gandi = ctx.obj
        return click.Choice.convert(self, value, param, ctx)

    def convert_deprecated_value(self, value):
        """ To override when needed """
        return value


class DatacenterParamType(GandiChoice):

    """ Choice parameter to select an available datacenter. """

    name = 'datacenter'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        iso_codes = []
        dc_codes = []
        for item in gandi.datacenter.list():
            iso_codes.append(item['iso'])
            if item.get('dc_code'):
                dc_codes.append(item['dc_code'])
        return dc_codes + iso_codes

    def convert(self, value, param, ctx):
        """ Convert value to uppercase. """
        self.gandi = ctx.obj
        value = value.upper()
        return click.Choice.convert(self, value, param, ctx)

    def convert_deprecated_value(self, value):
        """ To update the configuration with the new datacenter naming """
        convert = {
            'FR': 'FR-SD2',
            'LU': 'LU-BI1',
            'US': 'US-BA1',
        }
        return convert.get(value, value)


class PaasTypeParamType(GandiChoice):

    """ Choice parameter to select an available PaaS instance type. """

    name = 'paas type'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        return [item['name'] for item in gandi.paas.type_list()]


class IntChoice(click.Choice):

    """ Choice parameter to select an integer value in a set of int values."""

    name = 'integer choice'

    def convert(self, value, param, ctx):
        """ Convert value to int. """
        self.gandi = ctx.obj
        try:
            value = str(value)
        except Exception:
            pass
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class DiskImageParamType(GandiChoice):

    """ Choice parameter to select an available disk image. """

    name = 'images'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        image_list = [item['label'] for item in gandi.image.list()]
        disk_list = [item['name'] for item in gandi.disk.list_create()]
        return sorted(tuple(set(image_list))) + disk_list

    def convert(self, value, param, ctx):
        """ Try to find correct disk image regarding version. """
        self.gandi = ctx.obj
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


class KernelParamType(GandiChoice):

    """ Choice parameter to select an available kernel. """

    name = 'kernels'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        kernel_families = list(gandi.kernel.list(1).values())
        return [kernel for klist in kernel_families for kernel in klist]

    def convert(self, value, param, ctx):
        """ Try to find correct kernel regarding version. """
        self.gandi = ctx.obj
        # Exact match first
        if value in self.choices:
            return value

        # Also try with x86-64 suffix
        new_value = '%s-x86_64' % value
        if new_value in self.choices:
            return new_value

        self.fail('invalid choice: %s. (choose from %s)' %
                  (value, ', '.join(self.choices)), param, ctx)


class SnapshotParamType(GandiChoice):

    """ Choice parameter to select an available snapshot profile. """

    name = 'snapshot profile'
    target = None

    def __init__(self, target=None):
        """ Initialize choices list. """
        self._choices = []
        self.target = target

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        return [str(item['id'])
                for item in gandi.snapshotprofile.list(target=self.target)]

    def convert(self, value, param, ctx):
        """ Convert value to int. """
        self.gandi = ctx.obj
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class CertificatePackage(GandiChoice):

    """ Choice parameter to select an available certificate package. """

    name = 'certificate package'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        return [item['name'] for item in gandi.certificate.package_list()]


class CertificatePackageType(CertificatePackage):

    """ Choice parameter to select an available certificate package type. """

    name = 'certificate package type'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        packages = super(CertificatePackageType, self)._get_choices(gandi)
        return list(set([pack.split('_')[1] for pack in packages]))


class CertificatePackageMax(CertificatePackage):

    """
    Choice parameter to select an available certificate package max altname.
    """

    name = 'certificate package max'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        packages = super(CertificatePackageMax, self)._get_choices(gandi)
        ret = list(set([pack.split('_')[2] for pack in packages]))
        if 'w' in ret:
            ret.remove('w')
        return ret

    def convert(self, value, param, ctx):
        """ Convert value to int. """
        self.gandi = ctx.obj
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class CertificatePackageWarranty(CertificatePackage):

    """ Choice parameter to select an available certificate warranty. """

    name = 'certificate package warranty'

    def _get_choices(self, gandi):
        """ Internal method to get choices list """
        packages = super(CertificatePackageWarranty, self)._get_choices(gandi)
        return list(set([pack.split('_')[3] for pack in packages]))

    def convert(self, value, param, ctx):
        """ Convert value to int. """
        self.gandi = ctx.obj
        value = click.Choice.convert(self, value, param, ctx)
        return int(value)


class CertificateDcvMethod(click.Choice):

    """ Choice parameter to select a certificate dcv method.

    * 'email' will send you an email to check domain ownership
    * 'dns' will require you to add a TXT record in your domain zone
    * 'file' will require you to add a file on you server
    * 'auto' can only be used when your domain and its zone are on the
       same gandi account you are currently using (gandi will add the TXT
       dns record).
    """

    name = 'certificate dcv method'
    choices = ['email', 'dns', 'file', 'auto']

    def __init__(self):
        """ Initialize choices list. """
        pass


class IpType(click.Choice):
    """ Choice parameter to filter on ip types.

    * 'private' will only retrieve private ips
    * 'public' will only retrieve public ips
    """

    name = 'ip type'
    choices = ['private', 'public']

    def __init__(self):
        """ Initialize choices list. """
        pass


class StringConstraint(click.types.StringParamType):

    """ Check that provided string matches constraints."""

    name = 'string constraints'

    def __init__(self, minlen=None, maxlen=None):
        self.min = minlen
        self.max = maxlen

    def convert(self, value, param, ctx):
        value = click.types.StringParamType.convert(self, value, param, ctx)
        rv = len(value)
        if self.min is not None and rv < self.min or \
           self.max is not None and rv > self.max:
            if self.min is None:
                self.fail('%s is longer than the maximum valid length '
                          '%s.' % (rv, self.max), param, ctx)
            elif self.max is None:
                self.fail('%s is shorter than the minimum valid length '
                          '%s.' % (rv, self.min), param, ctx)
            else:
                self.fail('%s is not in the valid length range of %s to %s.'
                          % (rv, self.min, self.max), param, ctx)
        return value

    def __repr__(self):
        return 'StringConstraint(%r, %r)' % (self.min, self.max)


class EmailParamType(click.ParamType):

    """Check the email value and return a list ['login', 'domain']. """

    name = 'email'

    def convert(self, value, param, ctx):
        """ Validate value using regexp. """
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


class SizeParamType(click.ParamType):
    name = 'size'
    suffixes = {'M': 0,
                'G': 1,
                'T': 2}
    prefixes = ['+']

    def convert(self, value, param, ctx):
        prefix = ''
        suffix = ''
        for i, c in enumerate(value):
            if not c.isdigit():
                if c in self.prefixes:
                    prefix = c
                    continue
                suffix = value[i:]
                value = value[:i]
                break
        try:
            mul = self.suffixes[suffix] if suffix else 0
            return prefix, int(value) * (1 << (mul * 10))
        except ValueError:
            self.fail("%r is not an integer" % (value))
        except KeyError:
            self.fail("%r is not a supported suffix" % (suffix))


class BackendParamType(click.ParamType):

    """

    Check the validity of the server ip and port and return a dict
    ['ip', 'port'].

    """

    name = 'backend'

    def convert(self, value, param, ctx):
        """ Validate value using regexp. """
        rxp = "^(((([1]?\d)?\d|2[0-4]\d|25[0-5])\.){3}(([1]?\d)?\d|2[0-4]\d|"\
              "25[0-5]))|([\da-fA-F]{1,4}(\:[\da-fA-F]{1,4}){7})|(([\da-fA-F]"\
              "{1,4}:){0,5}::([\da-fA-F]{1,4}:)"\
              "{0,5}[\da-fA-F]{1,4})$"
        regex = re.compile(rxp, re.I)
        backend = {}
        if value.count(':') == 0:
            # port is not set
            backend['ip'] = value
        elif value.count(':') == 7:
            # it's an ipv6 without port
            backend['ip'] = value
        elif value.count(':') == 8:
            # it's an ipv6 with port
            backend['ip'] = value.rsplit(':', 1)[0]
            backend['port'] = int(value.rsplit(':', 1)[1])
        else:
            backend['ip'] = value.split(':')[0]
            backend['port'] = int(value.split(':')[1])
        try:
            if regex.match(backend['ip']):
                return backend
            else:
                self.fail('%s is not a valid ip address' %
                          backend['ip'], param, ctx)
        except ValueError:
            self.fail('%s is not a valid ip address' % backend['ip'], param,
                      ctx)


class WebAccNameParamType(GandiChoice):
    """ Choice a webaccelerator """

    name = 'webacc list'

    def _get_choices(self, gandi):
        """ Internal method to get choice list """
        return [str(item['name']) for item in gandi.webacc.list()]


class WebAccVhostParamType(GandiChoice):
    """ Retrieve vhost on a webaccelerator """
    name = 'webacc vhost list'

    def _get_choices(self, gandi):
        """ Internal method to get choice list """
        return [str(item['name']) for item in gandi.webacc.vhost_list()]


class OperStepParamType(click.Choice):
    """ Choice parameter to filter on operation step """

    name = 'oper step'
    choices = ['BILL', 'WAIT', 'RUN', 'ERROR']

    def __init__(self):
        """ Initialize choices list. """
        pass


DATACENTER = DatacenterParamType()
PAAS_TYPE = PaasTypeParamType()
DISK_IMAGE = DiskImageParamType()
DISK_MAXLIST = 500
KERNEL = KernelParamType()
SNAPSHOTPROFILE_PAAS = SnapshotParamType('paas')
SNAPSHOTPROFILE_VM = SnapshotParamType('vm')
CERTIFICATE_PACKAGE = CertificatePackage()
CERTIFICATE_PACKAGE_TYPE = CertificatePackageType()
CERTIFICATE_PACKAGE_MAX = CertificatePackageMax()
CERTIFICATE_PACKAGE_WARRANTY = CertificatePackageWarranty()
CERTIFICATE_DCV_METHOD = CertificateDcvMethod()
EMAIL_TYPE = EmailParamType()
IP_TYPE = IpType()
SIZE = SizeParamType()
BACKEND = BackendParamType()
WEBACC_NAME = WebAccNameParamType()
WEBACC_VHOST_NAME = WebAccVhostParamType()
OPER_STEP = OperStepParamType()


class GandiOption(click.Option):

    """ Custom command option class for handling configuration files.

    When no value was found on command line, try to pull it from configuration
    Display default or configuration value when needed
    """

    def display_value(self, ctx, value):
        """ Display value to be used for this parameter. """
        gandi = ctx.obj
        gandi.log('%s: %s' % (self.name, (value if value is not None
                                          else 'Not found')))

    def get_default(self, ctx):
        """ Retrieve default value and display it when prompt disabled. """
        value = click.Option.get_default(self, ctx)
        if not self.prompt:
            # value found in default display it
            self.display_value(ctx, value)
        return value

    def consume_value(self, ctx, opts):
        """ Retrieve default value and display it when prompt is disabled. """
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
                if self.default is None and self.required:
                    metavar = ''
                    if self.type.name not in ['integer', 'text']:
                        metavar = self.make_metavar()
                    prompt = '%s %s' % (self.help, metavar)
                    gandi.echo(prompt)
        return value

    def handle_parse_result(self, ctx, opts, args):
        """ Save value for this option in configuration
        if key/value pair doesn't already exist.
        Or old value in config was deprecated
        it needs to be updated to the new value format
        but the value keeps the same "meaning"
        """
        gandi = ctx.obj
        needs_update = False
        value, args = click.Option.handle_parse_result(self, ctx, opts, args)

        if value is not None:
            previous_value = gandi.get(global_=True, key=self.name)
            if isinstance(self.type, GandiChoice):
                if value == previous_value:
                    needs_update = True
                value = self.type.convert_deprecated_value(value)
            if not previous_value or needs_update:
                gandi.configure(global_=True, key=self.name, val=value)
        opts[self.name] = value
        value, args = click.Option.handle_parse_result(self, ctx, opts, args)
        return value, args


def option(*param_decls, **attrs):
    """Attach an option to the command.

    All positional arguments are passed as parameter declarations
    to :class:`Option`, all keyword arguments are forwarded unchanged.
    This is equivalent to creating an :class:`Option` instance manually and
    attaching it to the :attr:`Command.params` list.
    """
    def decorator(f):
        _param_memo(f, GandiOption(param_decls, **attrs))
        return f
    return decorator

# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper, ensure=True)
