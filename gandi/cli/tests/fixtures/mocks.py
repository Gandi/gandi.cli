
class MockObject(object):

    @classmethod
    def blank_func(cls, *args, **kwargs):
        pass

    @classmethod
    def execute(cls, command, shell=True):
        """ Execute a shell command. """
        print command
        return True
