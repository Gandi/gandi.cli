# -*- coding: utf-8 -*-
""" Configuration handler class declaration. """

import os
import sys
import yaml
import os.path
from distutils.dir_util import mkpath

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

import click


class GandiConfig(object):

    """ Base class for yaml configuration.

    Manage
    - read/write configuration files/values
    - handle two scopes : global/local

    """

    _conffiles = {}
    home_config = os.environ.get('GANDI_CONFIG',
                                 '~/.config/gandi/config.yaml')
    local_config = '.gandi.config.yaml'

    apienvs = {
        'ote': 'https://rpc.ote.gandi.net/xmlrpc/',
        'production': 'https://rpc.gandi.net/xmlrpc/',
    }
    default_apienv = 'production'

    @classmethod
    def load_config(cls):
        """ Load global and local configuration files and update if needed."""
        config_file = os.path.expanduser(cls.home_config)
        global_conf = cls.load(config_file, 'global')
        cls.load(cls.local_config, 'local')
        # update global configuration if needed
        cls.update_config(config_file, global_conf)

    @classmethod
    def update_config(cls, config_file, config):
        """ Update configuration if needed. """
        need_save = False
        # delete old env key
        if 'api' in config and 'env' in config['api']:
            del config['api']['env']
            need_save = True
        # convert old ssh_key configuration entry
        ssh_key = config.get('ssh_key')
        sshkeys = config.get('sshkey')
        if ssh_key and not sshkeys:
            config.update({'sshkey': [ssh_key]})
            need_save = True
        elif ssh_key and sshkeys:
            config.update({'sshkey': sshkeys.append(ssh_key)})
            need_save = True
        # remove old value
        if ssh_key:
            del config['ssh_key']
            need_save = True

        # save to disk
        if need_save:
            cls.save(config_file, config)

    @classmethod
    def load(cls, filename, name=None):
        """ Load yaml configuration from filename. """
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
        """ Save configuration to yaml file. """
        mode = os.O_WRONLY | os.O_TRUNC | os.O_CREAT
        with os.fdopen(os.open(filename, mode, 0o600), 'w') as fname:
            yaml.safe_dump(config, fname, indent=4, default_flow_style=False)

    @classmethod
    def _del(cls, scope, key, separator='.', conf=None):
        orig_key = key

        key = key.split(separator)
        if not conf:
            conf = cls._conffiles.get(scope, {})

        if separator not in orig_key:
            if orig_key in conf:
                del conf[orig_key]
                return

        for k in key:
            if k not in conf:
                return
            else:
                cls._del(scope, separator.join([k1 for k1 in key if k1 != k]),
                         conf=conf[k])
                return

    @classmethod
    def delete(cls, global_, key):
        """ Delete key/value pair from configuration file. """
        # first retrieve current configuration
        scope = 'global' if global_ else 'local'
        config = cls._conffiles.get(scope, {})
        cls._del(scope, key)
        conf_file = cls.home_config if global_ else cls.local_config
        # save configuration to file
        cls.save(os.path.expanduser(conf_file), config)

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
    def get(cls, key, default=None, separator='.', global_=False):
        """ Retrieve a key value from loaded configuration.

        Order of search if global_=False:
        1/ environnment variables
        2/ local configuration
        3/ global configuration
        """
        # first check environnment variables
        # if we're not in global scope
        if not global_:
            ret = os.environ.get(key.upper().replace('.', '_'))
            if ret is not None:
                return ret

        # then check in local and global configuration unless global_=True
        scopes = ['global'] if global_ else ['local', 'global']
        for scope in scopes:
            ret = cls._get(scope, key, default, separator)
            if ret is not None:
                return ret

        if ret is None:
            return default

    @classmethod
    def configure(cls, global_, key, val):
        """ Update and save configuration value to file. """
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
    def list(cls, global_):
        """ Return configuration file content. """
        scope = 'global' if global_ else 'local'
        return cls._conffiles.get(scope, {})

    @classmethod
    def init_config(cls):
        """ Initialize Gandi CLI configuration.

        Create global configuration directory with API credentials

        """
        try:
            # first load current conf and only overwrite needed params
            # we don't want to reset everything
            config_file = os.path.expanduser(cls.home_config)
            config = cls.load(config_file, 'global')
            cls._del('global', 'api.env')

            apikey = click.prompt('Api key')
            env_choice = click.Choice(list(cls.apienvs.keys()))
            apienv = click.prompt('Environnment [production]/ote',
                                  default=cls.default_apienv,
                                  type=env_choice,
                                  show_default=False)
            sshkey = click.prompt('SSH keyfile',
                                  default='~/.ssh/id_rsa.pub')

            config.update({
                'api': {'key': apikey,
                        'host': cls.apienvs[apienv]},
            })

            if sshkey is not None:
                sshkey_file = os.path.expanduser(sshkey)
                if os.path.exists(sshkey_file):
                    config['sshkey'] = [sshkey_file]

            directory = os.path.expanduser(os.path.dirname(config_file))
            if not os.path.exists(directory):
                mkpath(directory, 0o700)

            # save to disk
            cls.save(config_file, config)
            # load in memory
            cls.load(config_file, 'global')
        except (KeyboardInterrupt, click.exceptions.Abort):
            cls.echo('Aborted.')
            sys.exit(1)
