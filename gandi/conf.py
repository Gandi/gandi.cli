#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import socket
import os.path
import xmlrpclib

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

import click
from click.exceptions import UsageError


class GandiContextHelper(object):
    """ Gandi context helper

    Manage
    - reading configuration files
    - initializing xmlrpc connection
    - execute remote api calls

    """

    _conffiles = {}
    default_api_host = 'api-v3.dev.gandi.net'
    home_config = '~/.config/gandi/gandirc'
    local_config = '.gandirc'

    def __init__(self):
        """ initialize variables and api connection """
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

    def call(self, method, *args):
        """ call a remote api method and returned the result """
        print 'calling method:', method
        print 'with params:', args
        try:
            func = getattr(self.api, method)
            return func(self.apikey, *args)
        except socket.error:
            msg = 'Gandi API service is unreachable'
            raise UsageError(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error %s' % err
            raise UsageError(msg)


# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper)
