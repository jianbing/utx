#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from utx import *

if __name__ == '__main__':
    # setting.run_case = {Tag.SMOKE}  # 只运行SMOKE标记的测试用例
    setting.run_case = {Tag.FULL}  # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行SMOKE和SP标记的测试用例

    # setting.check_case_doc = False  # 关闭检测是否编写了测试用例描述

    runner = TestRunner()
    runner.run_test(r"testcase")
