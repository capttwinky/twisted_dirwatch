#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from twisted.internet import inotify, reactor
from twisted.python import filepath

import tw_simple_proc as tsp

import re

class Dir_Watcher(object):
    def __init__(self, dirpath, name_match = None, events = ['create']):
        '''
        Acts as a filtering and routing layer for inotify
        @param dirpath: FilePath to watch for changes
        @param name_match: regex for files to notify of changes on
        @param events: keys from callback_fns which have been implemented
        note: callback function 'all' will get both the event and the path
        of the triggering file
        '''
        self.watcher = inotify.INotify()
        self.watcher.watch(filepath.FilePath(dirpath), callbacks=[self.notify])
        self.watcher.startReading()
        #~ self.callback_fns['all'] = False
        self.name_regex = re.complie(name_match) if name_match else None
        self.callbacks = {
            'create': create_handler,
            'delete': delete_handler,
            'modify': modify_handler,
            'attrib': attrib_handler,
            'all': all_callback}
            
    def notify(self, ignored, filepath, mask):
       """
       For historical reasons, an opaque handle is passed as first
       parameter. This object should never be used.

       @param filepath: FilePath on which the event happened.
       @param mask: inotify event as hexadecimal masks
       """
       if self.name_regex and not self.name_regex.match(filepath.basename):
           return None
       str_event = inotify.humanReadableMask(mask)[0]
       if str_event in self.events:
           self.callbacks.get(str_event)(filepath)
       if 'all' in self.events:
           self.callbacks['all'](str_event, filepath)

def create_handler(file_path):
    raise NotImplemented('create called and not defined')
def delete_handler(file_path):
    raise NotImplemented('delete called and not defined')
def modify_handler(file_path):
    raise NotImplemented('modify called and not defined')
def attrib_handler(file_path):
    raise NotImplemented('attrib called and not defined')
def all_callback(event_name, file_path):
    raise NotImplemented('all called and not defined')



#### test functions below here

import functools
from pprint import pprint

def print_event(str_event, filepath):
    '''uses a dummy script to emulate sending to another process'''
    strme = "{0} - {1}".format(str_event, filepath.path)
    md = tsp.make_def(reactor, 0, '/usr/bin/python','./cmdline.py', strme)
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
