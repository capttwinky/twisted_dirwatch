#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import random
from time import sleep

e_strs = 'Server Error,Request Timeout'.split(',')

class dframe(object):
    def __init__(self, coef, value):
        self.value = "{0}: {1}".format(coef, value)

def main(marg):
    mi = random.choice(range(500,5000))/1000.0
    sleep(mi)
    if random.choice((True, False)):
        d_tag = 'results'
    else:
        d_tag = random.choice(e_strs)
    md = dframe(marg, "{0} after {1}".format(d_tag,mi))
    print md.value
    
if __name__ == '__main__':
    import sys
    main(str(sys.argv[1]))
