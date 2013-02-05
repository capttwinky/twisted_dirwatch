#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# tw_full_proc.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/...

#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.trial import unittest


import twisted.internet.protocol as protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import DeferredQueue
from twisted.internet.defer import Deferred
from twisted.internet.defer import returnValue

import re




class FullProcess(protocol.ProcessProtocol):
    def __init__(self, pid, exe, command):
        self.exe = exe
        self.command = command
        self.pid = pid  #for use with future implemention twisted.runner's process manager class
        ##~ self.ip_strs = [(str_to_send, fn_return_parse)]
        self.ip_pairs = []
        self.stage = "init"
        
        self.dqueue=DeferredQueue()
    
    def connectionMade(self, strin=False):
        '''child process has started'''
        self.stage = "!!!!connected!!!!!"
        print "connected"
        #~ self.doInputs()  ##to implement
        
    def closeConnection(self):
        self.stage = "connection closed"
        self.transport.closeStdin() # tell them we're done
        
    def outReceived(self, data):
        print "outReceived! with %d bytes!" % len(data)
        print data
        self.dqueue.put(data)
        
    def errReceived(self, data):
        self.status = 'error_back'
        print "errReceived! with %d bytefrom twisted.internet.defer import DeferredLists!" % len(data)

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        self.satus = "child closed"
        print "outConnectionLost! The child closed their stdout!"
        # now is the time to examine what they wrote
        #print "I saw them write:", self.data
        #~ self.cleanup() ## to implement
        
    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."
        
    def processExited(self, reason):
        self.status='exited'
        print "processExited, status %d" % (reason.value.exitCode,)
        
    def processEnded(self, reason):
        self.status='ended'
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()

    @inlineCallbacks
    def doInputs(self):
        self.stage = 'running commands'
        dlist = DeferredList()
        for (input_string, verify_callback) in self.ip_pairs:
            print input_string
            self.transport.write(input_string)
            child_def = yield self.dqueue.get()
            child_def.addCallback(verify_callback)
            dlist.append(child_def)
            #~ print str_ret
            #~ if not verify_callback(str_ret):
                #~ raise Exception("cmd broken")
        mret = yield dlist
        returnValue(mret)

#~~pp = FullProcess(pid, command, deffered)
#~ pp = FullProcess(10)
#~~reactor.spawnProcess(object which manages communication, process to communicate with, ["wc"], {})
#~ reactor.spawnProcess(FullProcess(0, cmd, d), exe, args=call_args,env=os.environ)
#~~reactor.spawnProcess(pp, "wc", ["wc"], {})
#~ reactor.run()
