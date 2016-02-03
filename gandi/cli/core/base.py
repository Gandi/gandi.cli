# -*- coding: utf-8 -*-
""" Contains GandiModule and GandiContextHelper classes.

GandiModule class is used by commands modules.
GandiContextHelper class is used as click context for commands.
"""

from __future__ import print_function
import os
import sys
import time
import os.path
from datetime import datetime
from subprocess import check_call, Popen, PIPE, CalledProcessError

import click
from click.exceptions import UsageError

from .client import XMLRPCClient, APICallFailed, DryRunException, JsonClient
from .conf import GandiConfig


class MissingConfiguration(Exception):

    """ Raise when no configuration was found. """


class GandiModule(GandiConfig):

    """ Base class for modules.

    Manage
    - initializing xmlrpc connection
    - execute remote api calls
    """

    _op_scores = {'BILL': 0, 'WAIT': 1, 'RUN': 2, 'DONE': 3}

    verbose = 0
    _api = None
    # frequency of api calls when polling for operation progress
    _poll_freq = 1

    @classmethod
    def get_api_connector(cls):
        """ Initialize an api connector for future use."""
        if cls._api is None:
            cls.load_config()
            cls.debug('initialize connection to remote server')
            apihost = cls.get('api.host')
            if not apihost:
                raise MissingConfiguration()

            apienv = cls.get('api.env')
            if apienv and apienv in cls.apienvs:
                apihost = cls.apienvs[apienv]

            cls._api = XMLRPCClient(host=apihost, debug=cls.verbose)

        return cls._api

    @classmethod
    def call(cls, method, *args, **kwargs):
        """ Call a remote api method and return the result."""
        api = None
        empty_key = kwargs.pop('empty_key', False)
        try:
            api = cls.get_api_connector()
            apikey = cls.get('api.key')
            if not apikey and not empty_key:
                cls.echo("No apikey found, please use 'gandi setup' "
                         "command")
                sys.exit(1)
        except MissingConfiguration:
            if api and empty_key:
                apikey = ''
            elif not kwargs.get('safe'):
                cls.echo("No configuration found, please use 'gandi setup' "
                         "command")
                sys.exit(1)
            else:
                return []

        # make the call
        cls.debug('calling method: %s' % method)
        for arg in args:
            cls.debug('with params: %r' % arg)
        try:
            return api.request(method, apikey, *args,
                               **{'dry_run': kwargs.get('dry_run', False),
                                  'return_dry_run':
                                  kwargs.get('return_dry_run', False)})
        except APICallFailed as err:
            if kwargs.get('safe'):
                return []
            if err.code == 530040:
                cls.echo("Error: It appears you haven't purchased any credits "
                         "yet.\n"
                         "Please visit https://www.gandi.net/credit/buy to "
                         "learn more and buy credits.")
                sys.exit(1)
            if err.code == 510150:
                cls.echo("Invalid API key, please use 'gandi setup' command.")
                sys.exit(1)
            if isinstance(err, DryRunException):
                if kwargs.get('return_dry_run', False):
                    return err.dry_run
                else:
                    for msg in err.dry_run:
                        # TODO use trads with %s
                        cls.echo(msg['reason'])
                        cls.echo('\t' + ' '.join(msg['attr']))
                    sys.exit(1)
            error = UsageError(err.errors)
            setattr(error, 'code', err.code)
            raise error

    @classmethod
    def safe_call(cls, method, *args):
        """ Call a remote api method but don't raise if an error occurred."""
        return cls.call(method, *args, safe=True)

    @classmethod
    def json_call(cls, url):
        """ Call a remote api using json format """
        # make the call
        cls.debug('calling url: %s' % url)
        try:
            return JsonClient.request(url)
        except APICallFailed as err:
            cls.echo('An error occured during call: %s' % err.errors)
            sys.exit(1)

    @classmethod
    def intty(cls):
        """ Check if we are in a tty. """
        # XXX: temporary hack until we can detect if we are in a pipe or not
        return True

        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            return True

        return False

    @classmethod
    def echo(cls, message):
        """ Display message. """
        if cls.intty():
            if message is not None:
                print(message)

    @classmethod
    def pretty_echo(cls, message):
        """ Display message using pretty print formatting. """
        if cls.intty():
            if message:
                from pprint import pprint
                pprint(message)

    @classmethod
    def separator_line(cls, sep='-', size=10):
        """ Display a separator line. """
        if cls.intty():
            cls.echo(sep * size)

    @classmethod
    def separator_sub_line(cls, sep='-', size=10):
        """ Display a separator line. """
        if cls.intty():
            cls.echo("\t" + sep * size)

    @classmethod
    def debug(cls, message):
        """ Display debug message if verbose level allows it. """
        if cls.verbose > 1:
            msg = '[DEBUG] %s' % message
            cls.echo(msg)

    @classmethod
    def log(cls, message):
        """ Display info message if verbose level allows it. """
        if cls.verbose > 0:
            msg = '[INFO] %s' % message
            cls.echo(msg)

    @classmethod
    def deprecated(cls, message):
        print('[deprecated]: %s' % message, file=sys.stderr)

    @classmethod
    def error(cls, msg):
        """ Raise click UsageError exception using msg. """
        raise UsageError(msg)

    @classmethod
    def execute(cls, command, shell=True):
        """ Execute a shell command. """
        cls.debug('execute command (shell flag:%r): %r ' % (shell, command))
        try:
            check_call(command, shell=shell)
            return True
        except CalledProcessError:
            return False

    @classmethod
    def exec_output(cls, command, shell=True, encoding='utf-8'):
        """ Return execution output

        :param encoding: charset used to decode the stdout
        :type encoding: str

        :return: the return of the command
        :rtype: unicode string
        """
        proc = Popen(command, shell=shell, stdout=PIPE)
        stdout, _stderr = proc.communicate()
        if proc.returncode == 0:
            return stdout.decode(encoding)

        return ''

    @classmethod
    def update_progress(cls, progress, starttime):
        """ Display an ascii progress bar while processing operation. """
        width, _height = click.get_terminal_size()
        if not width:
            return

        duration = datetime.utcnow() - starttime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        size = int(width * .6)
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = 'error: progress var must be float\n'
            cls.echo(type(progress))
        if progress < 0:
            progress = 0
            status = 'Halt...\n'
        if progress >= 1:
            progress = 1
            # status = 'Done...\n'
        block = int(round(size * progress))
        text = ('\rProgress: [{0}] {1:.2%} {2} {3:0>2}:{4:0>2}:{5:0>2}  '
                ''.format('#' * block + '-' * (size - block), progress,
                          status, hours, minutes, seconds))
        sys.stdout.write(text)
        sys.stdout.flush()

    @classmethod
    def display_progress(cls, operations):
        """ Display progress of Gandi operations.

        polls API every 1 seconds to retrieve status.
        """
        start_crea = datetime.utcnow()

        # count number of operations, 3 steps per operation
        if not isinstance(operations, (list, tuple)):
            operations = [operations]
        count_operations = len(operations) * 3
        updating_done = False
        while not updating_done:
            op_score = 0
            for oper in operations:
                op_ret = cls.call('operation.info', oper['id'])
                op_step = op_ret['step']
                if op_step in cls._op_scores:
                    op_score += cls._op_scores[op_step]
                else:
                    cls.echo('')
                    msg = 'step %s unknown, exiting' % op_step
                    if op_step == 'ERROR':
                        msg = ('An error has occured during operation '
                               'processing: %s' % op_ret['last_error'])
                    elif op_step == 'SUPPORT':
                        msg = ('An error has occured during operation '
                               'processing, you must contact Gandi support.')
                    cls.echo(msg)
                    sys.exit(1)

            cls.update_progress(float(op_score) / count_operations,
                                start_crea)

            if op_score == count_operations:
                updating_done = True

            time.sleep(cls._poll_freq)

        cls.echo('\r')


class GandiContextHelper(GandiModule):

    """ Gandi context helper.

    Import module classes from modules directory upon initialization.
    """

    _modules = {}

    def __init__(self, verbose=-1):
        """ Initialize variables and api connection. """
        GandiModule.verbose = verbose
        GandiModule.load_config()
        # only load modules once
        if not self._modules:
            self.load_modules()

    def __getattribute__(self, item):
        """ Return module from internal imported modules dict. """
        if item in object.__getattribute__(self, '_modules'):
            return object.__getattribute__(self, '_modules')[item]
        return object.__getattribute__(self, item)

    def load_modules(self):
        """ Import CLI commands modules. """
        module_folder = os.path.join(os.path.dirname(__file__),
                                     '..', 'modules')
        module_dirs = {
            'gandi.cli': module_folder
        }

        if 'GANDICLI_PATH' in os.environ:
            for _path in os.environ.get('GANDICLI_PATH').split(':'):
                # remove trailing separator if any
                path = _path.rstrip(os.sep)
                module_dirs[os.path.basename(path)] = os.path.join(path,
                                                                   'modules')

        for module_basename, dir in list(module_dirs.items()):
            for filename in sorted(os.listdir(dir)):
                if filename.endswith('.py') and '__init__' not in filename:
                    submod = filename[:-3]
                    module_name = module_basename + '.modules.' + submod
                    __import__(module_name, fromlist=[module_name])

        # save internal map of loaded module classes
        for subclass in GandiModule.__subclasses__():
            self._modules[subclass.__name__.lower()] = subclass
