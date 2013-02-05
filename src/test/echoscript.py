#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmcgrady@twitter.com
#
# echoscript.py
# REFS: JIRA HWENG-
# REPO: http://cgit.twitter.biz/tw_file_depot

## just a simple little testing script to process stdin -> stdout
## usefull for testing process protocols

while True:
    md = raw_input()
    print len(md)
