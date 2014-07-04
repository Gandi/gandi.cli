# -*- coding: utf-8 -*-
import os
import sys
import time
import os.path
from datetime import datetime
from subprocess import call

import click
from click.exceptions import UsageError

from .client import XMLRPCClient, APICallFailed
from .conf import GandiConfig


class GandiModule(GandiConfig):
    """ Base class for modules

    Manage
    - initializing xmlrpc connection
    - execute remote api calls

    """
    _op_scores = {'BILL': 0, 'WAIT': 1, 'RUN': 2, 'DONE': 3}

    verbose = False
    _api = None

    @classmethod
    def get_api_connector(cls):
        """ initialize an api connector for future use"""
        if cls._api is None:
            cls.load_config()
            cls.debug('initialize connection to remote server')
            apihost = cls.get('api.host')
            if not apihost:
                cls.echo("Welcome to GandiCLI, let's configure a few things "
                         "before we start")
                cls.init_config()
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
        # XXX: temporary hack until we can detect if we are in a pipe or not
        return True

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
    def separator_line(cls, sep='-', size=10):
        if cls.intty():
            cls.echo(sep * size)

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
        """ Display progress of Gandi operations

        polls API every 1 seconds to retrieve status
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
                op_step = cls.call('operation.info', oper['id'])['step']
                if op_step in cls._op_scores:
                    op_score += cls._op_scores[op_step]
                else:
                    msg = 'step %s unknown, exiting creation' % op_step
                    cls.error(msg)

            cls.update_progress(float(op_score) / count_operations,
                                start_crea)

            if op_score == count_operations:
                updating_done = True

            time.sleep(1)

        cls.echo('\r')


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

    def load_modules(self):
        module_folder = os.path.join(os.path.dirname(__file__), '../modules')
        for filename in os.listdir(module_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = 'gandi.cli.modules.' + submod
                __import__(module_name, fromlist=[module_name])

        # save internal map of loaded module classes
        for subclass in GandiModule.__subclasses__():
            self._modules[subclass.__name__.lower()] = subclass
