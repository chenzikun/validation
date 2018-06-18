#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安装程序
"""
__author__ = "chenzikun"

# todo 写安装程序

import setuptools

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(
    setup_requires=['pbr>=1.8'],
    pbr=True
)
