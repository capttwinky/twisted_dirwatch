#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# .py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/tw_file_depot

from twisted.internet import reactor
import functools
from sys import executable
from pprint import pprint
import tw_simple_proc as tsp

def print_event(str_event, filepath):
    '''uses a dummy script to emulate sending to another process'''
    strme = "{0} - {1}".format(str_event, filepath.path)
    md = tsp.make_def(reactor, 0, executable, './cmdline.py', strme)
    md.addCallback(pprint)

## create a watcher for a directory
my_notify = Dir_Watcher("/tmp/filewatch")

## register one or more callback functions - can be put on queues from here as well
my_notify.callbacks['create'] = functools.partial(print_event,'c')
my_notify.callbacks['modify'] = functools.partial(print_event,'m')
my_notify.callbacks['delete'] = functools.partial(print_event,'d')
my_notify.callbacks['attrib'] = functools.partial(print_event,'a')

## turn on the listeners for the scripted events
my_notify.events = ['create','modify','delete','attrib']

reactor.run()
