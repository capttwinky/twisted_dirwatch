#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
## run batch of jobs -- also need something to manage the batch
import os
import shlex

from twisted.internet.protocol import ProcessProtocol

from twisted.internet import threads
from twisted.internet.defer import Deferred
from twisted.internet.defer import DeferredList
from twisted.mail.smtp import sendmail
from email.mime.text import MIMEText

class FetcherError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class SimpleProcess(ProcessProtocol):
    '''runs python scripts in a different process'''
    def __init__(self, id, cmd, d):
        self.id = id
        self.d = d
        self.cmd = cmd
        self.data = []
        self.errors = []
    def outReceived(self, data):
        self.data.append(data)
    def errReceived(self, data):
        self.errors.append(FetcherError("{0} invalid with {1}".format(self.id, data)))
    def outConnectionLost(self):
        if self.errors:
            self.d.errback(self.errors)
        else:
            self.d.callback(((self.id,self.cmd), ''.join(self.data)))

def make_def(reactor, delay, exe, cmd, *args):
    if callable(cmd):
        to_yield = threads.deferToThread(cmd, cid)
    else:
        d = Deferred()
        call_args = [exe]+ shlex.split(cmd)
        if args:
            call_args.extend(args)
        if not delay:
            reactor.spawnProcess(SimpleProcess(0, cmd, d),
                exe, args=call_args,env=os.environ)
        else:
            reactor.callLater(delay, reactor.spawnProcess,
            SimpleProcess(0, cmd, d), exe, args=call_args, env=os.environ)
        to_yield = d
    return to_yield

def mail_def(to_addrs, message, subject):
    '''to_addrs := list of target email addresses'''
    from_addr = 'hweng@twitter.com'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    return sendmail('localhost', from_addr, to_addrs, msg.as_string())
