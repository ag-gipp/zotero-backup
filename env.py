#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

__ready__ = False


def _get_log_level():
    loglevel = os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    return numeric_level


def _init_logger():
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    outdir = os.getenv("ZB_OUT_DIR", "out")

    handler = logging.FileHandler(outdir + '/application.log')
    handler.setLevel(_get_log_level())
    handler.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    l = logging.getLogger()
    l.setLevel(logging.DEBUG)
    l.addHandler(handler)
    l.addHandler(ch)


def init():
    """ready the environment"""
    global __ready__
    if not __ready__:
        _init_logger()
        __ready__ = True


def logger():
    """get a logger"""
    if not __ready__:
        init()
    return logging.getLogger()
