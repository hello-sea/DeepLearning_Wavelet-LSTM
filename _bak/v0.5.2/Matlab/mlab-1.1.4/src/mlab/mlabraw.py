#!/usr/bin/env python
'''
A quick and a bit less dirty hack to wrap matlabpipe/matlabcom as if they
were mlabraw.

Author: Dani Valevski <daniva@gmail.com>
        Yauhen Yakimovich <eugeny.yakimovitch@gmail.com>

License: MIT
'''
import platform
is_win = platform.system() == 'Windows'
if is_win:
    from matlabcom import MatlabCom as MatlabConnection
    from matlabcom import MatlabError as error
    from matlabcom import discover_location, find_available_releases
    from matlabcom import WindowsMatlabReleaseNotFound as MatlabReleaseNotFound
else:
    from matlabpipe import MatlabPipe as MatlabConnection
    from matlabpipe import MatlabError as error
    from matlabpipe import discover_location, find_available_releases
    from matlabpipe import UnixMatlabReleaseNotFound as MatlabReleaseNotFound
try:
    import settings
except ImportError:
    class settings:
        MATLAB_PATH = 'guess'
import traceback


_MATLAB_RELEASE='latest'


def set_release(matlab_release):
    global _MATLAB_RELEASE
    _MATLAB_RELEASE=matlab_release


def open():
    global _MATLAB_RELEASE
    '''Opens MATLAB using specified connection (or DCOM+ protocol on Windows)where matlab_location  '''
    if is_win:
        ret = MatlabConnection()
        ret.open()
        return ret
    else:
        if settings.MATLAB_PATH != 'guess':
            matlab_path = settings.MATLAB_PATH + '/bin/matlab'
        elif _MATLAB_RELEASE != 'latest':
            matlab_path = discover_location(_MATLAB_RELEASE)
        else:
            # Latest release is found in __init__.by, i.e. higher logical level
            raise MatlabReleaseNotFound('Please select a matlab release or set its location.')
        try:
            ret = MatlabConnection(matlab_path)
            ret.open()
        except Exception:
            #traceback.print_exc(file=sys.stderr)
            raise MatlabReleaseNotFound('Could not open matlab, is it in %s?' % matlab_path)
        return ret

def close(matlab):
    matlab.close()

def eval(matlab, exp, log=False):
    if log or is_win:
        matlab.eval(exp)
    else:
        matlab.eval(exp, print_expression=False, on_new_output=None)
    return ''

def get(matlab, var_name):
    return matlab.get(var_name)

def put(matlab, var_name, val):
    matlab.put({var_name : val})
