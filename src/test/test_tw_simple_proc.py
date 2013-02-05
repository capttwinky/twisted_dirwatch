#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# test_tw_simple_proc.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/tw_file_depot


from twisted.internet import reactor as mreact
from pprint import pprint
from dir_watch import tw_simple_proc as tsp

'''
mrs = [tsp.make_def(mreact, 0, '/usr/bin/python','./cmdline.py', '30')]
for mr in mrs:
    mr.addCallback(pprint)
mreact.run()
#~ dl = yield DeferredList(mr)
import pdb; pdb.set_trace()
'''
