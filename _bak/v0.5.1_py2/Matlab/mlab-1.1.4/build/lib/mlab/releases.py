'''
MLAB calls MATLAB funcitons and looks like a normal python library.

authors:
    Yauhen Yakimovich <eugeny.yakimovitch@gmail.com>

Module wrapping borrowed from `sh` project by Andrew Moffat.
'''
import os
import sys
from types import ModuleType
from mlabwrap import (MlabWrap, choose_release, find_available_releases,
                      MatlabReleaseNotFound)
import traceback


# TODO: work with ENV
#os.getenv("MLABRAW_CMD_STR", "")


def get_available_releases():
    return dict(find_available_releases())


def get_latest_release(available_releases=None):
    if not available_releases:
        available_releases = dict(find_available_releases())
    versions = available_releases.keys()
    latest_release_version = sorted(versions)[-1]
    return latest_release_version


class MatlabVersions(dict):

    def __init__(self, globs):
        self.globs = globs
        self.__selected_instance = None
        self._available_releases = dict(find_available_releases())

    def __setitem__(self, k, v):
        self.globs[k] = v

    def __getitem__(self, k):
        try: return self.globs[k]
        except KeyError: pass

        # the only way we'd get to here is if we've tried to
        # import * from a repl.  so, raise an exception, since
        # that's really the only sensible thing to do
        if k == "__all__":
            raise ImportError('Cannot import * from mlab. Please import mlab '
                              'or import versions individually.')

        if k.startswith("__") and k.endswith("__"):
            raise AttributeError

        # how about an return a function variable?
        # try: return os.environ[k]
        # except KeyError: pass

        # is it a "release version"?
        if k.startswith('R') and k in self._available_releases:
            self[k] = self.get_mlab_instance(k)
            return self[k]

        if k == 'latest_release':
            matlab_release = self.pick_latest_release()
            instance = self.get_mlab_instance(matlab_release)
            self[k] = instance
            self[matlab_release] = instance
            return instance

        if self.__selected_instance is not None:
            instance = self[self.__selected_instance]
            try:
                return getattr(instance, k)
            except AttributeError:
                traceback.print_exc(file=sys.stdout)
        else:
            raise ImportError('Import failed, no MATLAB instance selected. Try import mlab.latest_release')


        raise ImportError('Failed to import anything for: %s' % k)

    def get_mlab_instance(self, matlab_release):
        choose_release(matlab_release)
        instance = MlabWrap()
        # Make it a module
        sys.modules['mlab.releases.' + matlab_release] = instance
        sys.modules['matlab'] = instance
        return instance

    def pick_latest_release(self):
        return get_latest_release(self._available_releases)


# this is a thin wrapper around THIS module (we patch sys.modules[__name__]).
# this is in the case that the user does a "from sh import whatever"
# in other words, they only want to import certain programs, not the whole
# system PATH worth of commands.  in this case, we just proxy the
# import lookup to our MatlabVersions class
class SelfWrapper(ModuleType):
    def __init__(self, self_module):
        # this is super ugly to have to copy attributes like this,
        # but it seems to be the only way to make reload() behave
        # nicely.  if i make these attributes dynamic lookups in
        # __getattr__, reload sometimes chokes in weird ways...
        for attr in ["__builtins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr, None))
        # python 3.2 (2.7 and 3.3 work fine) breaks on osx (not ubuntu)
        # if we set this to None.  and 3.3 needs a value for __path__
        self.__path__ = []
        self.module = self_module
        self.instances = MatlabVersions(globals())

    def __setattr__(self, name, value):
        #if hasattr(self, "instances"): self.instances[name] = value
        ModuleType.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == "instances": raise AttributeError
        if name in dir(self.module):
            return getattr(self.module, name)

        return self.instances[name]

    # accept special keywords argument to define defaults for all operations
    # that will be processed with given by return SelfWrapper
    def __call__(self, **kwargs):
        return SelfWrapper(self.self_module, kwargs)



# we're being imported from somewhere
if __name__ != '__main__':
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrapper(self)
