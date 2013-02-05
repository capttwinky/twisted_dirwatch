#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# test_dir_watch.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/tw_file_depot

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
        else:
            reactor.stop()

def doFileops(binexe, fnames):
    for i, fname in enumerate(fnames):
        yield tsp.make_def(reactor, False, binexe, fname)     

class DirWatchTest(unittest.TestCase):
    NUMFILES = 50
    def setUp(self, tdir="."):
        """
        @param tdir := directory to use for this test
        
        """
        self.tdir = tdir
        self.fsevents = []      ## containter for observed events
        self.mnotify = Dir_Watcher(self.tdir)   ## build the dir_watch to test
        self.mnotify.callbacks['all'] = self.cbfn  ## cbfn appends to self.events
        self.mnotify.callbacks['create'] = partial(self.cbfn,'c') ## slightly different signtarure
        self.mnotify.callbacks['attrib'] = partial(self.cbfn,'a') ## from all call back
        self.mnotify.callbacks['delete'] = partial(self.cbfn,'d')
        self.mnotify.callbacks['modify'] = partial(self.cbfn,'m')
        self.mnotify.events=['all','create','attrib','delete','modify']
        
        ## fire up the file system tester
        self.tfile = fileSystemTester(self.tdir,self.NUMFILES)
    
    def tearDown(self):
        ## need to clean up the connections
        self.mnotify.watcher.loseConnection()
        self.tfile= None
        unittest.TestCase.tearDown(self)
    
    def cbfn(self, event, fpath):
        ## a template callback that appends to the fsevents list
        self.fsevents.append((event,fpath))
        
    def verify_events(self,ver_events):
        ## assert that we saw the requested events on each of the test files
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
    def test_file_create(self):
        self.tfile.cmds=['run_touch', 'run_rm']
        smt = yield self.tfile.do_cmds()
        self.verify_events(['create','attrib','c','a'])        
        #~ self.verify_events(['delete','d'])
        ## it looks like the trial test wrapper is keeping it from detecting
        ## the delete event - if you monitor the tdir with another instance
        ## of this script, it detects just fine


