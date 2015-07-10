import logging
import importlib

log = logging.getLogger(__name__)


class Api(object):

    _calls = {}

    def request(self, method, apikey, *args, **kwargs):
        log.info('Calling %s%r' % (method, args))
        modname, func = method.split('.', 1)
        modname = 'gandi.cli.tests.fixtures._' + modname
        module = importlib.import_module(modname)
        func = func.replace('.', '_')
        try:
            self._calls.setdefault(method, []).append(args)
            return getattr(module, func)(*args)
        except Exception as exc:
            log.exception('Unexpected Exception %s while calling %s' % (exc,
                                                                        method)
                          )
