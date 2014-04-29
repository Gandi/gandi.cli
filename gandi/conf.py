#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import socket
import os.path
import xmlrpclib

import click
from click.exceptions import UsageError


class GandiContextHelper(object):
    """ Gandi context helper

    Manage
    - reading configuration files
    - initializing xmlrpc connection
    - execute remote api calls

    """

    default_api_host = 'api-v3.dev.gandi.net'

    def __init__(self):
        """ initialize variables and api connection """
        try:
            config_file = os.path.expanduser("~/.config/gandi/gandirc")
            config = yaml.load(open(config_file))
        except Exception:
            config = self.configure()
        self.apikey = config.get('apikey')
        self.apihost = config.get('apihost')
        self.api = xmlrpclib.ServerProxy(self.apihost)

    @classmethod
    def configure(cls):
        print ("This is your first time running GandiCLI, let's configure "
               "a few things")
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

        config_file = os.path.expanduser("~/.config/gandi/gandirc")
        yaml.dump(config, open(config_file, "w"), default_flow_style=False)

        return config

    def call(self, method, args):
        """ call a remote api method and returned the result """
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
