#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import os.path

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

import click


class GandiConfig(object):
    """ Base class for yaml configuration

    Manage
    - read/write configuration files/values
    - handle two scopes : global/local

    """

    _conffiles = {}
    home_config = '~/.config/gandi/config.yaml'
    local_config = '.gandi.config.yaml'

    apienvs = {
        'dev': 'http://api-v3.dev.gandi.net/',
        'ote': 'https://rpc.ote.gandi.net/xmlrpc/',
        'production': 'https://rpc.gandi.net/xmlrpc/',
    }
    default_apienv = 'production'

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
            return {}
        name = name or filename

        if name not in cls._conffiles:
            with open(filename) as fdesc:
                content = yaml.load(fdesc, YAMLLoader)
                # in case the file is empty
                if content is None:
                    content = {}
                cls._conffiles[name] = content

        return cls._conffiles[name]

    @classmethod
    def save(cls, filename, config):
        """ Save configuration to yaml file """
        yaml.safe_dump(config, open(filename, "w"), indent=4,
                       default_flow_style=False)

    @classmethod
    def _set(cls, scope, key, val, separator='.'):
        orig_key = key

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
        if not value:
            return default

        try:
            for k in key:
                value = value[k]
            return value
        except KeyError:
            return default

    @classmethod
    def get(cls, key, default=None, separator='.'):
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
            return default

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
        try:
            apikey = click.prompt('Api key')
            env_choice = click.Choice(cls.apienvs.keys())
            apienv = click.prompt('Environnment',
                                  default=cls.default_apienv,
                                  type=env_choice)
            ssh_key = click.prompt('SSH keyfile',
                                   default='~/.ssh/id_rsa.pub')

            config = {
                'api': {'key': apikey,
                        'env': apienv,
                        'host': cls.apienvs[apienv]},
            }
            if ssh_key is not None:
                config['ssh_key'] = os.path.expanduser(ssh_key)

            directory = os.path.expanduser("~/.config/gandi")
            if not os.path.exists(directory):
                os.mkdir(directory, 0755)

            config_file = os.path.expanduser(cls.home_config)
            # save to disk
            cls.save(config_file, config)
            # load in memory
            cls.load(config_file, 'global')
        except KeyboardInterrupt:
            cls.echo('Aborted.')
            sys.exit(1)
