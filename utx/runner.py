#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import unittest
from utx.BSTestRunner import BSTestRunner


class TestRunner:
    @staticmethod
    def run_test(*case_paths, title='接口自动化测试报告'):
        """执行测试入口，支持导入多个文件夹的测试用例

        runner = TestRunner()
        runner.run_test(r"testcase\battle",r"testcase\chat")

        :param case_paths: 测试文件夹的路径
        :param title: 测试报告标题
        :return:
        """
        if not os.path.exists("report"):
            os.mkdir("report")

        report_dir = os.path.abspath("report")
        suite = unittest.TestSuite()
        for case_path in case_paths:
            suite.addTests(unittest.TestLoader().discover(case_path))
        BSTestRunner(report_dir=report_dir, title=title).run(suite)

        print("测试完成，请查看报告")
        os.system("start report")
