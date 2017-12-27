#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
仅使用测试报告组件，不需要utx的其他扩展功能
"""

from utx import *

if __name__ == '__main__':
    utx.stop_patch()

    runner = TestRunner()
    runner.run_test(r"testcase\chat")
