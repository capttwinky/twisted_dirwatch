twisted_dirwatch
================

Twisted's inotify watches for changes in a directory, reactor handles response in a different thread or process.

Contents
========
README.md: this file
.gitignore: guess
/src
  cmdline.py: a simple test script that simulates random processing latency
  dir_watch.py: the main file for this module
  tw_simple_proc.py: simple implementation of twisted's process protocol & interface to threadding
  

To Use
======
1. import the module

    import dir_watch
    
2. create a watcher for a directory

    my_notify = Dir_Watcher("/tmp/filewatch")

3. register one or more callback functions
    a. declare a function that takes the event string and twisted FilePath
    b. use tw_simple_proc for parallel processing of events
    c. can also use Queue.Queue, etc.

    def callbackfn(event, filepath):
        print filepath
        
    my_notify.callbacks['create'] = callbackfn

4) turn on the listeners for the scripted events
    
    my_notify.events = ['create']

5) run your reactor
    
    reactor.run()

6) enjoy with family and friends.
