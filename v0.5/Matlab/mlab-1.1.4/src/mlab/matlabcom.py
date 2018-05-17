#!/usr/bin/env python

""" A python module for raw communication with Matlab(TM) using COM client
 under windows.

The module sends commands to the matlab process as a COM client. This is only
supported under windows.

Author: Dani Valevski <daniva@gmail.com>
        Yauhen Yakimovich <eugeny.yakimovitch@gmail.com>

Dependencies: pywin32, numpy
Tested Matlab Versions: 2011a
License: MIT
"""

import numpy as np
try:
  import win32com.client
except:
  print 'win32com in missing, please install it'
  raise

def find_available_releases():
    # report we have all versions
    return [('R%d%s' % (y,v), '')
        for y in range(2006,2015) for v in ('a','b')]

def discover_location(matlab_release):
    pass

class WindowsMatlabReleaseNotFound(Exception):
    '''Raised if specified release was not found.'''

class MatlabError(Exception):
  """Raised when a Matlab evaluation results in an error inside Matlab."""
  pass

class MatlabConnectionError(Exception):
  """Raised for errors related to the Matlab connection."""
  pass

class MatlabCom(object):
  """ Manages a matlab COM client.

  The process can be opened and close with the open/close methods.
  To send a command to the matlab shell use 'eval'.
  To load numpy data to the matlab shell use 'put'.
  To retrieve numpy data from the matlab shell use 'get'.
  """
  def __init__(self, matlab_process_path=None, matlab_version=None):
    self.client = None

  def open(self, visible=False):
    """ Dispatches the matlab COM client.

    Note: If this method fails, try running matlab with the -regserver flag.
    """
    if self.client:
      raise MatlabConnectionError('Matlab(TM) COM client is still active. Use close to '
                      'close it')
    self.client = win32com.client.Dispatch('matlab.application')
    self.client.visible = visible

  def close(self):
    """ Closes the matlab COM client.
    """
    self._check_open()
    try:
      pass    #self.eval('quit();')
    except:
      pass
    del self.client

  def eval(self, expression, identify_erros=True):
    """ Evaluates a matlab expression synchronously.

    If identify_erros is true, and the last output line after evaluating the
    expressions begins with '???' an excpetion is thrown with the matlab error
    following the '???'.
    The return value of the function is the matlab output following the call.
    """
    #print expression
    self._check_open()
    ret = self.client.Execute(expression)
    #print ret
    if identify_erros and ret.rfind('???') != -1:
      begin = ret.rfind('???') + 4
      end = ret.find('\n', begin)
      raise MatlabError(ret[begin:end])
    return ret

  def get(self, names_to_get, convert_to_numpy=True):
    """ Loads the requested variables from the matlab com client.

    names_to_get can be either a variable name or a list of variable names.
    If it is a variable name, the values is returned.
    If it is a list, a dictionary of variable_name -> value is returned.

    If convert_to_numpy is true, the method will all array values to numpy
    arrays. Scalars are left as regular python objects.

    """
    self._check_open()
    single_itme = isinstance(names_to_get, (unicode, str))
    if single_itme:
      names_to_get = [names_to_get]
    ret = {}
    for name in names_to_get:
      ret[name] = self.client.GetWorkspaceData(name, 'base')
      # TODO(daniv): Do we really want to reduce dimensions like that? what if this a row vector?
      while isinstance(ret[name], (tuple, list)) and len(ret[name]) == 1:
        ret[name] = ret[name][0]
      if convert_to_numpy and isinstance(ret[name], (tuple, list)):
        ret[name] = np.array(ret[name])
    if single_itme:
      return ret.values()[0]
    return ret

  def put(self, name_to_val):
    """ Loads a dictionary of variable names into the matlab com client.
    """
    self._check_open()
    for name, val in name_to_val.iteritems():
      # First try to put data as a matrix:
      try:
        self.client.PutFullMatrix(name, 'base', val, None)
      except:
        self.client.PutWorkspaceData(name, 'base', val)

  def _check_open(self):
    if not self.client:
      raise MatlabConnectionError('Matlab(TM) process is not active.')

if __name__ == '__main__':
  import unittest


  class TestMatlabCom(unittest.TestCase):
    def setUp(self):
      self.matlab = MatlabCom()
      self.matlab.open()

    def tearDown(self):
      self.matlab.close()

    def test_eval(self):
      for i in xrange(100):
        ret = self.matlab.eval('disp \'hiush world%s\';' % ('b'*i))
        self.assertTrue('hiush world' in ret)

    def test_put(self):
      self.matlab.put({'A' : [1, 2, 3]})
      ret = self.matlab.eval('A')
      self.assertTrue('A =' in ret)

    def test_1_element(self):
      self.matlab.put({'X': 'string'})
      ret = self.matlab.get('X')
      self.assertEquals(ret, 'string')

    def test_get(self):
      self.matlab.eval('A = [1 2 3];')
      ret = self.matlab.get('A')
      self.assertEquals(ret[0], 1)
      self.assertEquals(ret[1], 2)
      self.assertEquals(ret[2], 3)

    def test_error(self):
      self.assertRaises(MatlabError,
                        self.matlab.eval,
                        'no_such_function')

  unittest.main()