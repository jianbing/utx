#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-02
"""
import utx
from demo.testcase.legion.test_legion import TestLegion
import unittest

utx.stop_patch()

print(dir(TestLegion))
s = unittest.TestSuite()
s.addTest(TestLegion("test_quit_legion"))
unittest.TextTestRunner(verbosity=3).run(s)
