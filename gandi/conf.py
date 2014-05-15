#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import socket
import os.path
import xmlrpclib
from datetime import datetime
from subprocess import call

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

import click
from click.exceptions import UsageError


class GandiPlugin(object):
    """ Base class for plugins

    Manage
    - reading configuration files
    - initializing xmlrpc connection
    - execute remote api calls

    """

    _conffiles = {}
    default_api_host = 'api-v3.dev.gandi.net'
    home_config = '~/.config/gandi/gandirc'
    local_config = '.gandirc'

    verbose = False
    api = None

    def __init__(self, verbose=False):
        """ initialize variables and api connection """
        self.verbose = verbose
        config_file = os.path.expanduser(self.home_config)
        config = self.load(config_file, 'global')
        self.load(self.local_config, 'local')
        if not config:
            print ("This is your first time running GandiCLI, let's configure "
                   "a few things")
            config = self.init_config()

        self.apikey = config.get('apikey')
        self.apihost = config.get('apihost')
        self.api = xmlrpclib.ServerProxy(self.apihost)

    def call(self, method, *args):
        """ call a remote api method and returned the result """
        self.echo('calling method: %s' % method)
        for arg in args:
            self.echo('with params: %r' % arg)
        try:
            func = getattr(self.api, method)
            return func(self.apikey, *args)
        except socket.error:
            msg = 'Gandi API service is unreachable'
            raise UsageError(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error %s' % err
            raise UsageError(msg)

    def echo(self, message):
        if self.verbose:
            print >> sys.stdout, message

    def error(self, msg):
        raise UsageError(msg)

    @classmethod
    def load(cls, filename, name=None):
        if not os.path.exists(filename):
            return
        name = name or filename

        if name not in cls._conffiles:
            with open(filename) as fdesc:
                cls._conffiles[name] = yaml.load(fdesc, YAMLLoader)

        return cls._conffiles[name]

    @classmethod
    def save(cls, filename, config):
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
        apikey = raw_input("Api key: ")
        apihost = (raw_input("Api host[%s]: " % cls.default_api_host)
                   or cls.default_api_host)

        config = {
            'apikey': apikey,
            'apihost': 'http://%s' % apihost,
        }

        directory = os.path.expanduser("~/.config/gandi")
        if not os.path.exists(directory):
            os.mkdir(directory, 0755)

        config_file = os.path.expanduser(cls.home_config)
        cls.save(config_file, config)
        config = cls.load(config_file, 'global')

        return config

    @classmethod
    def _set(cls, scope, key, val, separator='.'):
        orig_key = key

        key = key.split(separator)
        value = cls._conffiles[scope]
        if separator not in orig_key:
            value[orig_key] = val
        else:
            for k in key:
                if k not in value:
                    value[k] = {}
                    last_val = value
                    value = value[k]
            last_val[k] = val

    def _get(self, scope, key, default=None, separator='.'):
        key = key.split(separator)
        value = self._conffiles[scope]
        try:
            for k in key:
                value = value[k]
            return value
        except KeyError:
            return default

    def get(self, key, default=None, separator='.'):
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
            ret = self._get(scope, key, default, separator)
            if ret is not None:
                return ret

        if ret is None:
            return default

    def shell(self, command):
        self.echo(command)
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
            print type(progress)
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


class GandiContextHelper(GandiPlugin):
    """ Gandi context helper

    Load plugin classes from plugin directory at start
    """

    _plugins = {}

    def __init__(self, verbose=False):
        """ initialize variables and api connection """
        GandiPlugin.__init__(self, verbose)
        self.load_plugins()

    def __getattribute__(self, item):
        if item in object.__getattribute__(self, '_plugins'):
            return object.__getattribute__(self, '_plugins')[item]()
        return object.__getattribute__(self, item)

    @classmethod
    def load_plugins(cls):
        plugin_folder = os.path.join(os.path.dirname(__file__), 'plugins')
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = __package__ + '.plugins.' + submod
                __import__(module_name, fromlist=[module_name])

        # save internal map of loaded plugin classes
        for subclass in GandiPlugin.__subclasses__():
            cls._plugins[subclass.__name__.lower()] = subclass

# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper)
