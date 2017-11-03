#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-02
"""
import utx

utx.stop_patch()

from demo.testcase.legion.test_legion import TestLegion
import unittest

suite = unittest.TestSuite()
suite.addTest(TestLegion("test_quit_legion"))
unittest.TextTestRunner(verbosity=3).run(suite)
