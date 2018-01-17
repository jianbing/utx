#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import unittest
from utx import log
from utx.BSTestRunner import BSTestRunner


class TestRunner:

    def __init__(self):
        self.case_dirs = []

    def add_case_dir(self, dir_path):
        """添加测试用例文件夹，多次调用可以添加多个文件夹，会按照文件夹的添加顺序执行用例

            runner = TestRunner()
            runner.add_case_dir(r"testcase\chat")
            runner.add_case_dir(r"testcase\battle")
            runner.run_test(report_title='接口自动化测试报告')

        :param dir_path:
        :return:
        """
        if not os.path.exists(dir_path):
            raise Exception("测试用例文件夹不存在：{}".format(dir_path))
        if dir_path in self.case_dirs:
            log.warn("测试用例文件夹已经存在了：{}".format(dir_path))
        else:
            self.case_dirs.append(dir_path)

    def run_test(self, report_title='接口自动化测试报告'):

        if not self.case_dirs:
            raise Exception("请先调用add_case_dir方法，添加测试用例文件夹")

        if not os.path.exists("report"):
            os.mkdir("report")

        report_dir = os.path.abspath("report")
        suite = unittest.TestSuite()
        for case_path in self.case_dirs:
            suite.addTests(unittest.TestLoader().discover(case_path))
        BSTestRunner(report_dir=report_dir, report_title=report_title).run(suite)

        print("测试完成，请查看报告")
        os.system("start report")
