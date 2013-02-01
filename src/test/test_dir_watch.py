
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.defer import DeferredList
from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest

import pdboard.tw_simple_proc as tsp
from pdboard.dir_watch import Dir_Watcher

from functools import partial


TOUCH = '/usr/bin/touch'
RM = '/usr/bin/rm'

class fileSystemTester(object):
    def __init__(self, dir_path, nfiles):
        self.dir_path = dir_path
        self.nfiles = nfiles
        self.touch = partial(doFileops, TOUCH)
        self.rm = partial(doFileops, RM)
        self.fnames = ["{0}/{1}.testtouch".format(self.dir_path,str(i)) 
            for i in range(self.nfiles)]
        self.cmds=[]
        self.outs = []

    def run_touch(self):
        return DeferredList(list(self.touch(self.fnames)))

    def run_rm(self):
        return DeferredList(list(self.rm(self.fnames)))

    @inlineCallbacks
    def do_cmds(self):
        ncmd = self.cmds.pop(0)
        ml = yield getattr(self, ncmd)()
        if len(self.cmds) > 0:
            self.do_cmds()

def doFileops(binexe, fnames):
    for i, fname in enumerate(fnames):
        yield tsp.make_def(reactor, False, binexe, fname)     

class DirWatchTest(unittest.TestCase):
    NUMFILES = 50
    def setUp(self):
        self.fsevents = []
        self.mnotify = Dir_Watcher(".")
        self.mnotify.callbacks['all'] = lambda a,b: self.fsevents.append((a,b))
        self.mnotify.events=['all']
        self.tfile = fileSystemTester('.',self.NUMFILES)
    
    def tearDown(self):
        self.mnotify.watcher.loseConnection()
        self.tfile= None
        unittest.TestCase.tearDown(self)
        
    def verify_events(self,ver_events):
        observed = [(f[1].basename().strip('.testtouch'),f[0]) for f in self.fsevents]
        md = {}
        for mevent in observed:
            md.setdefault(int(mevent[0]),[]).append(mevent[1])
        for file_int in range(self.NUMFILES):
            for evnt in ver_events:
                self.assertIn(evnt,md.get(file_int),
                    "{0} not seen for file {1}".format(evnt, file_int))
                self.assertTrue(all([e in ver_events for e in md.get(file_int)]))
        
    @inlineCallbacks    
    def test_file_create_remove(self):
        self.tfile.cmds=['run_touch','run_rm']
        smt = yield self.tfile.do_cmds()
        self.verify_events(['create','attrib'])
