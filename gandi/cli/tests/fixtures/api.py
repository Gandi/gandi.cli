import logging
import importlib

log = logging.getLogger(__name__)


class Api(object):

    _calls = {}

    def request(self, method, apikey, *args, **kwargs):
        log.info('Calling %s%r %r' % (method, args, kwargs))
        modname, func = method.split('.', 1)
        modname = 'gandi.cli.tests.fixtures._' + modname
        module = importlib.import_module(modname)
        func = func.replace('.', '_')
        if (kwargs.get('dry_run', False)
                and kwargs.get('return_dry_run', False)):
            func = func + '_dry_run'
        try:
            self._calls.setdefault(method, []).append(args)
            return getattr(module, func)(*args)
        except Exception as exc:
            log.exception('Unexpected Exception %s while calling %s' % (exc,
                                                                        method)
                          )
