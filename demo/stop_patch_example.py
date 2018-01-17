#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
如果项目使用utx，在调试单个用例的时候，需要先调用utx.stop_patch()，暂停utx对unittest模块的注入
"""
import utx

utx.stop_patch()  # 如果注释掉这句，运行会报错

from demo.testcase.legion.test_legion import TestLegion
import unittest

suite = unittest.TestSuite()
suite.addTest(TestLegion("test_quit_legion"))
unittest.TextTestRunner(verbosity=3).run(suite)
