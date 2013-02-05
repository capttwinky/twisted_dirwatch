#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from distutils.core import setup
setup(name='dir_watch',
      version='0.1',
      packages=['dir_watch', 'dir_watch.test'],
      package_dir = {'dir_watch':'src','dir_watch.test':'src/test'},
      )
