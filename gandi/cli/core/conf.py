#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import os.path
from datetime import datetime
from subprocess import call

from .client import XMLRPCClient, APICallFailed
from .utils import MissingConfiguration

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

import click
from click.exceptions import UsageError


class GandiModule(object):
    """ Base class for modules

    Manage
    - reading configuration files
    - initializing xmlrpc connection
    - execute remote api calls

    """

    _conffiles = {}
    default_api_host = 'http://api-v3.dev.gandi.net'
    home_config = '~/.config/gandi/config.yaml'
    local_config = '.gandi.config.yaml'

    verbose = False
    apikey = None
    apihost = None
    _api = None

    @classmethod
    def load_config(cls):
        """ Load global and local configuration files or initialize if needed
        """
        config_file = os.path.expanduser(cls.home_config)
        cls.load(config_file, 'global')
        cls.load(cls.local_config, 'local')

    @classmethod
    def load(cls, filename, name=None):
        """ Load yaml configuration from filename """
        if not os.path.exists(filename):
            return
        name = name or filename

        if name not in cls._conffiles:
            cls.debug('loading %s configuration' % name)
            with open(filename) as fdesc:
                cls._conffiles[name] = yaml.load(fdesc, YAMLLoader)

        return cls._conffiles[name]

    @classmethod
    def save(cls, filename, config):
        """ Save configuration to yaml file """
        yaml.safe_dump(config, open(filename, "w"), indent=4,
                       default_flow_style=False)

    @classmethod
    def configure(cls, global_, key, val):
        # first retrieve current configuration
        scope = 'global' if global_ else 'local'
        if scope not in cls._conffiles:
            cls._conffiles[scope] = {}
        config = cls._conffiles.get(scope, {})
        # apply modification to fields
        cls._set(scope, key, val)
        conf_file = cls.home_config if global_ else cls.local_config
        # save configuration to file
        cls.save(os.path.expanduser(conf_file), config)

    @classmethod
    def init_config(cls):
        """ Initialize Gandi CLI configuration

        Create global configuration directory with API credentials

        """
        apikey = raw_input("Api key: ")
        apihost = (raw_input("Api host[%s]: " % cls.default_api_host)
                   or cls.default_api_host)

        config = {
            'api': {'key': apikey,
                    'host': apihost},
        }

        directory = os.path.expanduser("~/.config/gandi")
        if not os.path.exists(directory):
            os.mkdir(directory, 0755)

        config_file = os.path.expanduser(cls.home_config)
        # save to disk
        cls.save(config_file, config)
        # load in memory
        cls.load(config_file, 'global')

    @classmethod
    def _set(cls, scope, key, val, separator='.'):
        orig_key = key

        cls.debug("saving key '%s' with value '%s' to scope %s" %
                 (key, val, scope))
        key = key.split(separator)
        value = cls._conffiles.get(scope, {})
        if separator not in orig_key:
            value[orig_key] = val
            return

        for k in key:
            if k not in value:
                value[k] = {}
                last_val = value
                value = value[k]
            else:
                last_val = value
                value = value[k]
        last_val[k] = val

    @classmethod
    def _get(cls, scope, key, default=None, separator='.'):
        key = key.split(separator)
        value = cls._conffiles.get(scope, {})
        try:
            for k in key:
                value = value[k]
            return value
        except KeyError:
            return default

    @classmethod
    def get(cls, key, default=None, separator='.', mandatory=True):
        """ Retrieve a key value from loaded configuration

        Order of search :
        1/ environnment variables
        2/ local configuration
        3/ global configuration
        """
        # first check environnment variables
        ret = os.environ.get(key.upper())
        if ret is not None:
            return ret

        # then check in local -> global configuration
        for scope in ['local', 'global']:
            ret = cls._get(scope, key, default, separator)
            if ret is not None:
                return ret

        if ret is None:
            if mandatory:
                raise UsageError('missing configuration value for %s' % key)
            return default

    @classmethod
    def get_api_connector(cls):
        """ initialize an api connector for future use"""
        if cls._api is None:
            cls.load_config()
            cls.debug('initialize connection to remote server')
            apihost = cls.get('api.host')
            cls._api = XMLRPCClient(host=apihost, debug=cls.verbose)

        return cls._api

    @classmethod
    def call(cls, method, *args):
        """ call a remote api method and return the result """
        api = cls.get_api_connector()
        apikey = cls.get('api.key')

        # make the call
        cls.debug('calling method: %s' % method)
        for arg in args:
            cls.debug('with params: %r' % arg)
        try:
            return api.request(apikey, method, *args)
        except APICallFailed as err:
            raise UsageError(err.errors)

    @classmethod
    def intty(cls):
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            return True

        return False

    @classmethod
    def echo(cls, message):
        if cls.intty():
            if message:
                print message

    @classmethod
    def pretty_echo(cls, message):
        if cls.intty():
            if message:
                from pprint import pprint
                pprint(message)

    @classmethod
    def debug(cls, message):
        if cls.verbose:
            msg = '[DEBUG] %s' % message
            cls.echo(msg)

    @classmethod
    def error(cls, msg):
        raise UsageError(msg)

    @classmethod
    def shell(cls, command):
        cls.debug(command)
        call(command, shell=True)

    @classmethod
    def update_progress(cls, progress, starttime):
        width, _height = click.get_terminal_size()
        if not width:
            return

        duration = datetime.utcnow() - starttime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        size = int(width * .7)
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = 'error: progress var must be float\r\n'
            cls.echo(type(progress))
        if progress < 0:
            progress = 0
            status = 'Halt...\r\n'
        if progress >= 1:
            progress = 1
            # status = 'Done...\r\n'
        block = int(round(size * progress))
        text = ('\rProgress: [{0}] {1:.2%}  {2}  {3:0>2}:{4:0>2}:{5:0>2}  '
                ''.format('#' * block + '-' * (size - block), progress,
                          status, hours, minutes, seconds))
        sys.stdout.write(text)
        sys.stdout.flush()


class GandiContextHelper(GandiModule):
    """ Gandi context helper

    Load module classes from modules directory at start
    """

    _modules = {}

    def __init__(self, verbose=False):
        """ initialize variables and api connection """
        GandiModule.verbose = verbose
        GandiModule.load_config()
        self.load_modules()

    def __getattribute__(self, item):
        if item in object.__getattribute__(self, '_modules'):
            return object.__getattribute__(self, '_modules')[item]
        return object.__getattribute__(self, item)

    @classmethod
    def load_modules(cls):
        module_folder = os.path.join(os.path.dirname(__file__), '../modules')
        for filename in os.listdir(module_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = 'gandi.cli.modules.' + submod
                __import__(module_name, fromlist=[module_name])

        # save internal map of loaded module classes
        for subclass in GandiModule.__subclasses__():
            cls._modules[subclass.__name__.lower()] = subclass

# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper)
