#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
单独使用测试报告组件，不需要utx的其他扩展功能
"""
import utx

if __name__ == '__main__':

    utx.stop_patch()

    runner = utx.TestRunner()
    runner.add_case_dir(r"testcase\chat")
    runner.run_test(report_title='接口自动化测试报告')