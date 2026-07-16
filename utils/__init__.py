#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
Utility Functions Module
"""

from .common import CommonUtils

class Utils:
    """工具类"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.common = CommonUtils(verbose)
