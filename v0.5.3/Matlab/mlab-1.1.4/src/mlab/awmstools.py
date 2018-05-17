# -*- encoding: utf-8 -*-
#############################################################################
################## awmstools : Common functions for python ###################
##############################################################################
##
## o author: Alexander Schmolck (A.Schmolck@gmx.net)
## o created: 2000-04-08T15:52:17+00:00
## o last changed: $Date: 2009-03-24 02:09:50 $
## o license: see file LICENSE
## o keywords: python, helper functions
## o requires: python >= 2.4
## o TODO:
##   - get rid of the bogus test failure (doctest: +ELLIPSIS)
##   - streamline or cull baroque stuff like reverse
##   - cull more stuff and factor into several files
##   - saveVars etc. should have `silent` option or so
##   - not all functions are tested rigorously yet
##   - write a fast merge (kicked old slow recursive one)
##
## Sorted in inverse order of uselessness :) The stuff under EXPERIMENTAL is
## just that: experimental. Expect it not to work, or to disappear or to be
## incompatibly modified in the future. The rest should be fairly stable.

"""A collection of various convenience functions and classes, small utilities
   and 'fixes'.

   Some just save a little bit of typing (`Result`), others are things that
   seem to have been forgotten in the standard libraries (`slurp`,
   `binarySearch`, `replaceStrs`) or that have a strange behavior
   (`os.path.splitext`). Apart from several general purpose utilities for
   lists (`flatten`) iterables in general (`window`, `unique`, `union`,
   `group` etc.) there are also more special purpose utilities such as various
   handy functions and classes for writing scripts (`DryRun`), for debugging
   (`makePrintReturner`) and for meta-programming (`gensym`).


"""
from __future__ import division
__docformat__ = "restructuredtext en"
__revision__ = "$Id: awmstools.py,v 1.29 2009-03-24 02:09:50 aschmolc Exp $"
__version__  = "0.9"
__author__   = "Alexander Schmolck <a.schmolck@gmx.net>"
__test__ = {} # this is for doctest

import bisect
import codecs
import copy
import cPickle
try: from functools import partial # python < 2.5 compatibility
except ImportError: partial = lambda f,*args,**kwargs: lambda *a,**k: f(args+a,update(kwargs,k))
from itertools import *
import inspect
import itertools
import math
import operator
import os
import getpass
import re
import sys
import tempfile
import time
import types
import urllib2
try: from threading import Lock
except ImportError: Lock = lambda: Null

try: any
except NameError: any = lambda xs: bool(some(xs)); all = lambda xs: bool(every(xs))

class _uniqueClass(object):
    """To create a single instance to be used for default values; supports
    comparison by-object identity to work around stupid classes that won't allow
    comparisons to non-self-instances."""
    def __eq__(a,b): return a is b;
    def __ne__(a,b): return a is not b
try: # don't redefine on reload
    __unique
except NameError:
    __unique = _uniqueClass()


if sys.maxint > 1e6*60*60*24*365*100: # see below
    # XXX this relies on the GIL & itertools for threadsafety
    # but since itertools.count can only count to sys.maxint...
    def Counter(start=0):
        """A threadsafe counter that let's you keep counting
        for at least 100 years at a rate of 1MHz (if `start`= 0).
        """
        return itertools.count(start).next
else:
    # ... we also need this more generic version
    class Counter(object):
        """A threadsafe counter that let's you keep counting
        for at least 100 years at a rate of 10^6/s (if `start`= 0).
        """
        def __init__(self, start=0):
            self.lock = Lock()
            self.count = start
        def __call__(self):
            try:
                self.lock.acquire()
                return self.count
            finally:
                self.count+=1
                self.lock.release()

# don't redefine on reload
try:
    _count
except NameError:
    _count = Counter()
    _gensyms = {}
def gensym(prefix="GSYM"):
    r"""Returns an string that is valid as a unique python variable name. Useful
    when creating functions etc. on the fly. Can be used from multiple threads
    and is `reload` safe.
    """
    return "%s%d" % (prefix, _count())

__test__['gensym'] = r"""
>>> import awmstools
>>> bak = awmstools._count
>>> awmstools._count = Counter()
>>> gensym()
'GSYM0'
>>> gensym()
'GSYM1'
>>> gensym('FOO')
'FOO2'
>>> import awmstools
>>> reload(awmstools) and None
>>> awmstools._count = bak
"""
# FIXME test threadsafety at least superficially!


#_. FIXES
# Fixes for things in python I'd like to behave differently

def rexGroups(rex):
    """Return the named groups in a regular expression (compiled or as string)
    in occuring order.

    >>> rexGroups(r'(?P<name>\w+) +(?P<surname>\w+)')
    ('name', 'surname')

    """
    if isinstance(rex,basestring): rex = re.compile(rex)
    return zip(*sorted([(n,g) for (g,n) in rex.groupindex.items()]))[1]


class IndexMaker(object):
    """Convinience class to make slices etc. that can be used for creating
    indices (mainly because using `slice` is a PITA).

    Examples:

    >>> range(4)[indexme[::-1]] == range(4)[::-1] == [3, 2, 1, 0]
    True
    >>> indexme[::-1]
    slice(None, None, -1)
    >>> indexme[0,:]
    (0, slice(None, None, None))
    """
    def __getitem__(self, a):
        return a
indexme = IndexMaker()


# A shortcut for 'infinite' integer e.g. for slicing: ``seq[4:INFI]`` as
# ``seq[4:len(seq)]`` is messy and only works if `seq` isn't an expression
INFI = sys.maxint
# real infinity
INF = 1e999999


class Result(object):
    """Circumvent python's lack of assignment expression (mainly useful for
       writing while loops):

        >>> import re
        >>> s = 'one 2 three 4 five 6'
        >>> findNumber = Result(re.compile('\d+').search)
        >>> while findNumber(s):
        ...     match = findNumber.result
        ...     print 'found', `match.group(0)`, 'at position', match.start()
        ...     s = s[match.end():]
        ...
        found '2' at position 4
        found '4' at position 7
        found '6' at position 6
    """
    def __init__(self, func):
        self.func = func
    def __call__(self,*args,**kwargs):
        self.result = self.func(*args,**kwargs)
        return self.result

class NullType(object):
    r"""Similar to `NoneType` with a corresponding singleton instance `Null`
that, unlike `None` accepts any message and returns itself.

Examples:
>>> Null("send", a="message")(*"and one more")[
...      "even index and"].what.you.get.still is Null
True
>>> not Null
True
>>> Null['something']
Null
>>> Null.something
Null
>>> Null in Null
False
>>> hasattr(Null, 'something')
True
>>> Null.something = "a value"
>>> Null.something
Null
>>> Null == Null
True
>>> Null == 3
False
"""

    def __new__(cls):                    return Null
    def __call__(self, *args, **kwargs): return Null
##    def __getstate__(self, *args):       return Null
    def __getinitargs__(self):
        print "__getinitargs__"
        return ('foobar',)
    def __getattr__(self, attr):         return Null
    def __getitem__(self, item):         return Null
    def __setattr__(self, attr, value):  pass
    def __setitem__(self, item, value):  pass
    def __len__(self):                   return 0
    def __iter__(self):                  return iter([])
    def __contains__(self, item):        return False
    def __repr__(self):                  return "Null"
Null = object.__new__(NullType)


def div(a,b):
    """``div(a,b)`` is like ``a // b`` if ``b`` devides ``a``, otherwise
    an `ValueError` is raised.

    >>> div(10,2)
    5
    >>> div(10,3)
    Traceback (most recent call last):
    ...
    ValueError: 3 does not divide 10
    """
    res, fail = divmod(a,b)
    if fail:
        raise ValueError("%r does not divide %r" % (b,a))
    else:
        return res


def ipshuffle(l, random=None):
    r"""Shuffle list `l` inplace and return it."""
    import random as _random
    _random.shuffle(l, random)
    return l

__test__['ipshuffle'] = r'''
>>> l = [1,2,3]
>>> ipshuffle(l, lambda :0.3) is l
True
>>> l
[2, 3, 1]
>>> l = [1,2,3]
>>> ipshuffle(l, lambda :0.4) is l
True
>>> l
[3, 1, 2]
'''


def shuffle(seq, random=None):
    r"""Return shuffled *copy* of `seq`."""
    if isinstance(seq, list):
        return ipshuffle(seq[:], random)
    elif isString(seq):
        # seq[0:0] == "" or  u""
        return seq[0:0].join(ipshuffle(list(seq)),random)
    else:
        return type(seq)(ipshuffle(list(seq),random))

__test__['shuffle'] = r'''
>>> l = [1,2,3]
>>> shuffle(l, lambda :0.3)
[2, 3, 1]
>>> l
[1, 2, 3]
>>> shuffle(l, lambda :0.4)
[3, 1, 2]
>>> l
[1, 2, 3]
'''

# s = open(file).read() would be a nice shorthand -- unfortunately it doesn't
# work (because the file is never properly closed, at least not under
# Jython). Thus:


def _normalizeToFile(maybeFile, mode, expand):
    if isinstance(maybeFile, int):
        return os.fdopen(maybeFile, mode)
    elif isString(maybeFile):
        if maybeFile.startswith('http://'): #XXX experimental
            return urllib2.urlopen(maybeFile)
        else:
            if expand:
                maybeFile = os.path.expandvars(os.path.expanduser(maybeFile))
            return open(maybeFile, mode)
    else:
        return maybeFile


def slurp(file, binary=False, expand=False):
    r"""Read in a complete file `file` as a string
    Parameters:

     - `file`: a file handle or a string (`str` or `unicode`).
     - `binary`: whether to read in the file in binary mode (default: False).
    """
    mode = "r" + ["b",""][not binary]
    file = _normalizeToFile(file, mode=mode, expand=expand)
    try: return file.read()
    finally: file.close()

# FIXME write proper tests for IO stuff
def withFile(file, func, mode='r', expand=False):
    """Pass `file` to `func` and ensure the file is closed afterwards. If
       `file` is a string, open according to `mode`; if `expand` is true also
       expand user and vars.
    """
    file = _normalizeToFile(file, mode=mode, expand=expand)
    try:      return func(file)
    finally:  file.close()


def slurpLines(file, expand=False):
    r"""Read in a complete file (specified by a file handler or a filename
    string/unicode string) as list of lines"""
    file = _normalizeToFile(file, "r", expand)
    try:     return file.readlines()
    finally: file.close()

def slurpChompedLines(file, expand=False):
    r"""Return ``file`` a list of chomped lines. See `slurpLines`."""
    f=_normalizeToFile(file, "r", expand)
    try: return list(chompLines(f))
    finally: f.close()

def strToTempfile(s, suffix=None, prefix=None, dir=None, binary=False):
    """Create a new tempfile, write ``s`` to it and return the filename.
    `suffix`, `prefix` and `dir` are like in `tempfile.mkstemp`.
    """
    fd, filename = tempfile.mkstemp(**dict((k,v) for (k,v) in
                                           [('suffix',suffix),('prefix',prefix),('dir', dir)]
                                           if v is not None))
    spitOut(s, fd, binary)
    return filename


def spitOut(s, file, binary=False, expand=False):
    r"""Write string `s` into `file` (which can be a string (`str` or
    `unicode`) or a `file` instance)."""
    mode = "w" + ["b",""][not binary]
    file = _normalizeToFile(file, mode=mode, expand=expand)
    try:     file.write(s)
    finally: file.close()

def spitOutLines(lines, file, expand=False):
    r"""Write all the `lines` to `file` (which can be a string/unicode or a
       file handler)."""
    file = _normalizeToFile(file, mode="w", expand=expand)
    try:     file.writelines(lines)
    finally: file.close()


#FIXME should use new subprocess module if possible
def readProcess(cmd, *args):
    r"""Similar to `os.popen3`, but returns 2 strings (stdin, stdout) and the
    exit code (unlike popen2, exit is 0 if no problems occured (for some
    bizarre reason popen2 returns None... <sigh>).

    FIXME: only works for UNIX; handling of signalled processes.
    """
    import popen2
    BUFSIZE=1024
    import select
    popen = popen2.Popen3((cmd,) + args, capturestderr=True)
    which = {id(popen.fromchild): [],
             id(popen.childerr):  []}
    select = Result(select.select)
    read   = Result(os.read)
    try:
        popen.tochild.close() # XXX make sure we're not waiting forever
        while select([popen.fromchild, popen.childerr], [], []):
            readSomething = False
            for f in select.result[0]:
                while read(f.fileno(), BUFSIZE):
                    which[id(f)].append(read.result)
                    readSomething = True
            if not readSomething:
                break
        out, err = ["".join(which[id(f)])
                    for f in [popen.fromchild, popen.childerr]]
        returncode = popen.wait()

        if os.WIFEXITED(returncode):
            exit = os.WEXITSTATUS(returncode)
        else:
            exit = returncode or 1 # HACK: ensure non-zero
    finally:
        try:
            popen.fromchild.close()
        finally:
            popen.childerr.close()
    return out or "", err or "", exit


def silentlyRunProcess(cmd,*args):
    """Like `runProcess` but stdout and stderr output is discarded. FIXME: only
       works for UNIX!"""
    return readProcess(cmd,*args)[2]

def runProcess(cmd, *args):
    """Run `cmd` (which is searched for in the executable path) with `args` and
    return the exit status.

    In general (unless you know what you're doing) use::

     runProcess('program', filename)

    rather than::

     os.system('program %s' % filename)

    because the latter will not work as expected if `filename` contains
    spaces or shell-metacharacters.

    If you need more fine-grained control look at ``os.spawn*``.
    """
    from os import spawnvp, P_WAIT
    return spawnvp(P_WAIT, cmd, (cmd,) + args)


#FIXME; check latest word on this...
def isSeq(obj):
    r"""Returns true if obj is a sequence (which does purposefully **not**
    include strings, because these are pseudo-sequences that mess
    up recursion.)"""
    return operator.isSequenceType(obj) and not isinstance(obj, (str, unicode))



# os.path's splitext is EVIL: it thinks that dotfiles are extensions!
def splitext(p):
    r"""Like the normal splitext (in posixpath), but doesn't treat dotfiles
    (e.g. .emacs) as extensions. Also uses os.sep instead of '/'."""

    root, ext = os.path.splitext(p)
    # check for dotfiles
    if (not root or root[-1] == os.sep): # XXX: use '/' or os.sep here???
        return (root + ext, "")
    else:
        return root, ext



#_. LIST MANIPULATION

def bipart(func, seq):
    r"""Like a partitioning version of `filter`. Returns
    ``[itemsForWhichFuncReturnedFalse, itemsForWhichFuncReturnedTrue]``.

    Example:

    >>> bipart(bool, [1,None,2,3,0,[],[0]])
    [[None, 0, []], [1, 2, 3, [0]]]
    """

    if func is None: func = bool
    res = [[],[]]
    for i in seq: res[not not func(i)].append(i)
    return res


def unzip(seq):
    r"""Perform the reverse operation to the builtin `zip` function."""
    # XXX should special case for more efficient handling
    return zip(*seq)

def binarySearchPos(seq, item, cmpfunc=cmp):
    r"""Return the position of `item` in ordered sequence `seq`, using comparison
    function `cmpfunc` (defaults to ``cmp``) and return the first found
    position of `item`, or -1 if `item` is not in `seq`. The returned position
    is NOT guaranteed to be the first occurence of `item` in `seq`."""

    if not seq:	return -1
    left, right = 0, len(seq) - 1
    if cmpfunc(seq[left],  item) ==  1 and \
       cmpfunc(seq[right], item) == -1:
        return -1
    while left <= right:
        halfPoint = (left + right) // 2
        comp = cmpfunc(seq[halfPoint], item)
        if   comp > 0: right = halfPoint - 1
        elif comp < 0: left  = halfPoint + 1
        else:          return  halfPoint
    return -1

__test__['binarySearchPos'] = r"""
>>> binarySearchPos(range(20), 20)
-1
>>> binarySearchPos(range(20), 1)
1
>>> binarySearchPos(range(20), 19)
19
>>> binarySearchPos(range(20), 0)
0
>>> binarySearchPos(range(1,21,2),4)
-1
>>> binarySearchPos(range(0,20,2), 6)
3
>>> binarySearchPos(range(19, -1, -1), 3, lambda x,y:-cmp(x,y))
16
"""


def binarySearchItem(seq, item, cmpfunc=cmp):
    r""" Search an ordered sequence `seq` for `item`, using comparison function
    `cmpfunc` (defaults to ``cmp``) and return the first found instance of
    `item`, or `None` if item is not in `seq`. The returned item is NOT
    guaranteed to be the first occurrence of item in `seq`."""
    pos = binarySearchPos(seq, item, cmpfunc)
    if pos == -1: raise KeyError("Item not in seq")
    else:         return seq[pos]

#XXX could extend this for other sequence types
def rotate(l, steps=1):
    r"""Rotates a list `l` `steps` to the left. Accepts
    `steps` > `len(l)` or < 0.

    >>> rotate([1,2,3])
    [2, 3, 1]
    >>> rotate([1,2,3,4],-2)
    [3, 4, 1, 2]
    >>> rotate([1,2,3,4],-5)
    [4, 1, 2, 3]
    >>> rotate([1,2,3,4],1)
    [2, 3, 4, 1]
    >>> l = [1,2,3]; rotate(l) is not l
    True
    """
    if len(l):
        steps %= len(l)
        if steps:
            res = l[steps:]
            res.extend(l[:steps])
    return res

def iprotate(l, steps=1):
    r"""Like rotate, but modifies `l` in-place.

    >>> l = [1,2,3]
    >>> iprotate(l) is l
    True
    >>> l
    [2, 3, 1]
    >>> iprotate(iprotate(l, 2), -3)
    [1, 2, 3]

    """
    if len(l):
        steps %= len(l)
        if steps:
            firstPart = l[:steps]
            del l[:steps]
            l.extend(firstPart)
    return l




# XXX: could wrap that in try: except: for non-hashable types, or provide an
# identity function parameter, but well... this is fast and simple (but wastes
# memory)
def unique(iterable):
    r"""Returns all unique items in `iterable` in the *same* order (only works
    if items in `seq` are hashable).
    """
    d = {}
    return (d.setdefault(x,x) for x in iterable if x not in d)

__test__['unique'] = r"""
>>> list(unique(range(3))) == range(3)
True
>>> list(unique([1,1,2,2,3,3])) == range(1,4)
True
>>> list(unique([1])) == [1]
True
>>> list(unique([])) == []
True
>>> list(unique(['a','a'])) == ['a']
True
"""

def notUnique(iterable, reportMax=INF):
    """Returns the elements in `iterable` that aren't unique; stops after it found
    `reportMax` non-unique elements.

    Examples:

    >>> list(notUnique([1,1,2,2,3,3]))
    [1, 2, 3]
    >>> list(notUnique([1,1,2,2,3,3], 1))
    [1]
    """
    hash = {}
    n=0
    if reportMax < 1:
        raise ValueError("`reportMax` must be >= 1 and is %r" % reportMax)
    for item in iterable:
        count = hash[item] = hash.get(item, 0) + 1
        if count > 1:
            yield item
            n += 1
            if n >= reportMax:
                return
__test__['notUnique'] = r"""
>>> list(notUnique(range(3)))
[]
>>> list(notUnique([1]))
[]
>>> list(notUnique([]))
[]
>>> list(notUnique(['a','a']))
['a']
>>> list(notUnique([1,1,2,2,3,3],2))
[1, 2]
>>> list(notUnique([1,1,2,2,3,3],0))
Traceback (most recent call last):
[...]
ValueError: `reportMax` must be >= 1 and is 0
"""



def unweave(iterable, n=2):
    r"""Divide `iterable` in `n` lists, so that every `n`th element belongs to
    list `n`.

    Example:

    >>> unweave((1,2,3,4,5), 3)
    [[1, 4], [2, 5], [3]]
    """
    res = [[] for i in range(n)]
    i = 0
    for x in iterable:
        res[i % n].append(x)
        i += 1
    return res




def weave(*iterables):
    r"""weave(seq1 [, seq2] [...]) ->  iter([seq1[0], seq2[0] ...]).

    >>> list(weave([1,2,3], [4,5,6,'A'], [6,7,8, 'B', 'C']))
    [1, 4, 6, 2, 5, 7, 3, 6, 8]

    Any iterable will work. The first exhausted iterable determines when to
    stop. FIXME rethink stopping semantics.

    >>> list(weave(iter(('is','psu')), ('there','no', 'censorship')))
    ['is', 'there', 'psu', 'no']
    >>> list(weave(('there','no', 'censorship'), iter(('is','psu'))))
    ['there', 'is', 'no', 'psu', 'censorship']
    """
    iterables = map(iter, iterables)
    while True:
        for it in iterables: yield it.next()

def atIndices(indexable, indices, default=__unique):
    r"""Return a list of items in `indexable` at positions `indices`.

    Examples:

    >>> atIndices([1,2,3], [1,1,0])
    [2, 2, 1]
    >>> atIndices([1,2,3], [1,1,0,4], 'default')
    [2, 2, 1, 'default']
    >>> atIndices({'a':3, 'b':0}, ['a'])
    [3]
    """
    if default is __unique:
        return [indexable[i] for i in indices]
    else:
        res = []
        for i in indices:
            try:
                res.append(indexable[i])
            except (IndexError, KeyError):
                res.append(default)
        return res

__test__['atIndices'] = r'''
>>> atIndices([1,2,3], [1,1,0,4])
Traceback (most recent call last):
[...]
IndexError: list index out of range
>>> atIndices({1:2,3:4}, [1,1,0,4])
Traceback (most recent call last):
[...]
KeyError: 0
>>> atIndices({1:2,3:4}, [1,1,0,4], 'default')
[2, 2, 'default', 'default']
'''




#XXX: should those have reduce like optional end-argument?
#FIXME should s defaul to n? (1 is less typing/better than len(somearg(foo)); )
def window(iterable, n=2, s=1):
    r"""Move an `n`-item (default 2) windows `s` steps (default 1) at a time
    over `iterable`.

    Examples:

    >>> list(window(range(6),2))
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    >>> list(window(range(6),3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
    >>> list(window(range(6),3, 2))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(window(range(5),3,2)) == list(window(range(6),3,2))
    True
    """
    assert n >= s
    last = []
    for elt in iterable:
        last.append(elt)
        if len(last) == n: yield tuple(last); last=last[s:]
#FIXME
xwindow = window
# FIXME rename to block?
def group(iterable, n=2, pad=__unique):
    r"""Iterate `n`-wise (default pairwise)  over `iter`.
    Examples:

    >>> for (first, last) in group("Akira Kurosawa John Ford".split()):
    ...     print "given name: %s surname: %s" % (first, last)
    ...
    given name: Akira surname: Kurosawa
    given name: John surname: Ford
    >>>
    >>> # both contain the same number of pairs
    >>> list(group(range(9))) == list(group(range(8)))
    True
    >>> # with n=3
    >>> list(group(range(10), 3))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    >>> list(group(range(10), 3, pad=0))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 0, 0)]
    """
    assert n>0    # ensure it doesn't loop forever
    if pad is not __unique: it = chain(iterable, (pad,)*(n-1))
    else:                   it = iter(iterable)
    perTuple = xrange(n)
    while True:
        yield tuple([it.next() for i in perTuple])

def iterate(f, n=None, last=__unique):
    """
    >>> list(iterate(lambda x:x//2)(128))
    [128, 64, 32, 16, 8, 4, 2, 1, 0]
    >>> list(iterate(lambda x:x//2, n=2)(128))
    [128, 64]
    """
    if n is not None:
        def funciter(start):
            for i in xrange(n): yield start; start = f(start)
    else:
        def funciter(start):
            while True:
                yield start
                last = f(start)
                if last == start: return
                last, start = start, last
    return funciter


def dropwhilenot(func, iterable):
    """
    >>> list(dropwhilenot(lambda x:x==3, range(10)))
    [3, 4, 5, 6, 7, 8, 9]
    """
    iterable = iter(iterable)
    for x in iterable:
        if func(x): break
    else: return
    yield x
    for x in iterable:
        yield x


def stretch(iterable, n=2):
    r"""Repeat each item in `iterable` `n` times.

    Example:

    >>> list(stretch(range(3), 2))
    [0, 0, 1, 1, 2, 2]
    """
    times = range(n)
    for item in iterable:
        for i in times: yield item


def splitAt(iterable, indices):
    r"""Yield chunks of `iterable`, split at the points in `indices`:

    >>> [l for l in splitAt(range(10), [2,5])]
    [[0, 1], [2, 3, 4], [5, 6, 7, 8, 9]]

    splits past the length of `iterable` are ignored:

    >>> [l for l in splitAt(range(10), [2,5,10])]
    [[0, 1], [2, 3, 4], [5, 6, 7, 8, 9]]


    """
    iterable = iter(iterable)
    now = 0
    for to in indices:
        try:
            res = []
            for i in range(now, to): res.append(iterable.next())
        except StopIteration: yield res; return
        yield res
        now = to
    res = list(iterable)
    if res: yield res


__test__['splitAt'] = r"""
>>> [l for l in splitAt(range(10), [1,5])]
[[0], [1, 2, 3, 4], [5, 6, 7, 8, 9]]
>>> [l for l in splitAt(range(10), [2,5,10])]
[[0, 1], [2, 3, 4], [5, 6, 7, 8, 9]]
>>> [l for l in splitAt(range(10), [2,5,9])]
[[0, 1], [2, 3, 4], [5, 6, 7, 8], [9]]
>>> [l for l in splitAt(range(10), [2,5,11])]
[[0, 1], [2, 3, 4], [5, 6, 7, 8, 9]]

"""




#_. HASH MANIPULATION


# XXX should we use copy or start with empty dict? former is more generic
# (should work for other dict types, too)
def update(d, e):
    """Return a copy of dict `d` updated with dict `e`."""
    res = copy.copy(d)
    res.update(e)
    return res

def invertDict(d, allowManyToOne=False):
    r"""Return an inverted version of dict `d`, so that values become keys and
    vice versa. If multiple keys in `d` have the same value an error is
    raised, unless `allowManyToOne` is true, in which case one of those
    key-value pairs is chosen at random for the inversion.

    Examples:

    >>> invertDict({1: 2, 3: 4}) == {2: 1, 4: 3}
    True
    >>> invertDict({1: 2, 3: 2})
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: d can't be inverted!
    >>> invertDict({1: 2, 3: 2}, allowManyToOne=True).keys()
    [2]
    """
    res = dict(izip(d.itervalues(), d.iterkeys()))
    if not allowManyToOne and len(res) != len(d):
        raise ValueError("d can't be inverted!")
    return res


#_. LISP LIKES

#AARGH strings are EVIL...
def iflatten(seq, isSeq=isSeq):
    r"""Like `flatten` but lazy."""
    for elt in seq:
        if isSeq(elt):
            for x in iflatten(elt, isSeq):
                yield x
        else:
            yield elt

__test__['iflatten'] = r"""
>>> type(iflatten([]))
<type 'generator'>
>>> iflatten([]).next()
Traceback (most recent call last):
  File "<console>", line 1, in ?
StopIteration
>>> (a,b,c) = iflatten([1,["2", ([3],)]])
>>> (a,b,c) == (1, '2', 3)
True

"""

def flatten(seq, isSeq=isSeq):
    r"""Returns a flattened version of a sequence `seq` as a `list`.
    Parameters:

     - `seq`: The sequence to be flattened (any iterable).
     - `isSeq`: The function called to determine whether something is a
        sequence (default: `isSeq`). *Beware that this function should
        **never** test positive for strings, because they are no real
        sequences and thus cause infinite recursion.*

    Examples:

    >>> flatten([1,[2,3,(4,[5,6]),7,8]])
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> # flaten only lists
    >>> flatten([1,[2,3,(4,[5,6]),7,8]], isSeq=lambda x:isinstance(x, list))
    [1, 2, 3, (4, [5, 6]), 7, 8]
    >>> flatten([1,2])
    [1, 2]
    >>> flatten([])
    []
    >>> flatten('123')
    ['1', '2', '3']
    """
    return [a for elt in seq
            for a in (isSeq(elt) and flatten(elt, isSeq) or
                      [elt])]


def countIf(predicate, iterable):
    r"""Count all the elements of for which `predicate` returns true."""
    return sum(1 for x in iterable if predicate(x))

__test__['countIf'] = r"""
>>> countIf(bool, range(10))
9
>>> countIf(bool, range(-1))
0
"""

def positionIf(pred, seq):
    """
    >>> positionIf(lambda x: x > 3, range(10))
    4
    """
    for i,e in enumerate(seq):
        if pred(e):
            return i
    return -1



def union(seq1=(), *seqs):
    r"""Return the set union of `seq1` and `seqs`, duplicates removed, order random.

    Examples:
    >>> union()
    []
    >>> union([1,2,3])
    [1, 2, 3]
    >>> union([1,2,3], {1:2, 5:1})
    [1, 2, 3, 5]
    >>> union((1,2,3), ['a'], "bcd")
    ['a', 1, 2, 3, 'd', 'b', 'c']
    >>> union([1,2,3], iter([0,1,1,1]))
    [0, 1, 2, 3]

    """
    if not seqs: return list(seq1)
    res = set(seq1)
    for seq in seqs:
        res.update(set(seq))
    return list(res)

# by making this a function, we can accomodate for new types later
def isSet(obj):
    import sets
    return isinstance(obj, (set,sets.BaseSet)) # AARGH -- WTF are they not subclasses!!!




def without(seq1, seq2):
    r"""Return a list with all elements in `seq2` removed from `seq1`, order
    preserved.

    Examples:

    >>> without([1,2,3,1,2], [1])
    [2, 3, 2]
    """
    if isSet(seq2): d2 = seq2
    else: d2 = set(seq2)
    return [elt for elt in seq1 if elt not in d2]


def findIf(predicate, iterable):
    """
    >>> findIf(lambda x: x>20, [10,20,30,40])
    30
    >>> findIf(lambda x: x>40, [10,20,30,40])
    False
    """
    try: return ifilter(predicate, iterable).next()
    except StopIteration: return False



def some(predicate, *seqs):
    """
    >>> some(lambda x: x, [0, False, None])
    False
    >>> some(lambda x: x, [None, 0, 2, 3])
    2
    >>> some(operator.eq, [0,1,2], [2,1,0])
    True
    >>> some(operator.eq, [1,2], [2,1])
    False
    """
    try:
        if len(seqs) == 1: return ifilter(bool,imap(predicate, seqs[0])).next()
        else:             return ifilter(bool,starmap(predicate, izip(*seqs))).next()
    except StopIteration: return False

def every(predicate, *iterables):
    r"""Like `some`, but only returns `True` if all the elements of `iterables`
    satisfy `predicate`.

    Examples:
    >>> every(bool, [])
    True
    >>> every(bool, [0])
    False
    >>> every(bool, [1,1])
    True
    >>> every(operator.eq, [1,2,3],[1,2])
    True
    >>> every(operator.eq, [1,2,3],[0,2])
    False
    """
    try:
        if len(iterables) == 1: ifilterfalse(predicate, iterables[0]).next()
        else:                  ifilterfalse(bool, starmap(predicate, izip(*iterables))).next()
    except StopIteration: return True
    else: return False





#_. TIME AND DATE HANDLING

# XXX: not strictly a time related function, but well...
def nTimes(n, f, *args, **kwargs):
    r"""Call `f` `n` times with `args` and `kwargs`.
    Useful e.g. for simplistic timing.

    Examples:

    >>> nTimes(3, sys.stdout.write, 'hallo\n')
    hallo
    hallo
    hallo

    """
    for i in xrange(n): f(*args, **kwargs)


def timeCall(*funcAndArgs, **kwargs):
    r"""Return the time (in ms) it takes to call a function (the first
    argument) with the remaining arguments and `kwargs`.

    Examples:

    To find out how long ``func('foo', spam=1)`` takes to execute, do:

    ``timeCall(func, foo, spam=1)``
    """

    func, args = funcAndArgs[0], funcAndArgs[1:]
    start = time.time()
    func(*args, **kwargs)
    return time.time() - start

__test__['timeCall'] = r"""
>>> round(timeCall(time.sleep, 1))
1.0
"""


#_. STRING PROCESSING

def isString(obj):
    r"""Return `True` iff `obj` is some type of string (i.e. `str` or
    `unicode`)."""
    return isinstance(obj, basestring)

chomp = partial(re.compile(r"\n+$").sub, '')
chomp.__doc__ =  r"""Discards all trailing newlines in string."""
__test__['chomp'] = r"""
>>> chomp('foobar\n\nf') == 'foobar\n\nf'
True
>>> chomp('foobar\n\n') == 'foobar'
True
"""

def chompLines(lines):
    r"""Returns a lazy sequence of `lines` sans any trailing newline."""
    return imap(chomp, lines)
    # faster 2.5 version (not 100% identical, but good enough):
    ## return (L[:-1] if L[-1:] == "\n" else L for L in lines)

__test__['chompLines'] = r"""
>>> list(chompLines(['\n', 'foo\n', 'foobar\n\nf']))
['', 'foo', 'foobar\n\nf']
>>> chompLines(['foo\n', '3', 'foobar\n\nf']).next()
'foo'
"""

def replaceStrs(s, *args):
    r"""Replace all ``(frm, to)`` tuples in `args` in string `s`.

    >>> replaceStrs("nothing is better than warm beer",
    ...             ('nothing','warm beer'), ('warm beer','nothing'))
    'warm beer is better than nothing'

    """
    if args == (): return s
    mapping = dict((frm, to) for frm, to in args)
    return re.sub("|".join(map(re.escape, mapping.keys())),
                  lambda match:mapping[match.group(0)], s)

def escape(s):
    ur"""Backslash escape non-printable non-ascii characters and ``"'\``.

    >>> escape('''a\\string"with'some\tspecial\ncharacters''')
    'a\\\\string"with\\'some\\tspecial\\ncharacters'
    >>> print eval(escape(u'''u"a\\'unicode\tstring ®"'''))
    a\'unicode	string ®

    """
    try:
        return escapeAscii(s)
    except (UnicodeEncodeError, TypeError):
        return escapeUnicode(s)
def escapeAscii(s):
    return codecs.getwriter('string_escape').encode(s)[0]
def escapeUnicode(s):
    return codecs.getwriter('unicode_escape').encode(s)[0]
def unescape(s):
    r"""Inverse of `escape`.
    >>> unescape(r'\x41\n\x42\n\x43')
    'A\nB\nC'
    >>> unescape(r'\u86c7')
    u'\u86c7'
    >>> unescape(u'ah')
    u'ah'
    """
    if re.search(r'(?<!\\)\\(\\\\)*[uU]', s) or isinstance(s, unicode):
        return unescapeUnicode(s)
    else:
        return unescapeAscii(s)
def unescapeAscii(s):
    return codecs.getreader('string_escape').decode(s)[0]
def unescapeUnicode(s):
    return codecs.getreader('unicode_escape').decode(s)[0]



def lineAndColumnAt(s, pos):
    r"""Return line and column of `pos` (0-based!) in `s`. Lines start with
    1, columns with 0.

    Examples:

    >>> lineAndColumnAt("0123\n56", 5)
    (2, 0)
    >>> lineAndColumnAt("0123\n56", 6)
    (2, 1)
    >>> lineAndColumnAt("0123\n56", 0)
    (1, 0)
    """
    if pos >= len(s):
        raise IndexError("`pos` %d not in string" % pos)
    # *don't* count last '\n', if it is at pos!
    line = s.count('\n',0,pos)
    if line:
        return line + 1, pos - s.rfind('\n',0,pos) - 1
    else:
        return 1, pos

#_. TERMINAL OUTPUT FUNCTIONS

def prin(*args, **kwargs):
    r"""Like ``print``, but a function. I.e. prints out all arguments as
    ``print`` would do. Specify output stream like this::

      print('ERROR', `out="sys.stderr"``).

    """
    print >> kwargs.get('out',None), " ".join([str(arg) for arg in args])
__test__['prin'] = r"""
>>> prin(1,2,3,out=None)
1 2 3
"""


def underline(s, lineC='-'):
    r"""Return `s` + newline + enough '-' (or lineC if specified) to underline it
    and a final newline.

    Example:

    >>> print underline("TOP SECRET", '*'),
    TOP SECRET
    **********

    """
    return s + "\n" + lineC * len(s) + "\n"

def fitString(s, maxCol=79, newlineReplacement=None):
    r"""Truncate `s` if necessary to fit into a line of width `maxCol`
    (default: 79), also replacing newlines with `newlineReplacement` (default
    `None`: in which case everything after the first newline is simply
    discarded).

    Examples:

    >>> fitString('12345', maxCol=5)
    '12345'
    >>> fitString('123456', maxCol=5)
    '12...'
    >>> fitString('a line\na second line')
    'a line'
    >>> fitString('a line\na second line', newlineReplacement='\\n')
    'a line\\na second line'
    """
    assert isString(s)
    if '\n' in s:
        if newlineReplacement is None:
            s = s[:s.index('\n')]
        else:
            s = s.replace("\n", newlineReplacement)
    if maxCol is not None and len(s) > maxCol:
        s = "%s..." % s[:maxCol-3]
    return s

#_. EVIL THINGS

def magicGlobals(level=1):
    r"""Return the globals of the *caller*'s caller (default), or `level`
    callers up."""
    return inspect.getouterframes(inspect.currentframe())[1+level][0].f_globals

def magicLocals(level=1):
    r"""Return the locals of the *caller*'s caller (default) , or `level`
    callers up.
    """
    return inspect.getouterframes(inspect.currentframe())[1+level][0].f_locals

def thisModule():
    return sys.modules[sys._getframe(3).f_globals['__name__']]

#_. PERSISTENCE

def __saveVarsHelper(filename, varNamesStr, outOf,extension='.bpickle',**opts):
    filename = os.path.expanduser(filename)
    if outOf is None: outOf = magicGlobals(2)
    if not varNamesStr or not isString(varNamesStr):
        raise ValueError, "varNamesStr must be a string!"
    varnames = varNamesStr.split()
    if not splitext(filename)[1]: filename += extension
    if opts.get("overwrite") == 0 and os.path.exists(filename):
	raise RuntimeError("File already exists")
    return filename, varnames, outOf

def saveVars(filename, varNamesStr, outOf=None, **opts):
    r"""Pickle name and value of all those variables in `outOf` (default: all
    global variables (as seen from the caller)) that are named in
    `varNamesStr` into a file called `filename` (if no extension is given,
    '.bpickle' is appended). Overwrites file without asking, unless you
    specify `overwrite=0`. Load again with `loadVars`.

    Thus, to save the global variables ``bar``, ``foo`` and ``baz`` in the
    file 'savedVars' do::

      saveVars('savedVars', 'bar foo baz')

    """
    filename, varnames, outOf = __saveVarsHelper(
        filename, varNamesStr, outOf, **opts)
    print "pickling:\n", "\n".join(sorted(varnames))
    try:
        f = None
	f = open(filename, "wb")

	cPickle.dump(dict(zip(varnames, atIndices(outOf, varnames))),
                     f, 1) # UGH: cPickle, unlike pickle doesn't accept bin=1
    finally:
        if f: f.close()


#FIXME untested
def saveDict(filename, d, **kwargs):
    saveVars(filename, " ".join(d.keys()), outOf=d, **kwargs)


def addVars(filename, varNamesStr, outOf=None):
    r"""Like `saveVars`, but appends additional variables to file."""
    filename, varnames, outOf = __saveVarsHelper(filename, varNamesStr, outOf)
    f = None
    try:
        f = open(filename, "rb")
        h = cPickle.load(f)
        f.close()

        h.update(dict(zip(varnames, atIndices(outOf, varnames))))
        f = open(filename, "wb")
        cPickle.dump( h, f , 1 )
    finally:
        if f: f.close()

def loadDict(filename):
    """Return the variables pickled pickled into `filename` with `saveVars`
    as a dict."""
    filename = os.path.expanduser(filename)
    if not splitext(filename)[1]: filename += ".bpickle"
    f = None
    try:
        f = open(filename, "rb")
        varH = cPickle.load(f)
    finally:
        if f: f.close()
    return varH

def loadVars(filename, ask=True, into=None, only=None):
    r"""Load variables pickled with `saveVars`.
    Parameters:

        - `ask`: If `True` then don't overwrite existing variables without
                 asking.
        - `only`: A list to limit the variables to or `None`.
        - `into`: The dictionary the variables should be loaded into (defaults
                   to global dictionary).
           """

    filename = os.path.expanduser(filename)
    if into is None: into = magicGlobals()
    varH = loadDict(filename)
    toUnpickle = only or varH.keys()
    alreadyDefined = filter(into.has_key, toUnpickle)
    if alreadyDefined and ask:
	print "The following vars already exist; overwrite (yes/NO)?\n",\
	      "\n".join(alreadyDefined)
	if raw_input() != "yes":
	    toUnpickle = without(toUnpickle, alreadyDefined)
    if not toUnpickle:
	print "nothing to unpickle"
	return None
    print "unpickling:\n",\
	  "\n".join(sorted(toUnpickle))
    for k in varH.keys():
        if k not in toUnpickle:
            del varH[k]
    into.update(varH)



#_. SCRIPTING



def runInfo(prog=None,vers=None,date=None,user=None,dir=None,args=None):
    r"""Create a short info string detailing how a program was invoked. This is
    meant to be added to a history comment field of a data file were it is
    important to keep track of what programs modified it and how.

    !!!:`args` should be a **``list``** not a ``str``."""

    return "%(prog)s %(vers)s;" \
           " run %(date)s by %(usr)s in %(dir)s with: %(args)s'n" % \
           mkDict(prog=prog or sys.argv[0],
                  vers=vers or magicGlobals().get("__version__", ""),
                  date=date or isoDateTimeStr(),
                  usr=user or getpass.getuser(),
                  dir=dir or os.getcwd(),
                  args=" ".join(args or sys.argv))




class DryRun:
    """A little class that is usefull for debugging and testing and for
programs that should have a "dry run" option.


Examples:

    >>> import sys
    >>> from os import system
    >>> dry = True
    >>> # that's how you can switch the programms behaviour between dry run
    >>>
    >>> if dry:
    ...     # (`out` defaults to stdout, but we need it here for doctest)
    ...     run = DryRun(dry=True, out=sys.stdout)
    ... else:
    ...     run = DryRun(dry=False, out=sys.stdout)
    ...
    >>> ## IGNORE 2 hacks to get doctest working, please ignore
    >>> def system(x): print "hallo"
    ...
    >>> run.__repr__ = lambda : "<awmstools.DryRun instance at 0x8222d6c>"
    >>> ## UNIGNORE
    >>> run(system, 'echo "hallo"')
    system('echo "hallo"')
    >>> # now let's get serious
    >>> run.dry = False
    >>> run(system, 'echo "hallo"')
    hallo
    >>> # just show what command would be run again
    >>> run.dry = True
    >>> # You can also specify how the output for a certain function should be
    ... # look like, e.g. if you just want to print the command for all system
    ... # calls, do the following:
    >>> run.addFormatter(system, lambda x,*args, **kwargs: args[0])
    <awmstools.DryRun instance at 0x8222d6c>
    >>> run(system, 'echo "hallo"')
    echo "hallo"
    >>> # Other functions will still be formated with run.defaultFormatter, which
    ... # gives the following results
    >>> run(int, "010101", 2)
    int('010101', 2)
    >>> # Switch to wet run again:
    >>> run.dry = False
    >>> run(int, "010101", 2)
    21
    >>>

Caveats:

    - remember that arguments might look different from what you specified in
      the source-code, e.g::

            >>> run.dry = True
            >>> run(chr, 0x50)
            chr(80)
            >>>

    - 'DryRun(showModule=True)' will try to print the module name where func
       was defined, this might however *not* produce the results you
       expected. For example, a function might be defined in another module
       than the one from which you imported it:

            >>> run = DryRun(dry=True, showModule=True)
            >>> run(os.path.join, "path", "file")
            posixpath.join('path', 'file')
            >>>

see `DryRun.__init__` for more details."""

    def __init__(self, dry=True, out=None, showModule=False):
        """
        Parameters:
            - `dry` : specifies whether to do a try run or not.
            - `out` : is the stream to which all dry runs will be printed
                      (default stdout).
            - `showModule` : specifies whether the name of a module in which a
               function was defined is printed (if known).
    """

        self.dry = dry
        self.formatterDict = {}
        self.out = out
        self.showModule = showModule
        def defaultFormatter(func, *args, **kwargs):
            if self.showModule and inspect.getmodule(func):
                funcName = inspect.getmodule(func).__name__ + '.' + func.__name__
            else:
                funcName = func.__name__
            return "%s(%s)" % (funcName,
              ", ".join(map(repr,args) + map(lambda x: "%s=%s" %
                                             tuple(map(repr,x)), kwargs.items())))
        self.defaultFormatter = defaultFormatter
    def __call__(self, func, *args, **kwargs):
        """Shorcut for self.run."""
        return self.run(func, *args, **kwargs)
    def run(self, func, *args, **kwargs):
        """Same as ``self.dryRun`` if ``self.dry``, else same as ``self.wetRun``."""
        if self.dry:
            return self.dryRun(func, *args, **kwargs)
        else:
            return self.wetRun(func, *args, **kwargs)
    def addFormatter(self, func, formatter):
        """Sets the function that is used to format calls to func. formatter is a
        function that is supposed to take these arguments: `func`, `*args` and
        `**kwargs`."""
        self.formatterDict[func] = formatter
        return self
    def dryRun(self, func, *args, **kwargs):
        """Instead of running function with `*args` and `**kwargs`, just print
           out the function call."""

        print >> self.out, \
              self.formatterDict.get(func, self.defaultFormatter)(func, *args, **kwargs)
    def wetRun(self, func, *args, **kwargs):
        """Run function with ``*args`` and ``**kwargs``."""
        return func(*args, **kwargs)




#_. DEBUGGING/INTERACTIVE DEVELOPMENT

def makePrintReturner(pre="", post="" ,out=None):
    r"""Creates functions that print out their argument, (between optional
    `pre` and `post` strings) and return it unmodified. This is usefull for
    debugging e.g. parts of expressions, without having to modify the behavior
    of the program.

    Example:

    >>> makePrintReturner(pre="The value is:", post="[returning]")(3)
    The value is: 3 [returning]
    3
    >>>
    """
    def printReturner(arg):
        myArgs = [pre, arg, post]
        prin(*myArgs, **{'out':out})
        return arg
    return printReturner



#_ : Tracing like facilities

# FIXME This is not recursive (and really shouldn't be I guess, at least not
# without extra argument) but returning a function wrapper here is really not
# enough, it should be a class (callable hack is of limited workability)
class ShowWrap(object):
    """A simple way to trace modules or objects
    Example::

    >> import os
    >> os = ShowWrap(os, '->')
    >> os.getenv('SOME_STRANGE_NAME', 'NOT_FOUND')
    -> os.getenv('SOME_STRANGE_NAME','NOT_FOUND')
    'NOT_FOUND'
    """
    def __init__(self,module, prefix='-> '):
        self.module=module
        self.prefix=prefix
    def __getattribute__(self, name):
        myDict = super(ShowWrap, self).__getattribute__('__dict__')
        realThing = getattr(myDict['module'], name)
        if not callable(realThing):
            return realThing
        else:
            def show(*x, **y):
                print >>sys.stderr, "%s%s.%s(%s)" % (
                    myDict['prefix'],
                    getattr(myDict['module'], '__name__', '?'),
                    name,
                    ",".join(map(repr,x) + ["%s=%r" % (n, v) for n,v in y.items()]))
                return realThing(*x, **y)
            return show


# XXX a nice example of python's expressiveness, but how useful is it?
def asVerboseContainer(cont, onGet=None, onSet=None, onDel=None):
    """Returns a 'verbose' version of container instance `cont`, that will
       execute `onGet`, `onSet` and `onDel` (if not `None`) every time
       __getitem__, __setitem__ and __delitem__ are called, passing `self`, `key`
       (and `value` in the case of set). E.g:

       >>> l = [1,2,3]
       >>> l = asVerboseContainer(l,
       ...                onGet=lambda s,k:k==2 and prin('Got two:', k),
       ...                onSet=lambda s,k,v:k == v and prin('k == v:', k, v),
       ...                onDel=lambda s,k:k == 1 and prin('Deleting one:', k))
       >>> l
       [1, 2, 3]
       >>> l[1]
       2
       >>> l[2]
       Got two: 2
       3
       >>> l[2] = 22
       >>> l[2] = 2
       k == v: 2 2
       >>> del l[2]
       >>> del l[1]
       Deleting one: 1

    """
    class VerboseContainer(type(cont)):
        if onGet:
            def __getitem__(self, key):
                onGet(self, key)
                return super(VerboseContainer, self).__getitem__(key)
        if onSet:
            def __setitem__(self, key, value):
                onSet(self, key, value)
                return super(VerboseContainer, self).__setitem__(key, value)
        if onDel:
            def __delitem__(self, key):
                onDel(self, key)
                return super(VerboseContainer, self).__delitem__(key)
    return VerboseContainer(cont)



#_. CONVENIENCE

#FIXME untested change
#FIXME add checks for valid names
class ezstruct(object):
    r"""
    Examples:

        >>> brian = ezstruct(name="Brian", age=30)
        >>> brian.name
        'Brian'
        >>> brian.age
        30
        >>> brian.life = "short"
        >>> brian
        ezstruct(age=30, life='short', name='Brian')
        >>> del brian.life
        >>> brian == ezstruct(name="Brian", age=30)
        True
        >>> brian != ezstruct(name="Jesus", age=30)
        True
        >>> len(brian)
        2

    Call the object to create a clone:

        >>> brian() is not brian and brian(name="Jesus") == ezstruct(name="Jesus", age=30)
        True

    Conversion to/from dict:

        >>> ezstruct(**dict(brian)) == brian
        True

    Evil Stuff:

        >>> brian['name', 'age']
        ('Brian', 30)
        >>> brian['name', 'age'] = 'BRIAN', 'XXX'
        >>> brian
        ezstruct(age='XXX', name='BRIAN')
    """
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    def __call__(self, **kwargs):
        import copy
        res = copy.copy(self)
        res.__init__(**kwargs)
        return res
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __len__(self):
        return len([k for k in self.__dict__.iterkeys()
                    if not (k.startswith('__') or k.endswith('__'))])
    # FIXME rather perverse
    def __getitem__(self, nameOrNames):
        if isString(nameOrNames):
            return self.__dict__[nameOrNames]
        else:
            return tuple([self.__dict__[n] for n in nameOrNames])
    # FIXME rather perverse
    def __setitem__(self, nameOrNames, valueOrValues):
        if isString(nameOrNames):
            self.__dict__[nameOrNames] = valueOrValues
        else:
            for (n,v) in zip(nameOrNames, valueOrValues):
                self.__dict__[n] = v
    def __contains__(self, key):
        return key in self.__dict__ and not (key.startswith('__') or key.endswith('__'))
    def __iter__(self):
        for (k,v) in self.__dict__.iteritems():
            if not (k.startswith('__') or k.endswith('__')):
                yield k,v
    def __repr__(self):
        return mkRepr(self, **vars(self))

#XXX should we really sort? This makes it impossible for the user to
#customise sorting by specifying a priority dict, but well...
#XXX this should do folding...

def mkRepr(instance, *argls, **kwargs):
    r"""Convinience function to implement ``__repr__``. `kwargs` values are
        ``repr`` ed. Special behavior for ``instance=None``: just the
        arguments are formatted.

    Example:

        >>> class Thing:
        ...     def __init__(self, color, shape, taste=None):
        ...         self.color, self.shape, self.taste = color, shape, taste
        ...     def __repr__(self):
        ...         return mkRepr(self, self.color, self.shape, taste=self.taste)
        ...
        >>> maggot = Thing('white', 'cylindrical', 'chicken')
        >>> maggot
        Thing('white', 'cylindrical', taste='chicken')
        >>> Thing('Color # 132942430-214809804-412430988081-241234', 'unkown', taste=maggot)
        Thing('Color # 132942430-214809804-412430988081-241234',
              'unkown',
              taste=Thing('white', 'cylindrical', taste='chicken'))
    """
    width=79
    maxIndent=15
    minIndent=2
    args = (map(repr, argls) + ["%s=%r" % (k, v)
                               for (k,v) in sorted(kwargs.items())]) or [""]
    if instance is not None:
        start = "%s(" % instance.__class__.__name__
        args[-1] += ")"
    else:
        start = ""
    if len(start) <= maxIndent and len(start) + len(args[0]) <= width and \
           max(map(len,args)) <= width: # XXX mag of last condition bit arbitrary
        indent = len(start)
        args[0] = start + args[0]
        if sum(map(len, args)) + 2*(len(args) - 1) <= width:
            return ", ".join(args)
    else:
        indent = minIndent
        args[0] = start + "\n" + " " * indent + args[0]
    return (",\n" + " " * indent).join(args)

__test__['mkRepr'] = r"""
>>> ezstruct()
ezstruct()
>>> ezstruct(a=1,b=2,c=3)(_='foooooooooooooooooooooooooooooooooooooooooooooooo000000000000000000')
ezstruct(
  _='foooooooooooooooooooooooooooooooooooooooooooooooo000000000000000000',
  a=1,
  b=2,
  c=3)
>>> ezstruct(a=1,b=2,c=3)(d='foooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000')
ezstruct(a=1,
         b=2,
         c=3,
         d='foooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000')
>>> ezstruct(a=1,b=2,c=3)
ezstruct(a=1, b=2, c=3)
"""


#_. EXPERIMENTAL

def d2attrs(*args, **kwargs):
    """Utility function to remove ``**kwargs`` parsing boiler-plate in
       ``__init__``:

        >>> kwargs = dict(name='Bill', age=51, income=1e7)
        >>> self = ezstruct(); d2attrs(kwargs, self, 'income', 'name'); self
        ezstruct(income=10000000.0, name='Bill')
        >>> self = ezstruct(); d2attrs(kwargs, self, 'income', age=0, bloodType='A'); self
        ezstruct(age=51, bloodType='A', income=10000000.0)

        To set all keys from ``kwargs`` use:

        >>> self = ezstruct(); d2attrs(kwargs, self, 'all!'); self
        ezstruct(age=51, income=10000000.0, name='Bill')
    """
    (d, self), args = args[:2], args[2:]
    if args[0] == 'all!':
        assert len(args) == 1
        for k in d: setattr(self, k, d[k])
    else:
        if len(args) != len(set(args)) or set(kwargs) & set(args):
            raise ValueError('Duplicate keys: %s' %
                             list(notUnique(args)) + list(set(kwargs) & set(args)))
        for k in args:
            if k in kwargs: raise ValueError('%s specified twice' % k)
            setattr(self, k, d[k])
        for dk in kwargs:
            setattr(self, dk, d.get(dk, kwargs[dk]))

def ipairwise(fun, v):
    for x0,x1 in window(v): yield fun(x0,x1)

def pairwise(fun, v):
    """
    >>> pairwise(operator.sub, [4,3,2,1,-10])
    [1, 1, 1, 11]
    >>> import numpy
    >>> pairwise(numpy.subtract, numpy.array([4,3,2,1,-10]))
    array([ 1,  1,  1, 11])
    """
    if not hasattr(v, 'shape'):
        return list(ipairwise(fun,v))
    else:
        return fun(v[:-1],v[1:])



def ignoreErrors(func, *args, **kwargs):
    """
    >>> ignoreErrors(int, '3')
    3
    >>> ignoreErrors(int, 'three')

    """
    try:    return func(*args, **kwargs)
    except Exception: return None



def argmax(iterable, key=None, both=False):
    """
    >>> argmax([4,2,-5])
    0
    >>> argmax([4,2,-5], key=abs)
    2
    >>> argmax([4,2,-5], key=abs, both=True)
    (2, 5)
    """
    if key is not None:
        it = imap(key, iterable)
    else:
        it = iter(iterable)
    score, argmax = reduce(max, izip(it, count()))
    if both:
        return argmax, score
    return argmax

def argmin(iterable, key=None, both=False):
    """See `argmax`.
    """
    if key is not None:
        it = imap(key, iterable)
    else:
        it = iter(iterable)
    score, argmin = reduce(min, izip(it, count()))
    if both:
        return argmin, score
    return argmin




# FIXME this won't work for complexes but then you can't use them as ints
# anyway
def isInt(num):
    """Returns true if `num` is (sort of) an integer.
    >>> isInt(3) == isInt(3.0) == 1
    True
    >>> isInt(3.2)
    False
    >>> import numpy
    >>> isInt(numpy.array(1))
    True
    >>> isInt(numpy.array([1]))
    False
    """
    try:
        len(num) # FIXME fails for Numeric but Numeric is obsolete
    except:
        try:
            return (num - math.floor(num) == 0) == True
        except: return False
    else: return False

def ordinalStr(num):
    """ Convert `num` to english ordinal.
    >>> map(ordinalStr, range(6))
    ['0th', '1st', '2nd', '3rd', '4th', '5th']
    """
    assert isInt(num)
    return "%d%s" % (num, {1:'st', 2:'nd', 3:'rd'}.get(int(num), 'th'))


# The stuff here is work in progress and may be dropped or modified
# incompatibly without further notice




# rename to mapcan
def mapConcat(func, *iterables):
    """Similar to `map` but the instead of collecting the return values of
    `func` in a list, the items of each return value are instaed collected
    (so `func` must return an iterable type).

    Examples:

    >>> mapConcat(lambda x:[x], [1,2,3])
    [1, 2, 3]
    >>> mapConcat(lambda x: [x,str(x)], [1,2,3])
    [1, '1', 2, '2', 3, '3']
    """
    return [e for l in imap(func, *iterables) for e in l]





def unfold(seed, by, last = __unique):
    """
    >>> list(unfold(1234, lambda x: divmod(x,10)))[::-1]
    [1, 2, 3, 4]
    >>> sum(imap(operator.mul,unfold(1234, lambda x:divmod(x,10)), iterate(lambda x:x*10)(1)))
    1234
    >>> g = unfold(1234, lambda x:divmod(x,10))
    >>> reduce((lambda (total,pow),digit:(total+pow*digit, 10*pow)), g, (0,1))
    (1234, 10000)
    """

    while True:
        seed, val = by(seed);
        if last == seed: return
        last = seed; yield val

def reduceR(f, sequence, initial=__unique):
    """*R*ight reduce.
    >>> reduceR(lambda x,y:x/y, [1.,2.,3.,4]) == 1./(2./(3./4.)) == (1./2.)*(3./4.)
    True
    >>> reduceR(lambda x,y:x-y, iter([1,2,3]),4) == 1-(2-(3-4)) == (1-2)+(3-4)
    True
    """
    try: rev = reversed(sequence)
    except TypeError: rev = reversed(list(sequence))
    if initial is __unique: return reduce(lambda x,y:f(y,x), rev)
    else:                   return reduce(lambda x,y:f(y,x), rev, initial)

# FIXME add doc kwarg?
def compose(*funcs):
    """Compose `funcs` to a single function.

    >>> compose(operator.abs, operator.add)(-2,-3)
    5
    >>> compose()('nada')
    'nada'
    >>> compose(sorted, set, partial(filter, None))(range(3)[::-1]*2)
    [1, 2]
    """
    # slightly optimized for most common cases and hence verbose
    if len(funcs) == 2: f0,f1=funcs; return lambda *a,**kw: f0(f1(*a,**kw))
    elif len(funcs) == 3: f0,f1,f2=funcs; return lambda *a,**kw: f0(f1(f2(*a,**kw)))
    elif len(funcs) == 0: return lambda x:x     # XXX single kwarg
    elif len(funcs) == 1: return funcs[0]
    else:
        def composed(*args,**kwargs):
            y = funcs[-1](*args,**kwargs)
            for f in funcs[:0:-1]: y = f(y)
            return y
        return composed


def romanNumeral(n):
    """
    >>> romanNumeral(13)
    'XIII'
    >>> romanNumeral(2944)
    'MMCMXLIV'
    """
    if 0 > n > 4000: raise ValueError('``n`` must lie between 1 and 3999: %d' % n)
    roman   = 'I IV  V  IX  X  XL   L  XC    C   CD    D   CM     M'.split()
    arabic  = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    res = []
    while n>0:
        pos = bisect.bisect_right(arabic, n)-1
        fit = n//arabic[pos]
        res.append(roman[pos]*fit); n -= fit * arabic[pos]
    return "".join(res)




def _docTest():
    import doctest, awmstools
    return doctest.testmod(awmstools)

def first(n, it, constructor=list):
    """
    >>> first(3,iter([1,2,3,4]))
    [1, 2, 3]
    >>> first(3,iter([1,2,3,4]), iter) #doctest: +ELLIPSIS
    <itertools.islice object at ...>
    >>> first(3,iter([1,2,3,4]), tuple)
    (1, 2, 3)
    """
    return constructor(itertools.islice(it,n))
def drop(n, it, constructor=list):
    """
    >>> first(10,drop(10,xrange(sys.maxint),iter))
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    """
    return constructor(itertools.islice(it,n,None))

if __name__ in ("__main__", "__IPYTHON_main__"):
    _docTest()
    import unittest
    class ProcessTest(unittest.TestCase):
        def testProcesses(self):
            assert silentlyRunProcess('ls') == 0
            assert silentlyRunProcess('ls', '/tmp') == 0
            assert silentlyRunProcess('i-DoNOT___EXIST')
            assert silentlyRunProcess('latex')
            assert readProcess('ls', '-d', '/tmp') == ('/tmp\n', '', 0)
            out = readProcess('ls', '-d', '/i-DoNOT___.EXIST')
            assert out[0] == ''
            assert re.match( 'ls:.*/i-DoNOT___.EXIST:.*No such file or directory.*', out[1])
            assert out[2] == 2, out[2]
    suite = unittest.TestSuite(map(unittest.makeSuite,
                                   (ProcessTest,
                                   )))
    #suite.debug()
    unittest.TextTestRunner(verbosity=2).run(suite)


# don't litter the namespace on ``from awmstools import *``
__all__ = []
me = sys.modules[__name__]
for n in dir(me):
    if n != me and not isinstance(getattr(me,n), type(me)):
        __all__.append(n)
del me, n

