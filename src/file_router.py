#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# file_router.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/tw_file_depot

# cli program 
# reads a file's contents, send them to a url,  do errback & callback

import sys
import json
import os

from zope.interface import implements

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, succeed
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from twisted.python import log


from pprint import pprint


agent = Agent(reactor)

class FileRouterException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class StringReciever(Protocol):
    def __init__(self, dfrd):
        self.deferred = dfrd
        self.data = []

    def dataReceived(self, bytes_in):
        self.data.append(bytes_in)

    def connectionLost(self, reason):
        self.deferred.callback(self.data)

class FileRouter(object):
    def __init__(self, url, filepath, callback=None):
        """
        @param url = resource to fetch
        @param filepath = string path of file to read
        @param callback = function to call with the filepath as arguement 
            after sucess response from url
        """
        if not os.path.exists(filepath):
            e = FileRouterException('{0} not found'.format(filepath))
            log.err(e)
            raise e
        with open(filepath) as ofile:
            try:
                self.data = json.loads(ofile.read())
            except Exception as e:
                log.error(e)
                raise e
        self.url = url
        self.file_callback = callback
        
    def do_send(self):
        self.deferred = agent.request(
            'PUT',
            self.url,
            Headers(
                {'User-Agent': ['Twisted Web Client Example'],
                'Content-Type':['application/json']}),
            StringProducer(json.dumps(self.data)))
        self.deferred.addCallback(self.cbResponse)
        self.deferred.addCallback(pprint)
        
    def cbResponse(self, response):
        print 'Response received'
        finished = Deferred()
        response.deliverBody(StringReciever(finished))
        #~ print finished.data
        return finished

    def cbShutdown(self, ignored):
        reactor.stop()

myfr = FileRouter('http://localhost:5000','./test/test_data.json')
myfr.do_send()
reactor.run()






