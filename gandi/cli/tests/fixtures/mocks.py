from __future__ import print_function
from datetime import datetime


class MockObject(object):

    @classmethod
    def blank_func(cls, *args, **kwargs):
        pass

    @classmethod
    def execute(cls, command, shell=True):
        """ Execute a shell command. """
        if not shell:
            print(' '.join(command))
        else:
            print(command)
        return True

    @classmethod
    def exec_output(cls, command, shell=True, encoding='utf-8'):
        """ Return execution output

        :param encoding: charset used to decode the stdout
        :type encoding: str

        :return: the return of the command
        :rtype: unicode string
        """
        if not shell:
            return ' '.join(command)
        return command

    @classmethod
    def now(cls, *args, **kwargs):
        return datetime(2020, 12, 25, 0, 0, 0)

    @classmethod
    def deprecated(cls, message):
        pass
