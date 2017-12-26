#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import unittest
from utx.BSTestRunner import BSTestRunner


class TestRunner:
    def run_test(self, path="testcase", title='接口自动化测试报告'):
        if not os.path.exists("report"):
            os.mkdir("report")

        report_dir = os.path.abspath("report")
        suite = unittest.TestLoader().discover(path)

        BSTestRunner(report_dir=report_dir, title=title).run(suite)

        print("测试完成，请查看报告")
        os.system("start report")
