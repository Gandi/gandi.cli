#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import socket
import os.path
import logging
import xmlrpclib

import click

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class GandiContextHelper(object):
    """ Gandi context helper

    Manage reading configuration files and initializing xml rpc connection
    """

    def __init__(self):
        # initialize variables and api connection
        try:
            config_file = os.path.expanduser("~/.config/gandi/gandirc")
            config = yaml.load(open(config_file))
        except Exception:
            config = self.configure()
        self.apikey = config.get('apikey')
        self.apihost = config.get('apihost')
        self.api = xmlrpclib.ServerProxy(self.apihost)

        log.debug('apikey found: %r' % self.apikey)

    @classmethod
    def configure(cls):
        print ("This is your first time running GandiCLI, let's configure "
               "a few things")
        apikey = raw_input("Api key: ")

        config = {
            'apikey': apikey,
            'apihost': 'http://10.55.32.116:8083',
        }

        directory = os.path.expanduser("~/.config/gandi")
        if not os.path.exists(directory):
            os.mkdir(directory, 0755)

        config_file = os.path.expanduser("~/.config/gandi/gandirc")
        yaml.dump(config, open(config_file, "w"), default_flow_style=False)

        return config

    def call(self, method, args):

        try:
            func = getattr(self.api, method)
            return func(self.apikey, *args)
            #return self.api.vm.list(gandi.apikey, options)
        except socket.error:
            log.error('Gandi API service is unreachable')
            return
        except xmlrpclib.Fault as err:
            log.error('Gandi API has returned an error %s' % err)
            return


# create a decorator to pass the Gandi object as context to click calls
pass_gandi = click.make_pass_decorator(GandiContextHelper)


