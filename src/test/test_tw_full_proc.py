#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# test_tw_full_proc.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/...

#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


import pdboard.tw_full_proc as tfp

from twisted.internet import reactor
from twisted.trial import unittest
from twisted.test import proto_helpers

#~ from twisted.internet import defer


import sys
import shlex

def rtrue(*args, **kwargs):
    return True


class FullProcessTest(unittest.TestCase):
    def setUp(self):
        #~ pass
        self.fp = tfp.FullProcess(None, sys.executable, shlex.split('-m pdboard.cmdline 30'))
        
    def t_first(self):
        self.fp.ip_pairs = [('marco',rtrue)]
        reactor.spawnProcess(self.fp, sys.executable, [sys.executable, "echoscript.py"], {})
        md = self.fp.doInputs()
        #~ self.fp.closeConnection()
        #~ import pdb; pdb.set_trace()
FullProcessTest.todo = "implementing this test"



#~! pp = FullProcess(pid, command, deffered)
#~ pp = FullProcess(10)
#~! reactor.spawnProcess(object which manages communication, process to communicate with, ["wc"], {})
#~ reactor.spawnProcess(FullProcess(0, cmd, d), exe, args=call_args,env=os.environ)
#~! reactor.spawnProcess(pp, "wc", ["wc"], {})
#~ reactor.run()
