#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from utx import *

if __name__ == '__main__':
    setting.run_case = {Tag.FULL}  # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE}  # 只运行SMOKE标记的测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行SMOKE和SP标记的测试用例
    # setting.check_case_doc = False  # 关闭检测是否编写了测试用例描述
    setting.full_case_name = True
    setting.max_case_name_len = 80  # 测试报告内，显示用例名字的最大程度
    setting.show_error_traceback = True  # 执行用例的时候，显示报错信息
    setting.sort_case = True  # 是否按照编写顺序，对用例进行排序

    runner = TestRunner()
    runner.add_case_dir(r"testcase")
    runner.run_test(report_title='接口自动化测试报告')
